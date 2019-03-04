from django.shortcuts import render, redirect, HttpResponse
from .models import Cart
from products.models import Product


def cart_home(request):
    cart_obj = Cart.objects.get_or_create_cart(request)
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
        cart_obj = Cart.objects.new_or_get(request)
        print(cart_obj.id)
        if remove_product:
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
        request.session['cart_items'] = cart_obj.products.count()
        # return redirect(product_obj.get_absolute_url())
    return redirect("carts:cart")