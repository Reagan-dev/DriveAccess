from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from accounts.models import User
from .models import Vehicle


class VehicleModelTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            type="matatu",
            model="Toyota Hiace",
            licence_plate="KDA123A",
            hourly_rate=Decimal("1000.00"),
            location="Nairobi"
        )

    def test_vehicle_creation(self):
        self.assertEqual(self.vehicle.model, "Toyota Hiace")
        self.assertEqual(self.vehicle.status, "available")

    def test_mark_as_maintenance(self):
        self.vehicle.mark_as_maintenance()
        self.assertEqual(self.vehicle.status, "maintenance")

    def test_mark_as_available(self):
        self.vehicle.mark_as_available()
        self.assertEqual(self.vehicle.status, "available")

    def test_mark_as_leased(self):
        self.vehicle.mark_as_leased()
        self.assertEqual(self.vehicle.status, "leased")


class VehicleAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users (admin and normal user)
        self.admin_user = User.objects.create_user(
            email="admin@gmail.com", name="Admin User",
            password="adminpass123", phone_number="0711111111",
            is_admin=True, is_staff=True
        )
        self.normal_user = User.objects.create_user(
            email="user@gmail.com", name="Normal User",
            password="userpass123", phone_number="0722222222"
        )

        # Create a sample vehicle
        self.vehicle = Vehicle.objects.create(
            type="motorcycle",
            model="Honda",
            licence_plate="KDB456B",
            hourly_rate=Decimal("500.00"),
            location="Kisumu"
        )

    def test_get_vehicle_list(self):
        response = self.client.get(reverse("vehicle-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_vehicle_by_type(self):
        response = self.client.get(reverse("vehicle-list"), {"type": "motorcycle"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["type"], "motorcycle")

    def test_create_vehicle_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "type": "matatu",
            "model": "Nissan Caravan",
            "licence_plate": "KDC789C",
            "hourly_rate": "2000.00",
            "location": "Mombasa",
        }
        response = self.client.post(reverse("vehicle-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vehicle_as_normal_user_forbidden(self):
        self.client.force_authenticate(user=self.normal_user)
        data = {
            "type": "matatu",
            "model": "Nissan Caravan",
            "licence_plate": "KDC890D",
            "hourly_rate": "2000.00",
            "location": "Nakuru",
        }
        response = self.client.post(reverse("vehicle-create"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_vehicle_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("vehicle-update", args=[self.vehicle.vehicle_id])
        response = self.client.put(url, {"status": "maintenance"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.status, "maintenance")

    def test_update_vehicle_as_normal_user_forbidden(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("vehicle-update", args=[self.vehicle.vehicle_id])
        response = self.client.put(url, {"status": "leased"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
