from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_users, name='get_all_users'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('<int:user_id>/', views.user_profile, name='user_profile'),
] 