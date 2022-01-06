from django import template

from core.models import Order


register = template.Library()

@register.filter
def number_of_items_in_cart(user):
	if user.is_authenticated:
		qs = Order.objects.filter(user=user, ordered=False)
		if qs.exists():
			return qs[0].items.count()
	return int(0)