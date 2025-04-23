from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_courts, name='get_all_courts'),
    path('create/', views.create_court, name='create_court'),
    path('<int:court_id>/', views.get_court_details, name='get_court_details'),
    path('update/<int:court_id>/', views.update_court, name='update_court'),
    path('delete/<int:court_id>/', views.delete_court, name='delete_court'),
] 