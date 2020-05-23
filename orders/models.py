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
    ('placed', 'Placed'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('cancelled', 'Cancelled'),
    ('refunded', 'Refunded'),
)

ORDER_PAYMENT_METHODS = (
    ('cash_on_delivery', 'Cash On Delivery'),
)

SHIPPING_COST = 140.00


class OrderManager(models.Manager):
    def get_or_create_order(self, billing_profile, cart_obj):
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

    def get_active_order(self, billing_profile, cart):
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart,
            active=True)
        return qs.first() or None



class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=140.00, decimal_places=2, max_digits=20)
    order_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    payment_method = models.CharField(max_length=120, default='cash_on_delivery', choices=ORDER_PAYMENT_METHODS)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderManager()


    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.old_status = self.status

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     # when status changes from created to places
    #     # decrement stock of the products
    #     if self.old_status == 'created' and self.status == 'placed':
    #         for product in self.cart.products:
    #             product.decrement_stock()
    #     # if product is cancelled increment stock
    #     if self.status == 'cancelled':
    #         for product in self.cart.products:
    #             product.increment_stock()

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
    if instance.old_status == 'created' and instance.status == 'placed':
        # when status changes from created to places
        # decrement stock of the products
        if instance.old_status == 'created' and instance.status == 'placed':
            for product in instance.cart.products.all():
                product.decrement_stock()
                product.save()
            instance.old_status = 'placed'
            # for adding orders in the admin
            instance.cart.active = False
            instance.cart.save()
            instance.active = False
            instance.save()

    # if product is cancelled increment stock
    if instance.old_status == 'placed' and instance.status == 'cancelled':
        for product in instance.cart.products.all():
            product.increment_stock()
            product.save()
            instance.old_status = 'cancelled'


pre_save.connect(pre_save_order_receiver, Order)
post_save.connect(post_save_cart_total_receiver, Cart)
post_save.connect(post_save_order_created, Order)