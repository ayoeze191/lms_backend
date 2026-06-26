from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, ProfileView, SuperUserCreateView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('superuser/create/', SuperUserCreateView.as_view(), name='superuser_create'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
