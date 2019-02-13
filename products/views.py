from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/product_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/product_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        print(context['object'].title)
        print(context['object'].description)
        print(context['object'].price)
        return context