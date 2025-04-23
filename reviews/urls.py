from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_reviews, name='get_all_reviews'),
    path('create/', views.create_review, name='create_review'),
    path('<int:review_id>/', views.get_review_details, name='get_review_details'),
    path('update/<int:review_id>/', views.update_review, name='update_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
] 