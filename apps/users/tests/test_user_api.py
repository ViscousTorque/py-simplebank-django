from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.hashers import make_password
from apps.users.models import User
from rest_framework_simplejwt.tokens import AccessToken

class LoginUserAPITest(APITestCase):

    def setUp(self):
        self.login_url = reverse('login-user')
        self.username = "testuser"
        self.password = "securepass123"
        self.user = User.objects.create(
            username=self.username,
            email="test@example.com",
            hashed_password=make_password(self.password),
            role="depositor",
            full_name="Test User"
        )

    def test_successful_login(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.login_url, data, format="json")    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertEqual(response.data["user"]["username"], self.username)

    def test_invalid_password(self):
        data = {
            "username": self.username,
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_user_does_not_exist(self):
        data = {
            "username": "nonexistent",
            "password": "whatever"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

# Todo : fix this test, I used the wrong token :-)
# class UpdateUserAPITest(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create(
#             username="updateuser",
#             hashed_password=make_password("pass123"),
#             role="depositor",
#             full_name="Old Name",
#             email="update@example.com"
#         )
#         self.token = str(AccessToken.for_user(self.user))
#         self.url = reverse("update-user")

#     def test_update_own_full_name(self):
#         new_name = "Updated Name"
#         headers = {
#             "HTTP_AUTHORIZATION": f"Bearer {self.token}"
#         }
#         data = {
#             "username": self.user.username,
#             "full_name": new_name
#         }

#         response = self.client.patch(self.url, data, format="json", **headers)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.full_name, new_name)
