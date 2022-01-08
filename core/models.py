from django.db import models

from django.urls import reverse
from django_countries.fields import CountryField

from django.contrib.auth.models import User
# Create your models here.


CATEGORY_CHOICES = (
	("S","Shirt"),
	("SW","Sport Wear"),
	("OW","OutWear")
)

LABELCHOICES = (
	("P","primary"),
	("D","danger"),
	("S","secondary")
)

class Item(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	price = models.IntegerField(default=120)
	price_after_disc = models.IntegerField(null=True, blank=True)
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
	label = models.CharField(choices=LABELCHOICES, max_length=1)
	

	def __str__(self):
		return f'{self.title}'

	def get_absolute_url(self):
		return reverse("core:product" , kwargs={'pk': self.id})

	def get_add_to_cart_url(self):
		return reverse("core:add-to-cart" , kwargs={'pk': self.id})

	def get_remove_from_cart_url(self):
		return reverse("core:remove-from-cart" , kwargs={'pk': self.id})




class OrderItem(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	ordered = models.BooleanField(default=False)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f'{self.quantity} of {self.item.title}'

	def get_total_price(self):
		return self.item.price * self.quantity

	def get_total_price_after_disc(self):
		return self.quantity * self.item.price_after_disc

	def get_total_disc(self):
		return int(self.get_total_price - self.get_total_price_after_disc)


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)
	billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, null=True, blank=True)
	payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return f'{self.user.username} on {self.start_date}'


	def get_order_total_price(self):
		sum = 0
		for order_item in self.items.all():
			if order_item.item.price_after_disc:
				sum += order_item.get_total_price_after_disc()
			else:
				sum += order_item.get_total_price()

		return sum


class BillingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	street_address = models.CharField(max_length=100)
	apartment_address = models.CharField(max_length=100)
	country = CountryField(multiple=False)
	zip = models.CharField(max_length=10)


	def __str__(self):
		return f'{self.user.username}'


class Payment(models.Model):
	stripe_charge_id = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user.username}'