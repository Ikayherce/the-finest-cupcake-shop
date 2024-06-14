from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0