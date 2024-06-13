from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.http import Http404
from django.db.models import Q
import json
from cart.cart import Cart



def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
    

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User profile has been updated")
            return redirect('home')
        return render (request,"update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You must be logged in to access the page")
        return redirect ('home')


def category(request,cat):
    #Replace hyphens with spaces
    cat = cat.replace('-',' ')
    #Take the category from url
    try:
    #Look up the category
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products,'category':category})

    except Category.DoesNotExist:
        raise Http404("That category does not exist")

    #except:
    #    messages.success(request, ("That category doesn't exist"))
    #    return redirect('home')


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request,'home.html', {'products':products})

def about(request):
    return render(request,'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)

            #shopping cart persistence
            current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
            saved_cart = current_user.old_cart
			# Convert database string to python dictionary
            if saved_cart:
				# Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
                cart = Cart(request)
				# Loop through the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ("You have been logged in"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again"))
            return redirect('login') 
    else: 
        return render(request,'login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("Username created. Please fill out your details"))
            return redirect('update_info')
        else: 
            messages.success(request,("Oops,there was a problem registering, please try again"))
            return redirect('register')

    else:
        return render(request,'register.html',{'form':form})
