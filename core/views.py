from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages

from .forms import CheckoutForm, RefundForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund

import string
import random
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
			try:
				default_shipping = Address.objects.filter(user=self.request.user, default=True, address_type='S')[0]
				context.update({'shipping_address':default_shipping})
			except:
				pass
			try:
				default_billing = Address.objects.filter(user=self.request.user, default=True, address_type='B')[0]
				context.update({'billing_address':default_billing})
			except:
				pass
			print(context)
			return render(self.request, 'core/checkout.html', context)
		except Exception as e:
			print(e)
			# TODO: redirect with error message
			messages.info(self.request, "NO ACTIVE ORDERs")
			return redirect("core:home-page")
	def post(self, *args, **kwargs):

		shipping_as_billing = self.request.POST.get('shipping_as_billing')
		set_default_billing = self.request.POST.get('set_default_billing')
		use_default_billing = self.request.POST.get('use_default_billing')

		set_default_shipping = self.request.POST.get('set_default_shipping')
		use_default_shipping = self.request.POST.get('use_default_shipping')

		form = CheckoutForm(self.request.POST or None)
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			if form.is_valid():
				print(form.cleaned_data)
				print("#####THIS FORM IS VALID#####")
				user = self.request.user

				if use_default_billing:
					try:
						billing_address = Address.objects.get(user=user, default=True, address_type="B")
					except:
						messages.error(self.request, "you have no default billing address")
						return redirect('core:checkout')
				else:
					billing_address1 = self.request.POST.get('billing_address1')
					billing_address2 = self.request.POST.get('billing_address2')
					billing_country = self.request.POST.get('billing_country')
					billing_zip = self.request.POST.get('billing_zip')
					billing_address = Address(
							user = user,
							street_address=billing_address1,
							apartment_address=billing_address2,
							country=billing_country,
							zip=billing_zip,
							address_type="B"
						)
					if set_default_billing:
						billing_address.default = True
					billing_address.save()
					if shipping_as_billing:
						shipping_address = billing_address
						shipping_address.id = None
						shipping_address.address_type = "S"
						shipping_address.save()

				if not shipping_as_billing:
					if use_default_shipping:
						try:
							shipping_address = Address.objects.get(user=user, default=True, address_type="B")
						except:
							messages.error(self.request, "you have no default shipping address")
							return redirect('core:checkout')
					else:
						shipping_address1 = self.request.POST.get('shipping_address1')
						shipping_address2 = self.request.POST.get('shipping_address2')
						shipping_country = self.request.POST.get('shipping_country')
						shipping_zip = self.request.POST.get('shipping_zip')
						shipping_address = Address(
								user = user,
								street_address=shipping_address1,
								apartment_address=shipping_address2,
								country=shipping_country,
								zip=shipping_zip,
								address_type="S"
							)
						if set_default_shipping:
							shipping_address.default = True
						shipping_address.save()


				order.billing_address = billing_address
				order.shipping_address = shipping_address
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
					# TODO: handle the stripe webhook
					# order.ordered = True
					# order.ref_code = random.randint(???)
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


class RefundView(View):
	def get(self, *args, **kwargs):
		form = RefundForm()
		context = {
			'form': form
		}
		return render(self.request, "core/refund_request.html", context)

	def post(self, *args, **kwargs):
		ref_code = self.request.POST.get("ref_code")
		description = self.request.POST.get("description")
		try:
			order = Order.objects.get(user=self.request.user, ref_code=ref_code , ordered=True)
			order.refund_requested = True
			order.save()
			refund = Refund(order_ref_code=ref_code, description=description)
			refund.save()
			messages.success(self.request, f"your request have submited successfully")
			return redirect('core:request-refund')
		except:
			messages.error(self.request, f"You have no order with this ref_code {ref_code}")
			return redirect('core:request-refund')

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