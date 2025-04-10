import logging
import os

from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from apps.accounts.models import Account
from apps.accounts.serializers import AccountSerializer
from apps.users.models import User
from utils.auth import get_jwt_payload

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")


class CreateAccountView(APIView):
    """
    Because I am using a custom using a custom APIView, drf-spectacular doesn’t know what
    serializer to document unless you explicitly tell it. So I need to use serializer_class ..
    TODO: standardise the classes?
    """

    serializer_class = AccountSerializer

    @extend_schema(
        request=AccountSerializer,
        responses={201: AccountSerializer, 400: None, 401: None, 404: None},
        summary="Create a new account",
        description="Creates an account for the authenticated "
        "user. The user is extracted from the JWT token.",
    )
    def post(self, request):
        payload, error_response = get_jwt_payload(request)
        if error_response:
            return error_response

        username_from_token = payload.get("username")

        if not username_from_token:
            return Response(
                {"detail": "Username not found in token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            user = User.objects.get(username=username_from_token)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            # this bypasses the read_only serialiser stuff - crazy Djang
            serializer.save(owner=user, balance=0)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAccountView(APIView):
    serializer_class = AccountSerializer

    @extend_schema(
        responses={200: AccountSerializer, 401: None, 404: None, 500: None},
        summary="Retrieve account by ID",
        description="Returns a specific account if it belongs to the authenticated user.",
    )
    def get(self, request, id):
        payload, error_response = get_jwt_payload(request)
        if error_response:
            return error_response

        username_from_token = payload.get("username")

        if not username_from_token:
            return Response(
                {"detail": "Username not found in token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not username_from_token:
            return Response(
                {"detail": "Username not found in token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            user = User.objects.get(username=username_from_token)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Now retrieve the account owned by this user
        try:
            account = Account.objects.get(id=id, owner=user)
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListAccountsView(APIView, PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10
    serializer_class = AccountSerializer

    @extend_schema(
        summary="List user's accounts",
        description="Returns a paginated list of accounts belonging to the authenticated user.",
        parameters=[
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Page number",
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Number of results per page",
            ),
        ],
        responses={200: AccountSerializer(many=True)},
    )
    def get(self, request):
        payload, error_response = get_jwt_payload(request)
        if error_response:
            return error_response

        username_from_token = payload.get("username")

        if not username_from_token:
            return Response(
                {"detail": "Username not found in token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            user = User.objects.get(username=username_from_token)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        accounts = Account.objects.filter(owner=user)
        result_page = self.paginate_queryset(accounts, request, view=self)
        serializer = AccountSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


def error_response(message):
    return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
