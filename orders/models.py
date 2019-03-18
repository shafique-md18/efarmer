from django.db import models
from django.contrib.auth.models import User
from utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
from carts.models import Cart
from billings.models import BillingProfile
from addresses.models import Address
from math import fsum

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

ORDER_PAYMENT_METHODS = (
    ('cash_on_delivery', 'Cash On Delivery'),
)

SHIPPING_COST = 140.00


class OrderManager(models.Manager):
    def get_or_create_order(self, billing_profile, cart_obj):
        obj = None
        obj_created = False
        # get all the incomplete active order of same user with same cart
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True)
        # current order object or previously created object
        if qs.count() == 1:
            obj = qs.first()
        # previously created incomplete objects
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj
            )
            obj_created = True
        return obj, obj_created



class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    shipping_address = models.ForeignKey(Address, blank=True, null=True)
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    cart = models.ForeignKey(Cart)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=140.00, decimal_places=2, max_digits=20)
    order_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    payment_method = models.CharField(max_length=120, default='cash_on_delivery', choices=ORDER_PAYMENT_METHODS)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderManager()

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
    # Issue: might need some extra logic to handle multiple orders of same cart


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