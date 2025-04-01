from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from apps.users.models import User, VerifyEmail
from datetime import timedelta
from faker import Faker

faker = Faker()

class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create(
            username=faker.user_name(),
            role='depositor',
            hashed_password=faker.sha256(),
            full_name=faker.name(),
            email=faker.unique.email()
        )

        self.assertEqual(user.role, 'depositor')
        self.assertFalse(user.is_verified)
        self.assertIsNotNone(user.created_at)

    def test_str_method(self):
        user = User.objects.create(
            username='testuser123',
            hashed_password='pw',
            full_name='Tester',
            email='test@example.com'
        )
        self.assertEqual(str(user), 'testuser123')

    def test_unique_username(self):
        username = faker.user_name()
        User.objects.create(
            username=username,
            hashed_password='pw1',
            full_name='User One',
            email=faker.unique.email()
        )
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username=username,
                hashed_password='pw2',
                full_name='User Two',
                email=faker.unique.email()
            )

class VerifyEmailModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            role="depositor",
            hashed_password="dummyhash",
            full_name="Test User",
            email="test@example.com"
        )

    def test_create_verify_email(self):
        expired_at = timezone.now() + timedelta(days=1)
        ve = VerifyEmail.objects.create(
            username=self.user,
            email="verify@example.com",
            secret_code="123456",
            expired_at=expired_at
        )

        self.assertEqual(ve.email, "verify@example.com")
        self.assertFalse(ve.is_used)
        self.assertEqual(ve.username, self.user)
        self.assertEqual(ve.secret_code, "123456")
        self.assertIsNotNone(ve.created_at)
        self.assertEqual(ve.expired_at, expired_at)

    def test_str_method(self):
        expired_at = timezone.now() + timedelta(days=1)
        ve = VerifyEmail.objects.create(
            username=self.user,
            email="verify@example.com",
            secret_code="123456",
            expired_at=expired_at
        )

        expected_str = f"Verify verify@example.com - Used: False"
        self.assertEqual(str(ve), expected_str)

