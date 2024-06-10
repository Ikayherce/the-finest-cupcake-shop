from django.shortcuts import render, get_object_or_404
from.cart import Cart
from shop.models import Product
from django.http import JsonResponse


def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities})


def cart_add(request):
    #get the cart
    cart = Cart(request)
    #test for POST
    if request.POST.get('action') == 'post':
        #Get products
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #look up product in database
        product = get_object_or_404(Product, id=product_id)
        #save to the session
        cart.add(product=product, quantity=product_qty)

        #get cart quantity
        cart_quantity = cart.__len__()

        #response = JsonResponse({'Product Name: ':product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    pass

def cart_update(request):
    pass