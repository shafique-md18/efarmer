from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.http import Http404
from django.shortcuts import get_object_or_404
import random


class ProductCategoryListView(ListView):
    template_name = "products/product_list.html"

    def get_context_data(self, **kwargs):
        """
        Method is used here just to have the category name in the context object
        :param kwargs:
        :return:
        """
        slug = self.kwargs.get('slug')
        # context is obtained from the get_queryset() method defined below
        context = super(ProductCategoryListView, self).get_context_data(**kwargs)
        category = Category.objects.get(slug__iexact=slug)
        context['category'] = category.name.capitalize()
        return context

    def get_queryset(self, **kwargs):
        # get the query set for the matching category of products
        slug = self.kwargs.get('slug')
        try:
            # category is expected to be a single distinct object
            category = Category.objects.get(slug__iexact=slug)
        except Category.DoesNotExist:
            raise Http404("Category does not exist!")
        except:
            raise Http404("Something terrible has happened!")
        products = Product.objects.filter(category__slug__iexact=slug, stock__gt=0).order_by('?')
        # return random sample of products - NOT EFFICIENT
        return products


class ProductDetailView(DetailView):
    template_name = "products/product_detail.html"
    # queryset = Product.objects.all()

    def get_context_data(self, pk=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context

    def get_object(self, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Product does not exist!")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something terrible has happened :(")

        return instance
