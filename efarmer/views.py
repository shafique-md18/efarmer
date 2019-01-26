from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm


def home_page(request):
    context = {
        "title": "Hello World!",
    }
    return render(request, "home_page.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None) # submitted data stays on webpage
    context = {
        "title": "Contact Us",
        "form": contact_form,
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request, "contact/contact.html", context)