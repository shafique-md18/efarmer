from django.shortcuts import render
from django.views.generic import ListView, DetailView
from products.models import Product, Category
from django.http import Http404
from django.shortcuts import get_object_or_404


class SearchProductListView(ListView):
    template_name = "search/search_list.html"

    def get_context_data(self, **kwargs):
        context = super(SearchProductListView, self).get_context_data(**kwargs)
        query = self.request.GET.get("q")
        context['featured_list'] = Product.objects.get_featured(5)
        context['query'] = query
        print(context)
        return context

    def get_queryset(self, **kwargs):
        search_query = self.request.GET.get('q')
        if search_query is None:
            return Product.objects.get_featured(5)
        return Product.objects.search(search_query)