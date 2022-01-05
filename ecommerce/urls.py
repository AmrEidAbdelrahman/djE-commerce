from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls' , namespace='core')),

    path('accounts/', include('allauth.urls')),
    


    path('admin/', admin.site.urls),
]
