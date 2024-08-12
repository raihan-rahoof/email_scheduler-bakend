from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerialiser,MyTokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import generate_otp
from .tasks import send_registration_email


# Create your views here.
class UserRegisterView(APIView):
    def post(self,request):
        serializer = UserRegisterSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()

            otp = generate_otp()
            subject = 'Email Verification OTP'
            message = f'Your otp for email verification is "{otp}", Thank you for choosing our service'
            send_registration_email.delay(serializer.data['email'],subject,message)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer