from django.urls import path
from .views import UserListAPIView, UserDetailAPIView

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailAPIView.as_view(), name='user-detail'),
    # Add login/register/logout here too
]