from django.shortcuts import render, redirect, HttpResponse
from .models import Cart
from products.models import Product
from orders.models import Order
from billings.models import BillingProfile
from addresses.forms import AddressForm
from addresses.models import Address
from django.utils.http import is_safe_url


def cart_home(request):
    cart_obj, cart_created = Cart.objects.get_or_create_cart(request)
    context = {
        "cart_obj": cart_obj,
    }
    return render(request, "carts/cart.html", context)


def cart_update(request):
    product_id = request.POST.get('product_id')
    remove_product = request.POST.get('remove_product', None)
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Error! Product does not exist!")
            return redirect("carts:cart")
        cart_obj, cart_created = Cart.objects.get_or_create_cart(request)
        print(cart_obj.id)
        if remove_product:
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
        request.session['cart_items'] = cart_obj.products.count()
        # return redirect(product_obj.get_absolute_url())
    return redirect("carts:cart")


def checkout_home(request):
    context = {}
    if request.user.is_authenticated():
        # checkout will be after cart view, ie when cart is created
        cart_obj, cart_created = Cart.objects.get_or_create_cart(request)
        if cart_obj.products.count() == 0:
            # cart is empty redirect to cart view
            return redirect("carts:cart")
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            user=request.user, email=request.user.email)

        if billing_profile is not None:
            order_obj, order_obj_created = Order.objects.get_or_create_order(
                billing_profile, cart_obj
            )

        billing_address_form = AddressForm()
        shipping_address_form = AddressForm()
        addresses = Address.objects.filter(billing_profile=billing_profile) or None

        context = {
            'object': order_obj,
            'addresses': addresses,
            'billing_profile': billing_profile,
            'shipping_address_form': shipping_address_form,
        }
    return render(request, "carts/checkout.html", context)


def checkout_address_create(request):
    next_ = request.GET.get('next', None)
    next_post = request.POST.get('next', None)
    redirect_to = next_ or next_post
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            print('Form is valid')
            model_instance = form.save(commit=False)
            model_instance.address_type = form.cleaned_data.get('address_type') or 'shipping'
            model_instance.billing_profile = BillingProfile.objects.filter(user=request.user).first()
            print(model_instance)
            model_instance.save()
            if redirect_to and is_safe_url(redirect_to):
                return redirect(redirect_to)
            return redirect('home')
    else:
        form = AddressForm()
        context = {
            'shipping_address_form': form,
        }
        return render(request, 'carts/create_address.html', context)