from django.urls import path
from . import views as core_views

app_name = 'core'
urlpatterns = [
	path('home/', core_views.home, name='home-page'),
]