from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Item


# Create your views here.

class HomeView(ListView):
	model = Item
	template_name = 'core/home-page.html'

class ProductDetailView(DetailView):
	model = Item
	template_name = 'core/product.html'

'''
def home(request):
	context = {
		'items': Item.objects.all(),
	}
	return render(request, 'core/home-page.html', context)
'''

def product(request):
	context = {
		'items': Item.objects.all(),
	}
	return render(request, 'core/home-page.html', context)