from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.urls import reverse
from .forms import LoginForm, RegistrationForm
from django.http import HttpResponse
from orders.models import Order
from addresses.models import Address
from billings.models import BillingProfile


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
    next_ = request.GET.get('next', None)
    next_post = request.POST.get('next', None)
    redirect_to = next_ or next_post
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = User.objects.create_user(username, email, password)
        if user is not None:
            user.save()
            return redirect(reverse('login_page') + f'?next={redirect_to}')
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


def my_account(request):
    if not request.user.is_authenticated():
        return redirect('home')
    billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
        user=request.user, email=request.user.email)
    addresses = Address.objects.filter(billing_profile=billing_profile)
    orders = Order.objects.filter(billing_profile=billing_profile, active=False)
    context = {
        'addresses': addresses,
        'orders': orders,
    }
    return render(request, 'auth/my_account.html', context)