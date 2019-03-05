from django.db import models
from django.contrib.auth.models import User
from utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
from carts.models import Cart
from math import fsum

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

SHIPPING_COST = 140.00


class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    cart = models.ForeignKey(Cart)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=140.00, decimal_places=2, max_digits=20)
    order_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

    def update_total(self):
        if self.cart.total < 500:
            self.shipping_total = SHIPPING_COST
            # correction for decimal and float addition
            self.order_total = format(fsum([self.cart.total, self.shipping_total]), '.2f')
        else:
            self.shipping_total = 0
            self.order_total = format(fsum([self.cart.total, self.shipping_total]), '.2f')
        self.save()
        return self.order_total

def pre_save_order_receiver(sender, instance, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


# update total of order if cart changes
def post_save_cart_total_receiver(sender, instance, **kwargs):
    cart_id = instance.id
    qs = Order.objects.filter(cart__id=cart_id)
    if qs.count() == 1:
        order_obj = qs.first()
        order_obj.update_total()

# update total when order is first created
def post_save_order_created(sender, instance, created, **kwargs):
    if created:
        instance.update_total()


pre_save.connect(pre_save_order_receiver, Order)
post_save.connect(post_save_cart_total_receiver, Cart)
post_save.connect(post_save_order_created, Order)