from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import jwt
import logging

logger = logging.getLogger(__name__)


def get_jwt_payload(request):
    """
    Extracts and decodes the JWT token from the Authorization header.
    Returns: (payload, error_response) tuple
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, Response(
            {"detail": "Authorization header missing or malformed"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        logger.debug(f"JWT payload: {payload}")
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, Response(
            {"detail": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        return None, Response(
            {"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )
