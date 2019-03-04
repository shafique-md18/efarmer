from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, m2m_changed


class CartManager(models.Manager):
    def get_or_create_cart(self, cart_id=None):
        obj = None
        if cart_id is None:
            obj = Cart()
            obj.save()
        else:
            qs =  self.get_queryset().filter(id=cart_id)
            if qs.count() == 1:
                obj = qs.first()
            else:
                raise Exception(f'Error while looking up cart via cart_id: {cart_id}')
        return obj


class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)

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
        total = 0;
        for product in instance.products.all():
            total += product.selling_price
        instance.total = total
        instance.save()


m2m_changed.connect(cart_items_changed, sender=Cart.products.through)