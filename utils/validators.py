# utils/validators.py (or wherever makes sense)
from rest_framework import serializers
import os

SUPPORTED_CURRENCIES = os.getenv("SUPPORTED_CURRENCIES", "USD")

def validate_currency(value):
    if value not in SUPPORTED_CURRENCIES:
        raise serializers.ValidationError(f"Unsupported currency: {value}")
    return value
