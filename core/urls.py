from django.urls import path
from . import views as core_views

app_name = 'core'
urlpatterns = [
	path('home/', core_views.HomeView.as_view(), name='home-page'),
	path('product/<pk>', core_views.ProductDetailView.as_view(), name="product"),
]