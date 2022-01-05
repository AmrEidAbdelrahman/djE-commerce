from django.db import models

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
	price = models.IntegerField(default=18)

	category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
	label = models.CharField(choices=LABELCHOICES, max_length=1)

	def __str__(self):
		return f'{self.title}'

class OrderItem(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f'{self.quantity} of {self.item.title}'


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user.username} on {self.start_date}'

