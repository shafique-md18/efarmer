from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm, LoginForm


def home_page(request):
    context = {
        "title": "Hello World!",
    }
    return render(request, "home_page.html", context)

def contact_page(request):
    form = ContactForm(request.POST or None) # submitted data stays on webpage
    context = {
        "title": "Contact Us",
        "form": form,
    }
    if form.is_valid():
        print(form.cleaned_data)
    return render(request, "contact/contact.html", context)

def login_page(request):
    form = LoginForm(request.POST or None)
    print("User logged in: ", request.user.is_authenticated())
    context = {
        "form": form,
    }
    if form.is_valid():
        print(form.cleaned_data)
        # get username and password
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        # log user in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # clear the form when the user logs in
            context['form'] = LoginForm()  # empty form
            return redirect("/login")
        else:
            print("Error")
        print("User logged in: ", request.user.is_authenticated())
    return render(request, "auth/login.html", context)

def register_page(request):
    return render(request, "auth/register.html", {})