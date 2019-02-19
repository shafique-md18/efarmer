from django.db import models
import os
from uuid import uuid4
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.urls import reverse


def path_and_rename(instance, filename):
    upload_to ="products/"
    ext = filename.split('.')[-1]
    if instance.pk:
        new_filename = f'{instance.pk}.{ext}'
    else:
        # primary key is not present, set filename as random string
        new_filename = f'{uuid4().hex}.{ext}'
    return os.path.join(upload_to, new_filename)



class Category(models.Model):
    name = models.CharField('Category', max_length=30, default="", db_index=True, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def get_absolute_url(self):
        return reverse('products:product_list', kwargs={"slug":self.slug})

    def __str__(self):
        return self.name


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def recently_added(self):
        return self.all().order_by('-created_at')

class ProductManager(models.Manager):
    """ extend existing product manager,
        provide database query operations
    """

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_featured(self, num_of_products=0):
        return self.get_queryset().featured()[:num_of_products]

    def get_recently_added(self, num_of_products=0):
        return self.get_queryset().recently_added()[:num_of_products]


class Product(models.Model):
    name = models.CharField('Product Name', max_length=120)
    brand = models.CharField('Brand', default="", max_length=120)
    size = models.CharField('Size', default="", max_length=10, blank=True)
    stock = models.PositiveIntegerField('Stock', default=0)
    description = models.TextField('Description', blank=True, default="")
    maximum_retail_price = models.DecimalField('Maximum Retail Price', max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField('Selling Price', max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField('Product Image', upload_to=path_and_rename, default='image_not_available.jpg')
    featured = models.BooleanField('Add to featured products?', default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)

    objects = ProductManager()

    class Meta:
        ordering = ('name', )


    def clean(self):
        from django.core.exceptions import ValidationError
        if self.maximum_retail_price < 0:
            raise ValidationError("MRP cannot be negative")
        if self.selling_price < 0:
            raise ValidationError("Selling Price cannot be negative.")
        if self.selling_price > self.maximum_retail_price:
            raise ValidationError("Selling Price cannot be greater than MRP.")

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={"slug":self.slug})


    def is_featured(self):
        return self.featured

    def is_available(self):
        return self.stock > 0

    def __str__(self):
        return self.name

def pre_save_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, Product)
pre_save.connect(pre_save_receiver, Category)

