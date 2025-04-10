"""
Models for Account
"""

import os
import ast
from django.db import models
from apps.users.models import User


raw_value = os.getenv("SUPPORTED_CURRENCIES")
if raw_value:
    # Example: raw_value = "[('USD', 'USD'), ('EUR', 'EUR')]"
    SUPPORTED_CURRENCIES = ast.literal_eval(raw_value)
else:
    SUPPORTED_CURRENCIES = [("USD", "USD")]


class Account(models.Model):
    """
    Accounts Model to store current balance and specific currency for the account
    """

    id = models.BigAutoField(primary_key=True)
    # need to use column to force Django to use column name = "owner"
    owner = models.ForeignKey(
        User,
        to_field="username",
        db_column="owner",
        on_delete=models.CASCADE,
        related_name="accounts",
    )
    balance = models.BigIntegerField(default=0)
    currency = models.CharField(max_length=10, choices=SUPPORTED_CURRENCIES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("owner", "currency")

    def __str__(self):
        return f"{self.owner.username} - {self.currency}: {self.balance}"
