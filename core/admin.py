from django.contrib import admin
from .models import Item, Order, OrderItem, BillingAddress, Payment, Coupon

# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)
