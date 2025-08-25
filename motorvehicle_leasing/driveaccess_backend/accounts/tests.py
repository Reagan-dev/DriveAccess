from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

# Create your tests here.
class UserModelTest(APITestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="normal45@gmail.com",
            name="normal User",
            password="987normal",
            phone_number="0768976324"
        )
        self.assertEqual(user.email, "normal45@gmail.com")
        self.assertTrue(user.check_password("987normal"))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@gmail.com",
            name="Admin User",
            phone_number="0787654321",
            password="adminpass123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class RegisterViewTest(APITestCase):
    def test_register_user(self):
        url = reverse("register")  
        data = {
            "name": "ryan Mukalo",
            "email": "ryan26@gmail.com",
            "phone_number": "0111222333",
            "password": "ryan@12345"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, "ryan26@gmail.com")


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="login56@gmail.com",
            name="Login User",
            password="testpass123",
            phone_number="0722333444"
        )

    def test_login_valid_user(self):
        url = reverse("login")  
        data = {
            "email": "login56@gmail.com",
            "password": "testpass123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_user(self):
        url = reverse("login")
        data = {
            "email": "wrong67@gmail.com",
            "password": "wrongpass"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="logout09@gmail.com",
            name="Logout User",
            password="testpass123",
            phone_number="555666777"
        )
        login_url = reverse("login")
        response = self.client.post(login_url, {
            "email": "logout09@gmail.com",
            "password": "testpass123"
        }, format="json")
        self.token = response.data["refresh"]  # store refresh token
        self.access = response.data["access"]

    def test_logout_user(self):
        url = reverse("logout")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(url, {"refresh": self.token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data["detail"], "Successfully logged out.")

