from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from .validators import validate_unique_email



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(email = email, password = password)
            if not user:
                raise serializers.ValidationError("Incorrect email or password")
        else:
            raise serializers.ValidationError("Both email and password are required")

        return data

class UserSignupSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(validators=[validate_unique_email])
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password' : {'write_only':True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
# class UserSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'password']
    #     extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user
    
class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'