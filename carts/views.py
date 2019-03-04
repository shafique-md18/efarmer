from django.shortcuts import render, redirect, HttpResponse
from .models import Cart
from products.models import Product


def cart_home(request):
    # user already has a cart_id assigned to him, or get a new cart as a guest
    cart_obj = Cart.objects.get_or_create_cart(request.session.get('cart_id', None))
    # merge carts if the user has logged in
    cart_id = associate_user_with_cart(request, cart_obj.id)
    if cart_id != cart_obj.id: # if the user has logged in
        request.session['cart_id'] = cart_id
        # cart_obj is old guest cart and will be deleted if the same user logs in
        cart_obj = Cart.objects.get_or_create_cart(cart_id)
    context = {
        'cart_obj': cart_obj,
    }
    return render(request, 'carts/cart.html', context)


def cart_update(request):
    # Issue: Duplication of carts of a logged in user and his previous
    # guest cart is only removed when he visits the '/carts/' explicitly
    # Solution: We need to redirect user to the cart whenever he wants to checkout
    product_id = request.POST.get('product_id', None)
    if product_id:
        cart_obj = Cart.objects.get_or_create_cart(request.session.get('cart_id', None))
        cart_obj.products.add(Product.objects.get(id=int(product_id)))
        request.session['cart_id'] = cart_obj.id
        cart_obj.save()
    else:
        raise Exception("Error while updating cart!")
    context = {
        'cart_products': cart_obj.products.all(),
    }
    print(context['cart_products'])
    print(cart_obj.id)
    return redirect('carts:cart')

def associate_user_with_cart(request, cart_id=None):
    # get the cart of the current user, guest or otherwise
    cart_obj = Cart.objects.get_or_create_cart(cart_id)
    # associate user with cart if user logs in after cart creation
    if request.user.is_authenticated() and cart_obj.user is None:
        # check if user already has a cart alloted in db
        user = request.user
        user_carts = user.cart_set.all()
        if user_carts.count() == 1 :
            # user already has a cart in db and the guest cart has atleast 1
            # product, copy the guest cart in the user cart
            if cart_obj.products.count() > 0:
                for product in cart_obj.products.all():
                    if product not in user_carts.first().products.all():
                        user_carts.first().products.add(product)
                user_carts.first().save()
            # delete the guest cart
            cart_obj.delete()
            cart_id = user_carts.first().id
        else:
            # user has no carts
            cart_obj.user = request.user
            cart_obj.save()
    else:
        # user is not authenticated, and the cart is guest
        pass
    # this is the user cart if he has been previously alloted a cart
    return cart_id