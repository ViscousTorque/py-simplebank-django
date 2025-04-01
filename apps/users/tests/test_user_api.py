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

class CreateUserViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('create-user')

    def test_create_user_success(self):
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "full_name": "testuser",
            "password": "strongpassword123"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], payload["username"])
        self.assertEqual(response.data["email"], payload["email"])
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_create_user_invalid_data(self):
        payload = {
            "username": "",  # Invalid: required field
            "email": "not-an-email",  # Invalid email
            "password": "123"  # Too short or doesn't meet validation
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)


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
