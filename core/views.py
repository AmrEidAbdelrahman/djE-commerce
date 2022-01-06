from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages

from .models import Item, OrderItem, Order


# Create your views here.

class HomeView(ListView):
	model = Item
	paginate_by = 1
	template_name = 'core/home-page.html'

class OrderSummaryView(View):
	def get(self, *args, **kwargs):
		order = get_object_or_404(Order, user=self.request.user, ordered=False)
		print(order)
		context = {
			'order': order,
		}
		return render(self.request, "core/order_summary.html", context)

class ProductDetailView(DetailView):
	model = Item
	template_name = 'core/product.html'


class CheckoutView(View):
	def get(self, *args, **kwargs):
		return render(self.request, 'core/checkout.html')


def add_to_cart(request, pk):
	item = get_object_or_404(Item, id=pk)
	order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item__id=pk).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, 'the item increased successfuly.')
		else:
			order.items.add(order_item)
			messages.info(request, 'the item Added successfuly.')
	else:
		order = Order.objects.create(user=request.user, ordered_date=timezone.now())
		order.items.add(order_item)
		messages.info(request, 'Start new Order and Add the item successfuly.')

	return redirect("core:product", pk=pk)


def remove_from_cart(request, pk):
	redirect_to = request.GET.get('redirect_to', 'core:product')
	item = get_object_or_404(Item, id=pk)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item__id=pk).exists():
			order_item = OrderItem.objects.get(item=item, user=request.user, ordered=False)
			order.items.remove(order_item)
			order_item.delete()
			# message says: the item removed successfuly
			messages.info(request, 'the item removed successfuly.')
			if redirect_to == "core:product":
				return redirect(redirect_to, pk=pk)
			else:
				return redirect(redirect_to)
		else:
			# message says: the item isn't in your cart
			messages.info(request, "the item isn't in your cart.")
			if redirect_to == "core:product":
				return redirect(redirect_to, pk=pk)
			else:
				return redirect(redirect_to)
	else:
		# return error message says: There are no active Order
		messages.info(request, 'There are no active Order.')
		if redirect_to == "core:product":
			return redirect(redirect_to, pk=pk)
		else:
			return redirect(redirect_to)