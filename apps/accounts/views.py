from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.accounts.models import Account
from apps.accounts.serializers import AccountSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from apps.users.models import User
from utils.auth import get_jwt_payload
import logging
import jwt
import os

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")

class CreateAccountView(APIView):
    def post(self, request):
        payload, error_response = get_jwt_payload(request)
        if error_response:
            return error_response
        
        username_from_token = payload.get("username")

        if not username_from_token:
            return Response({'detail': 'Username not found in token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(username=username_from_token)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user, balance=0) # this bypasses the read_only serialiser stuff - crazy Django
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAccountView(APIView):
    def get(self, request, id):
        payload, error_response = get_jwt_payload(request)
        if error_response:
            return error_response
        
        username_from_token = payload.get("username")

        if not username_from_token:
            return Response({'detail': 'Username not found in token'}, status=status.HTTP_401_UNAUTHORIZED)

        if not username_from_token:
            return Response({'detail': 'Username not found in token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(username=username_from_token)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Now retrieve the account owned by this user
        try:
            account = Account.objects.get(id=id, owner=user)
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class ListAccountsView(APIView, PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get(self, request):
        payload, error_response = get_jwt_payload(request)
        if error_response:
            return error_response
        
        username_from_token = payload.get("username")

        if not username_from_token:
            return Response({'detail': 'Username not found in token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(username=username_from_token)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        accounts = Account.objects.filter(owner=user)
        result_page = self.paginate_queryset(accounts, request, view=self)
        serializer = AccountSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)
    

def error_response(message):
    return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)