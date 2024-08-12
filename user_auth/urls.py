from django.contrib import admin
from django.urls import path
from .views import UserRegisterView,MyTokenObtainPairView,OtpVerificationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='user_register'),
    path('verify-email/',OtpVerificationView.as_view(),name = 'verify-email'),

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]