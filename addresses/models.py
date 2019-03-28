from django.db import models
from billings.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

COUNTRIES = (
    ('india', 'India'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    full_name = models.CharField(max_length=120, blank=True)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20, default='india', choices=COUNTRIES)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)


    def __str__(self):
        return f'{self.billing_profile.email} - {self.id}'

    def get_name(self):
        return self.__str__()
