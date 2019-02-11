from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm, LoginForm, RegistrationForm
from django.contrib.auth.models import User
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

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        # get username and password
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        # log user in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # clear the form when the user logs in
            context['form'] = LoginForm()  # empty form
            return redirect("home")
        else:
            print("Error")
    return render(request, "auth/login.html", context)


def register_page(request):
    if request.user.is_authenticated():
        return redirect("home")
    # fill the form with the last post request if the form has validation errors
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = User.objects.create_user(username, email, password)
        if user is not None:
            user.save()
            return redirect("home")
        else:
            print("Error creating the user")
    context = {
        'form': form,
    }
    return render(request, "auth/register.html", context)

def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect("home")