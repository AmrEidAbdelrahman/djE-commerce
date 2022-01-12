from django.contrib import admin
from .models import Item, Order, OrderItem, Address, Payment, Coupon, Refund

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
	list_display = [
		'user',
		'ordered',
		'refund_requested',
		'refund_accepted'
	]
	search_fields = ['user__username']
	list_filter = ['ordered']


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)

