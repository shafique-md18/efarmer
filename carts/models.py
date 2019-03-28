from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, m2m_changed


STATUS = (
    (True, 'Active'),
    (False, 'Inactive'),
)


class CartManager(models.Manager):

    def get_or_create_cart_1(self, request):
        cart_id = request.session.get("cart_id", None)
        obj = None
        obj_created = False
        # new user with no guest cart
        if cart_id is None:
            obj = Cart()
            obj.active = True
            obj.save()
            obj_created = True
            request.session['cart_id'] = obj.id
        # user with guest cart present
        else:
            qs =  self.get_queryset().filter(id=cart_id)
            qs = qs.filter(active=True)
            # user already has an active cart
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
            # user does not have an active cart
            elif qs.count() == 0:
                # get the guest cart
                obj = self.get_queryset().filter(id=cart_id).first()
                # user with a guest cart but no user associated cart
                if request.user.is_authenticated() and obj.user is None:
                    obj.user = request.user
                    obj.save()
            else:
                raise Exception(f'Error while looking up cart via cart_id: {cart_id}, {qs.count()}')
        return obj, obj_created


    def get_or_create_cart(self, request):
        """
        gets the current active cart for the given user or creates one
        if doesnt exist
        :param request:
        :return: object, object_created(bool)
        """
        # for guest session
        guest_cart_id = request.session.get("cart_id", None)
        guest_cart = None
        if guest_cart_id is not None:
            # guest_cart_id is valid
            guest_cart = self.model.objects.filter(id=guest_cart_id, active=True).first()
        # for authenticated users
        object = None
        object_created = False
        if request.user.is_authenticated():
            # return the current active cart if exists
            qs = self.model.objects.filter(user=request.user, active=True)
            if qs.count() == 1:
                object = qs.first()
                if guest_cart is not None and guest_cart.user is None:
                    # user has cart and guest cart exists
                    cart_id = self.associate_user_with_cart(request, guest_cart)
                    # maybe local(object) does not change ? BUG
                    object = self.model.objects.filter(id=cart_id, active=True).first()
                    request.session['cart_id'] = cart_id
                else:
                    # user has a cart and guest cart doesn't exist
                    # object -> user cart, object_created -> false
                    pass
            elif qs.count() > 1:
                raise Exception("User has more than one active carts!")
            else:
                # user does not have a cart allocated to him, but guest cart exists
                if guest_cart is not None and guest_cart.user is None:
                    object = guest_cart
                    # map user
                    object.user = request.user
                    object.save()
                else:
                    # user does not have a cart allocated to him and guest cart doesnt exist
                    object = self.new(active=True, user=request.user)
                    object_created = True
        else:
            if guest_cart_id is None: # new guest user
                object = self.new(active=True)
                object_created = True
                request.session['cart_id'] = object.id
            else:
                object = self.model.objects.filter(id=guest_cart_id, active=True).first()
                if object is None:
                    # if cart with id guest_cart_id does not exist, create new cart
                    object = self.new(active=True)
                    object_created = True
                    request.session['cart_id'] = object.id # save cart id to user
        return (object, object_created)



    def new(self, active=False, user=None):
        """
        creates new cart for the given user,
        active state is default
        :param user:
        :return: newly created cart object
        """
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj, active=active)



    def associate_user_with_cart(self, request, cart_obj):
        """
        sets cart_obj.user to request.user if request.user doesnt have any active cart
        copies cart_obj to the request.user cart and delete cart_obj, otherwise
        :param request:
        :param cart_obj:
        :return: cart_id
        """
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
                    if product not in active_user_carts.first().products.all():
                        active_user_carts.first().products.add(product)
                active_user_carts.first().save()
            # delete the guest cart
            cart_obj.delete()
            cart_id = active_user_carts.first().id
        elif active_user_carts.count() > 1:
            raise Exception("More than one active carts for the user")
        else:
            # user has no carts
            cart_obj.user = request.user
            cart_obj.save()
        return cart_id

    def change_cart_status(self, cart_id, active):
        qs = Cart.objects.filter(id=cart_id)
        object = qs.first()
        object.active = active
        object.save()
        return object.active


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
            return f'{self.user.username} - {self.id}'
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