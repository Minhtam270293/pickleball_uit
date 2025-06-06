from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the UIT Pickleball site!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pickleball_platform_management.urls')),
    path('', home, name='home'),
]