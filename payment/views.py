import logging
import datetime
import stripe
import json 
from cart.cart import Cart
from django.shortcuts import render, redirect, get_object_or_404
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from shop.models import Product, Profile


def order_confirmation(request):
    if request.user.is_authenticated:
        # Retrieve the last order of the user
        last_order = Order.objects.filter(user=request.user).order_by('-id').first()
    else:
        # Retrieve the last order placed in the session for not logged-in users
        order_id = request.session.get('last_order_id')
        if order_id:
            last_order = Order.objects.filter(id=order_id).first()
        else:
            last_order = None

    # If there is no order found, redirect to home or an appropriate page
    if not last_order:
        messages.error(request, "No order found.")
        return redirect('home')

    # Get the order items for the last order
    order_items = OrderItem.objects.filter(order=last_order)

    # Prepare the context
    context = {
        'order': last_order,
        'order_items': order_items,
    }

    return render(request, 'payment/order_confirmation.html', context)

def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
            # Get the order ID
            order_id = create_order.pk
            
            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                price = product.price

                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart field)
            current_user.update(old_cart="")

            # Store the order ID in the session for not logged-in users
            request.session['last_order_id'] = order_id

            messages.success(request, "Order Placed!")
            return redirect('order_confirmation')

            
        else:
            # not logged in
            # Create Order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
            
            # Get the order ID
            order_id = create_order.pk
            
            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                price = product.price

                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            # Store the order ID in the session for not logged-in users
            request.session['last_order_id'] = order_id

            messages.success(request, "Order Placed!")
            return redirect('order_confirmation')

    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def billing_info(request):
    logging.basicConfig(level=logging.INFO)

    # Directly set the Stripe API key using the secret key stored in your settings
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY  # This line is kept for clarity, even though it's not used

    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Validate and sanitize POST data before using it
        my_shipping = request.POST.copy()  # Make a mutable copy to modify safely
        # Perform validation/sanitization here
        request.session['my_shipping'] = my_shipping

        # Calculate total amount based on cart totals
        total_amount = round(totals * 100)  # Correctly convert to cents and round
        
        try:
            # Serialize the my_shipping dictionary into a JSON string
            my_shipping_json = json.dumps(my_shipping)

            # Create a PaymentIntent with the calculated total amount
            payment_intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency='usd',  # Use the appropriate currency code
                metadata={'shipping': my_shipping_json},  # Correctly use the serialized JSON string
            )

            # Log successful payment intent creation
            logging.info(f"PaymentIntent created successfully with ID: {payment_intent.id}")
            
            # Generate client secret for the PaymentIntent
            client_secret = payment_intent.client_secret

            context = {
                'cart_products': cart_products,
                'quantities': quantities,
                'totals': totals,
                'shipping_info': my_shipping,
                'stripe_public_key': stripe_public_key,
                'client_secret': client_secret,  # Pass the client secret to the template
            }

            if request.user.is_authenticated:
                billing_form = PaymentForm()
                context['billing_form'] = billing_form
                return render(request, "payment/billing_info.html", context)
            else:
                messages.error(request, "Please log in to proceed.")
                return redirect('login')  # Redirect to login page if not authenticated
        except Exception as e:
            # Log the exception
            logging.error(f"Failed to create payment intent: {str(e)}")
            messages.error(request, f"Failed to create payment intent: {str(e)}")
            return redirect('home')
    else:
        messages.error(request, "Access Denied")
        return redirect('home')

#def billing_info(request):
    # Directly set the Stripe API key using the secret key stored in your settings
#    stripe.api_key = settings.STRIPE_SECRET_KEY
    
#    stripe_public_key = settings.STRIPE_PUBLIC_KEY
#    stripe_secret_key = settings.STRIPE_SECRET_KEY  # This line is kept for clarity, even though it's not used

#    if request.method == 'POST':
#        cart = Cart(request)
#        cart_products = cart.get_prods()
#        quantities = cart.get_quants()
#        totals = cart.cart_total()

        # Validate and sanitize POST data before using it
#        my_shipping = request.POST.copy()  # Make a mutable copy to modify safely
        # Perform validation/sanitization here
#        request.session['my_shipping'] = my_shipping

        # Calculate total amount based on cart totals
#        total_amount = round(totals * 100)  # Correctly convert to cents and round
        
#        try:
            # Serialize the my_shipping dictionary into a JSON string
#            my_shipping_json = json.dumps(my_shipping)

            # Create a PaymentIntent with the calculated total amount
#            payment_intent = stripe.PaymentIntent.create(
#                amount=total_amount,
#                currency='usd',  # Use the appropriate currency code
#                metadata={'shipping': my_shipping_json},  # Correctly use the serialized JSON string
#            )

            # Generate client secret for the PaymentIntent
#            client_secret = payment_intent.client_secret

#            context = {
#                'cart_products': cart_products,
#                'quantities': quantities,
#                'totals': totals,
#                'shipping_info': my_shipping,
#                'stripe_public_key': stripe_public_key,
#               'client_secret': client_secret,  # Pass the client secret to the template
#            }

#            if request.user.is_authenticated:
#                billing_form = PaymentForm()
#                context['billing_form'] = billing_form
#                return render(request, "payment/billing_info.html", context)
#            else:
#                messages.error(request, "Please log in to proceed.")
#                return redirect('login')  # Redirect to login page if not authenticated
#        except Exception as e:
#            messages.error(request, f"Failed to create payment intent: {str(e)}")
#            return redirect('home')
#    else:
#        messages.error(request, "Access Denied")
#        return redirect('home')



def checkout(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()

	if request.user.is_authenticated:
		# Checkout as logged in user
		# Shipping User
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		# Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
	else:
		# Checkout as guest
		shipping_form = ShippingForm(request.POST or None)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
	


def payment_success(request):
	return render(request, "payment/payment_success.html", {})
