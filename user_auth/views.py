from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerialiser,MyTokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import generate_otp
from .tasks import send_registration_email
from .models import UserVerification

# Create your views here.
class UserRegisterView(APIView):
    def post(self,request):
        try:
            serializer = UserRegisterSerialiser(data=request.data)
            if serializer.is_valid():
                user=serializer.save()

                otp = generate_otp()
                subject = 'Email Verification OTP'
                message = f'Your otp for email verification is "{otp}", Thank you for choosing our service'
                send_registration_email.delay(user.email,subject,message)
                verification_details = UserVerification.objects.create(
                    user=user,
                    email = user.email,
                    otp=otp
                )
                verification_details.save()
                
                return Response(serializer.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

