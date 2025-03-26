
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from .serializers import CreateUserSerializer, UserResponseSerializer, LoginUserSerializer, UpdateUserSerializer
from apps.users.models import VerifyEmail
from datetime import timedelta, datetime, timezone
from django.utils.timezone import make_aware
from .models import User
from apps.authentication.models import Session
from utils.auth import get_jwt_payload
import logging
import os

logger = logging.getLogger(__name__)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")


class CreateUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_serializer = UserResponseSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
    
    def post(self, request):

        headers = {k: v for k, v in request.META.items() if k.startswith("HTTP_")}
        logger.info("Request Headers:\n" + "\n".join([f"{k}: {v}" for k, v in headers.items()]))

        serializer = LoginUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        # TODO: Manually querying custom User model to find and auth the user by username
        # read up on Django's authenticate()
        logger.info(f"Attempting to authenticate user: {username}")
        try:
            user = User.objects.get(username=username)
            logger.info(f"{user=}")
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.hashed_password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user:
            logger.info("Authentication failed")
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username
        refresh['role'] = user.role
        refresh_exp = datetime.fromtimestamp(refresh['exp'], tz=timezone.utc)
        
        access = AccessToken.for_user(user)
        access['username'] = user.username
        access['role'] = user.role
        access_exp = datetime.fromtimestamp(access['exp'], tz=timezone.utc)

        logger.info(f"{refresh=}")
        logger.info(f"{access=}")

        try:
            session = Session.objects.create(
                id=refresh['jti'],
                username=user,
                refresh_token=str(refresh),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                client_ip=self.get_client_ip(request),
                is_blocked=False,
                expires_at = refresh_exp 
            )
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            return Response({"error": "Session creation failed"}, status=500)

        try:
            serialized_user = UserResponseSerializer(user).data
        except Exception as e:
            logger.error(f"Error serializing user: {e}")
            return Response({"error": "Failed to serialize user"}, status=500)
         
        response_data = {
            "session_id": str(session.id),
            "access_token": str(access),
            "access_token_expires_at": access_exp.isoformat(),
            "refresh_token": str(refresh),
            "refresh_token_expires_at": refresh_exp.isoformat(),
            "user": {
                "username": serialized_user["username"],
                "full_name": serialized_user["full_name"],
                "email": serialized_user["email"],
                "password_changed_at": serialized_user["password_changed_at"],
                "created_at": serialized_user["created_at"],
            }
        }

        logger.info(f"{response_data=}")
        
        return Response(response_data, status=status.HTTP_200_OK)



class UpdateUserView(APIView):
    def patch(self, request):
        payload, error_response = get_jwt_payload(request)
        if error_response:
            return error_response

        username_from_token = payload.get("username")
        role_from_token = payload.get("role")
        user_id_from_token = payload.get("user_id")

        username = request.data.get("username")
        if not username:
            return Response({"error": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST)

        if username_from_token != username and role_from_token != 'banker':
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        try:
            auth_user = User.objects.get(id=user_id_from_token)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        username = request.data.get("username")

        if not username:
            return Response({"error": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST)

        if auth_user.username != username and auth_user.role != 'banker':
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateUserSerializer(target_user, data=request.data, partial=True)
        if serializer.is_valid():
            if "password" in serializer.validated_data:
                serializer.validated_data["hashed_password"] = make_password(serializer.validated_data["password"])
                serializer.validated_data["password_changed_at"] = timezone.now()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO: fix!
# class VerifyEmailView(APIView):
#     def post(self, request):
#         email_id = request.data.get("email_id")
#         secret_code = request.data.get("secret_code")
        
#         if not email_id or not secret_code:
#             return Response({"error": "Email ID and secret code are required"}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             verify_email = VerifyEmail.objects.get(email=email_id, secret_code=secret_code, is_used=False)
#         except ObjectDoesNotExist:
#             return Response({"error": "Invalid email verification request"}, status=status.HTTP_400_BAD_REQUEST)
        
#         verify_email.is_used = True
#         verify_email.save()
        
#         user = User.objects.get(email=email_id)
#         user.is_verified = True
#         user.save()
        
#         return Response({"is_verified": user.is_verified}, status=status.HTTP_200_OK)
    
# TODO: fix!!
# class RenewAccessTokenView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         refresh_token = request.data.get("refresh_token")
#         if not refresh_token:
#             return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             refresh = RefreshToken(refresh_token)
#             user = User.objects.get(id=refresh.payload['user_id'])
            
#             access_token = AccessToken.for_user(user)
#             access_token.set_exp(lifetime=timedelta(minutes=15))

#             return Response({
#                 "access_token": str(access_token),
#                 "access_token_expires_at": access_token['exp'],
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
