from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerialiser,MyTokenObtainPairSerializer,VerifyOtpSerializer,ResendOTPSerializer
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

class OtpVerificationView(APIView):
    def post(self,request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            try:
                user_verification = UserVerification.objects.get(email=email,otp=otp)
                if user_verification.is_expired():
                    user_verification.delete()
                    return Response({'error': 'OTP has expired.Try with New Otp'}, status=status.HTTP_400_BAD_REQUEST)
                user = user_verification.user
                user.is_active = True
                user.save()
                user_verification.delete()
                return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
            except UserVerification.DoesNotExist:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


                
class ResendOtpVIew(APIView):
    serializer = ResendOTPSerializer
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data['email']

        try:
            user_verification,created = UserVerification.objects.get_or_create(email=email)
            new_otp = generate_otp()
            subject = 'Email Verification OTP'
            message = f'Your new OTP for email verification is "{new_otp}", Thank you for choosing our service'

            if not created:
                user_verification.otp = new_otp
                user_verification.save()
            else:
                created.user = request.user
                created.otp = new_otp
                created.save()

            send_registration_email.delay(email,subject,message)
            return Response({'message': 'New OTP sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

