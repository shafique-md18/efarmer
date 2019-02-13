from django.db import models
import os
from uuid import uuid4


def path_and_rename(instance, filename):
    upload_to ="products/"
    ext = filename.split('.')[-1]
    if instance.pk:
        new_filename = f'{instance.pk}.{ext}'
    else:
        # primary key is not present, set filename as random string
        new_filename = f'{uuid4().hex}.{ext}'
    return os.path.join(upload_to, new_filename)


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to=path_and_rename, default='image_not_available.jpg')

    def __str__(self):
        return self.title
