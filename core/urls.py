from django.urls import path
from . import views as core_views

app_name = 'core'
urlpatterns = [
	path('home/', core_views.HomeView.as_view(), name='home-page'),
	path('product/<pk>/', core_views.ProductDetailView.as_view(), name="product"),
	path('add-to-cart/<pk>/', core_views.add_to_cart, name="add-to-cart"),
	path('remove-from-cart/<pk>/', core_views.remove_from_cart, name="remove-from-cart"),

]