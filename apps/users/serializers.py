from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['role'] = user.role

        return token

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "password", "full_name", "email"]

    def create(self, validated_data):
        validated_data["hashed_password"] = make_password(validated_data["password"])
        validated_data.pop('password', None)
        return super().create(validated_data)


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "full_name", "email", "password_changed_at", "created_at"]  # Exclude 'password'


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UpdateUserSerializer(serializers.ModelSerializer):
    hashed_password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'hashed_password']
        extra_kwargs = {'username': {'read_only': True}}

    def update(self, instance, validated_data):
        if 'hashed_password' in validated_data:
            instance.hashed_password = make_password(validated_data['hashed_password'])
            instance.password_changed_at = timezone.now()
        return super().update(instance, validated_data)
