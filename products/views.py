from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product
from django.http import Http404
from django.shortcuts import get_object_or_404


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/product_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context


class ProductDetailView(DetailView):
    template_name = "products/product_detail.html"
    # queryset = Product.objects.all()

    def get_context_data(self, pk=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        print(context['object'].title)
        print(context['object'].description)
        print(context['object'].selling_price)
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
