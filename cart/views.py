from django.shortcuts import render, get_object_or_404
from.cart import Cart
from shop.models import Product
from django.http import JsonResponse


def cart_summary(request):
    return render(request, "cart_summary.html", {})

def cart_add(request):
    #get the cart
    cart = Cart(request)
    #test for POST
    if request.POST.get('action') == 'post':
        #Get products
        product_id = int(request.POST.get('product_id'))
        #look up product in database
        product = get_object_or_404(Product, id=product_id)
        #save to the session
        cart.add(product=product)

        response = JsonResponse({'Product Name: ':product.name})
        return response


def cart_delete(request):
    pass

def cart_update(request):
    pass