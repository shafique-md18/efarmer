from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm
from django import forms

def home_page(request):
    context = {
        "title": "E-Farmer | Homepage",
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
