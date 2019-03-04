from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, m2m_changed


STATUS = (
    (True, 'Active'),
    (False, 'Inactive'),
)


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            cart_obj = qs.first()
            # if logged in and the guest cart is present
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_id = self.associate_user_with_cart(request, cart_obj)
                # cart_id is changed if user has logged in with a guest cart
                cart_obj = self.get_queryset().filter(id=cart_id).first()
                cart_obj.active = True
                cart_obj.save()
        else:
            # cart_id is assigned to existing user when he logsin in the accounts app
            # new user
            cart_obj = Cart.objects.new(user=request.user)
            cart_obj.active = True
            cart_obj.save()
            request.session['cart_id'] = cart_obj.id
        return cart_obj


    def get_or_create_cart(self, request):
        cart_id = request.session.get("cart_id", None)
        obj = None
        if cart_id is None:
            obj = Cart()
            obj.active = True
            obj.save()
            request.session['cart_id'] = obj.id
        else:
            qs =  self.get_queryset().filter(id=cart_id)
            if qs.count() == 1:
                obj = qs.first()
                # if logged in and the guest cart is present
                if request.user.is_authenticated() and obj.user is None:
                    cart_id = self.associate_user_with_cart(request, obj)
                    # cart_id is changed if user has logged in with a guest cart
                    request.session['cart_id'] = cart_id
                    obj = self.get_queryset().filter(id=cart_id).first()
                    obj.active = True
                    obj.save()
            else:
                raise Exception(f'Error while looking up cart via cart_id: {cart_id}')
        return obj

    def new(self, user=None):
        # new empty cart with just user associated
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)

    def associate_user_with_cart(self, request, cart_obj):
        # associate user with cart if user logs in after cart creation
        # check if user already has a cart alloted in db
        user = request.user
        user_carts = user.cart_set.all()
        active_user_carts = user_carts.filter(active=True)
        cart_id = cart_obj.id
        if active_user_carts.count() == 1 :
            # user already has a cart in db and the guest cart has atleast 1
            # product, copy the guest cart in the user cart
            if cart_obj.products.count() > 0:
                for product in cart_obj.products.all():
                    if product not in user_carts.first().products.all():
                        user_carts.first().products.add(product)
                user_carts.first().save()
            # delete the guest cart
            cart_obj.delete()
            cart_id = user_carts.first().id
        elif active_user_carts.count() > 1:
            raise Exception("More than one active carts for the user")
        else:
            # user has no carts
            cart_obj.user = request.user
            cart_obj.save()
        return cart_id


class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    active = models.BooleanField(default=False, choices=STATUS)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return str(self.id)

    class Meta:
        ordering = ('-created_at', )


def cart_items_changed(sender, instance, pk_set, action, **kwargs):
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        # recalculate cart total
        total = 0
        for product in instance.products.all():
            total += product.selling_price
        instance.total = total
        instance.save()


m2m_changed.connect(cart_items_changed, sender=Cart.products.through)