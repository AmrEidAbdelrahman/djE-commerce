from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages

from .forms import CheckoutForm
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon

import stripe

# This is your test secret API key.
stripe.api_key = 'sk_test_51KFRKhA4DXRyfULlrSdK7tXMBkowVabtTbmUJtNYwOjLdtFv8LKxBAxKLvWoFjayqlAXcZoFlHi5fulb1A1D8NKa00B6y8odr9'


# Create your views here.

class HomeView(ListView):
	model = Item
	paginate_by = 1
	template_name = 'core/home-page.html'

class OrderSummaryView(View):
	def get(self, *args, **kwargs):
		try:
			order = get_object_or_404(Order, user=self.request.user, ordered=False)
		except:
			order = Order(user=self.request.user, ordered=False, ordered_date=timezone.now())
			order.save()
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
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			form = CheckoutForm()
			context = {
				'form': form,
				'order':order
			}
			return render(self.request, 'core/checkout.html', context)
		except:
			# TODO: redirect with error message
			messages.info(self.request, "WHAT IS WRONG ?")
			return render(self.request, 'core/checkout.html', context)
	def post(self, *args, **kwargs):
		form = CheckoutForm(self.request.POST or None)
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			print("$$$$$$",order)
			if form.is_valid():
				print(form.cleaned_data)
				print("#####THIS FORM IS VALID#####")
				user = self.request.user
				street_address = self.request.POST.get('street_address')
				apartment_address = self.request.POST.get('apartment_address')
				country = self.request.POST.get('country')
				zip = self.request.POST.get('zip')
				billing_address = BillingAddress(
						user = user,
						street_address=street_address,
						apartment_address=apartment_address,
						country=country,
						zip=zip
					)
				billing_address.save()
				order.billing_address = billing_address
				order.save()
				payment_option = self.request.POST.get("payment_option")
				'''will be included when paypal works
				if payment_option == "S":
					return redirect('core:payment' , payment_option="Stripe")
				elif payment_option == "P":
					return redirect('core:payment' , payment_option="Paypal")
				else:
					messages.info(self.request, "SELECT A CORRECT PAYMENT-OPTION...")
					return redirect('core:checkout')
				'''
				YOUR_DOMAIN = "http://127.0.0.1:8000/"
				try:
					checkout_session = stripe.checkout.Session.create(
					    line_items=[
							{
								# Provide the exact Price ID (for example, pr_1234) of the product you want to sell
								'price_data': {
									'currency':'usd',
									'product_data': {
										'name':'test100',
										'description':'test100 description'
									},
									'unit_amount':5000
								},
								'quantity': 1,
							},
						],
						mode='payment',
						success_url=YOUR_DOMAIN + 'success/',
						cancel_url=YOUR_DOMAIN + 'cancel/',
					)

					# TODO: edite the total amount in payment
					payment = Payment()
					payment.stripe_charge_id = checkout_session.id
					payment.user = self.request.user
					payment.amount = 10.5
					payment.save()

					# adding the payment into the order and set the order state to ordered
					order.ordered = True
					order.payment = payment
					order.save()

					# setting the order_items state to ordered
					order_items = order.items.all()
					order_items.bulk_update(ordered=True)


				except Exception as e:
					print(e)

				return redirect(checkout_session.url, code=303)
				print("##################################")
		except Exception as e:
			print(e)
			messages.info(self.request, "THERE IS NO ACTIVE ORDER")
			return redirect("core:order-summary")

		messages.info(self.request, "THERE IS A PROBLEM....")
		return redirect('core:checkout')

'''
class PaymentView(View):
	def get(self, *args, **kwagrs):
		return render(self.request, "core/stripe_checkout.html")

	def post(self, *args, **kwargs):
		print("#########")
		YOUR_DOMAIN = "http://127.0.0.1:8000/"
		try:
			checkout_session = stripe.checkout.Session.create(
			    line_items=[
					{
						# Provide the exact Price ID (for example, pr_1234) of the product you want to sell
						'price': 'price_1KFSTjA4DXRyfULlCr276pnu',
						'quantity': 1,
					},
				],
				mode='payment',
				success_url=YOUR_DOMAIN + '/success/',
				cancel_url=YOUR_DOMAIN + '/cancel/',
			)
		except Exception as e:
			print(e)

		return redirect(checkout_session.url, code=303)
'''

def add_coupon(request):
	try:
		order = Order.objects.get(user=request.user, ordered=False)
		coupon_entered = request.POST.get('coupon')
		print(coupon_entered)
		coupon = Coupon.objects.get(coupon=coupon_entered)
		order.coupon = coupon
		order.save()
		return redirect("core:checkout")
	except Exception as e:
		print(e)
		messages.info(request, "INVALID")
		return redirect("core:checkout")

def remove_coupon(request):
	order = Order.objects.get(user=request.user, ordered=False)
	order.coupon = None
	order.save()
	return redirect("core:checkout")


def add_to_cart(request, pk):
	redirect_to = request.GET.get('redirect_to', 'core:product')
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

	if redirect_to == "core:product":
		return redirect(redirect_to, pk=pk)
	else:
		return redirect(redirect_to)


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


def decrease_single_item_from_cart(request, pk):
	item = get_object_or_404(Item, id=pk)
	order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item__id=pk).exists():
			if order_item.quantity > 1: 
				order_item.quantity -= 1
				order_item.save()
			else:
				order.items.remove(order_item)
				order_item.delete()
			messages.info(request, 'the item decreased successfuly.')
		else:
			messages.info(request, 'this item isnot in your cart righ now !')
	else:
		messages.info(request, 'Sorry, No active order')

	return redirect("core:order-summary")