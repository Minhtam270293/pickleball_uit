from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_guides, name='get_all_guides'),
    path('create/', views.create_guide, name='create_guide'),
    path('<int:guide_id>/', views.get_guide_details, name='get_guide_details'),
    path('update/<int:guide_id>/', views.update_guide, name='update_guide'),
    path('delete/<int:guide_id>/', views.delete_guide, name='delete_guide'),
] 