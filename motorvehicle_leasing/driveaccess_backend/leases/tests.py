from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
from accounts.models import User
from vehicles.models import Vehicle
from leases.models import lease


class LeaseTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users (admin and normal user)
        # Admin user
        self.admin_user = User.objects.create_user(
            email="admin@gmail.com",
            password="adminpass123",
            name="Admin User",
            phone_number="0712345678",
            is_staff=True,
            is_admin=True
        )
        # Normal user
        self.normal_user = User.objects.create_user(
            email="user@gmail.com",
            password="userpass123",
            name="Normal User",
            phone_number="0798765432"
        )

        # Authenticate as admin by default
        self.client.force_authenticate(user=self.admin_user)

        # Create a vehicle
        self.vehicle = Vehicle.objects.create(
          type="motorcycle",
          model="Honda",
          licence_plate="KDB456B",
          hourly_rate=Decimal("500.00"),
          location="Kisumu" 
        )

        # Create a lease
        self.lease = lease.objects.create(
            user_id=self.admin_user,
            vehicle_id=self.vehicle,
            lease_type="daily",
            status="pending",
            total_cost=Decimal("1000.00")
        )

    def test_list_leases(self):
        url = reverse("lease-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_lease_as_admin(self):
        url = reverse("lease-list")
        payload = {
            "user_id": self.admin_user.id,
            "vehicle_id": self.vehicle.id,
            "lease_type": "weekly",
            "status": "pending",
            "total_cost": "2000.00"
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["lease_type"], "weekly")

    def test_create_lease_as_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("lease-list")
        payload = {
            "user_id": self.normal_user.id,
            "vehicle_id": self.vehicle.id,
            "lease_type": "hourly",
            "status": "pending",
            "total_cost": "500.00"
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_approve_lease(self):
        url = reverse("lease-approve", args=[self.lease.lease_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lease.refresh_from_db()
        self.assertEqual(self.lease.status, "active")

    def test_reject_lease(self):
        url = reverse("lease-reject", args=[self.lease.lease_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lease.refresh_from_db()
        self.assertEqual(self.lease.status, "rejected")

    def test_return_lease(self):
        url = reverse("lease-return", args=[self.lease.lease_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lease.refresh_from_db()
        self.assertEqual(self.lease.status, "returned")

    def test_filter_lease_by_status(self):
        self.lease.status = "active"
        self.lease.save()
        url = reverse("lease-status-list") + "?status=active"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["status"], "active")
