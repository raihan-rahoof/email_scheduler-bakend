from django.contrib import admin
from django.urls import path
from .views import UserRegisterView,MyTokenObtainPairView,OtpVerificationView,ResendOtpVIew
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='user_register'),
    path('verify-email/',OtpVerificationView.as_view(),name = 'verify-email'),
    path('resend-email/',ResendOtpVIew.as_view(),name = 'resend-email'),

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]