from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.http import Http404
import string
from django.shortcuts import get_object_or_404


class ProductListView(ListView):
    template_name = "products/product_list.html"

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        slugqs = Category.objects.filter(slug__iexact=slug)
        print(slugqs)
        if slugqs.count() == 0:
            raise Http404("Category Doesn't Exist!")
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['category'] = slugqs.first().name.capitalize()
        return context

    def get_queryset(self, **kwargs):
        slug = self.kwargs.get('slug')
        # print(Product.objects.filter(category__name__iexact=category))
        try:
            categoryqs = Category.objects.filter(slug__iexact=slug)
        except Category.DoesNotExist:
            raise Http404("Category does not exist!")
        except:
            raise Http404("Something terrible has happened!")
        return Product.objects.filter(category__slug__iexact=slug)


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
