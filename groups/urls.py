from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_groups, name='get_all_groups'),
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/', views.get_group_details, name='get_group_details'),
    path('update/<int:group_id>/', views.update_group, name='update_group'),
    path('delete/<int:group_id>/', views.delete_group, name='delete_group'),
    path('<int:group_id>/members/add/', views.add_member, name='add_member'),
    path('<int:group_id>/members/remove/<int:user_id>/', views.remove_member, name='remove_member'),
] 