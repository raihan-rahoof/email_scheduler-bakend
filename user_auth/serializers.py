from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re

class UserRegisterSerialiser(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=255,required=True)
    last_name = serializers.CharField(max_length=255,required=True)
    email = serializers.EmailField(max_length=255,required=True)
    
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']
        extra_kwargs = {'password':{'write_only':True}}
    
    def validate(self,data):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$'
        if not data['email'].strip():
            raise serializers.ValidationError({'email':('email is required')})
        elif User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email':('email already exists')})
        elif not re.match(pattern,data['password']):
            raise serializers.ValidationError({'password':('password must contain at least 8 characters, one uppercase, one lowercase, one number and one special character')})
        elif not data['first_name'].strip():
            raise serializers.ValidationError({'first_name':('first_name is required')})
        elif not data['last_name'].strip():
            raise serializers.ValidationError({'last_name':('last_name is required')})
        
        return data
    
    def create(self,validated_data):
        user = User(
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
    
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        username = attrs.get('username',None)
        password = attrs.get('password',None)

        if User.objects.filter(email=username).exists():
            username = User.objects.get(email=username).username

        attrs.update({'username':username})
        return super().validate(attrs)
