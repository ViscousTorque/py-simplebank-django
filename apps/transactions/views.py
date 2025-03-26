from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from apps.accounts.models import Account
from apps.transactions.models import Transfer
from apps.users.models import User
from apps.transactions.serializers import TransferSerializer
import logging
import jwt
import os

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")

# TODO: Fix this, refactor it
class CreateTransferView(APIView):
    def post(self, request):
        # JWT auth header check
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'detail': 'Authorization header missing or malformed'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get('username')
            logger.info(f"JWT payload: {payload}")
        except jwt.ExpiredSignatureError:
            return Response({'detail': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        if not username:
            return Response({'detail': 'Username not found in token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Proceed with transfer logic
        serializer = TransferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        from_account = serializer.validated_data['from_account_id']
        logging.info(f"{from_account=}")
        to_account = serializer.validated_data['to_account_id']
        amount = serializer.validated_data['amount']
        currency = serializer.validated_data['currency']

        try:
            from_account_obj = Account.objects.get(id=from_account.id)
            to_account_obj = Account.objects.get(id=to_account.id)
        except ObjectDoesNotExist:
            return Response({"error": "One or both accounts do not exist"}, status=status.HTTP_404_NOT_FOUND)

        if from_account.currency != currency or to_account.currency != currency:
            return Response({"error": "Currency mismatch between accounts"}, status=status.HTTP_400_BAD_REQUEST)

        if from_account_obj.owner != user:
            return Response({"error": "Unauthorized to transfer from this account"}, status=status.HTTP_401_UNAUTHORIZED)

        transfer = Transfer.objects.create(
            from_account_id=from_account_obj,
            to_account_id=to_account_obj,
            amount=amount
        )

        return Response(TransferSerializer(transfer).data, status=status.HTTP_201_CREATED)
