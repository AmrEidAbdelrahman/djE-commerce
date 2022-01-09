from django.contrib import admin
from .models import Item, Order, OrderItem, Address, Payment, Coupon, Refund

# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)

