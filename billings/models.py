from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class BillingProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    active = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


def user_created_receiver(sender, instance, created, **kwargs):
    # create a billing profile for every new user
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)
