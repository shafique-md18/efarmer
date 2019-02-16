from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm
from products.models import Product, Category
from django import forms

def home_page(request):
    product_qs = Product.objects.all()
    category_qs = Category.objects.all()
    features_qs = Product.objects.get_featured(5)
    recently_added_qs = Product.objects.get_recently_added(5)
    context = {
        "title": "E-Farmer | Homepage",
        "products": product_qs,
        "categories": category_qs,
        "featured_products": features_qs,
        "recently_added": recently_added_qs,
    }
    return render(request, "home_page.html", context)

def contact_page(request):
    form = ContactForm(request.POST or None) # submitted data stays on form
    context = {
        "title": "Contact Us",
        "form": form,
    }
    if form.is_valid():
        print(form.cleaned_data)
    return render(request, "contact/contact.html", context)
