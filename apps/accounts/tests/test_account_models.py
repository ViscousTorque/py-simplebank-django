from django.test import TestCase
from django.db import IntegrityError
from apps.users.models import User
from apps.accounts.models import Account
from rest_framework.exceptions import ValidationError, ErrorDetail
from apps.accounts.serializers import AccountSerializer

class AccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser123',
            hashed_password='pw',
            full_name='Tester',
            email='test@example.com'
        )

    def test_account_creation(self):
        account = Account.objects.create(
            owner=self.user,
            balance=1000,
            currency="USD"
        )
        self.assertEqual(account.owner, self.user)
        self.assertEqual(account.balance, 1000)
        self.assertEqual(account.currency, "USD")
        self.assertIsNotNone(account.created_at)
        expected_str = f"{self.user.username} - USD: 1000"
        self.assertEqual(str(account), expected_str)

    def test_account_unique_together_constraint(self):
        Account.objects.create(owner=self.user, balance=500, currency="EUR")
        with self.assertRaises(IntegrityError):
            Account.objects.create(owner=self.user, balance=800, currency="EUR")

    def test_serializer_rejects_invalid_currency(self):
        data = {
            "currency": "JPY",
            "balance": 1000,
            "owner": self.user.username
        }
        serializer = AccountSerializer(data=data)
        
        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)

        self.assertEqual(
            ctx.exception.detail["currency"],
            [ErrorDetail(string='"JPY" is not a valid choice.', code='invalid_choice')]
        )
                                                                        
