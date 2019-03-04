from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django import forms
from django.utils.http import is_safe_url
from .forms import LoginForm, RegistrationForm
from django.http import HttpResponse

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form,
    }
    next_ = request.GET.get('next', None)
    next_post = request.POST.get('next', None)
    redirect_to = next_ or next_post
    if request.user.is_authenticated():
        return redirect(redirect_to or "home")
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

            if request.session.get('cart_id', None):
                # assign cart_id to the user session
                user = request.user
                user_carts = user.cart_set.all()
                active_user_cart = user_carts.filter(active=True).first()
                request.session['cart_id'] = active_user_cart.id or None

            # redirect user
            if redirect_to and is_safe_url(redirect_to):
                return redirect(redirect_to)
            return redirect("home")
        else:
            context['login_error'] = True
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
        # remove cart when user logs out
        request.session['cart_id'] = None
        logout(request)
    return redirect("home")