from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from accounts.models import User
from vehicles.models import Vehicle
from leases.models import lease
from payments.models import payment


class PaymentTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.admin_user = User.objects.create_user(
            email="admin@gmail.com",
            password="adminpass123",
            name="Admin User",
            phone_number="0712345678",
            is_staff=True,
            is_admin=True
        )
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

        # Create a lease for the normal user
        self.lease = lease.objects.create(
            user_id=self.normal_user,
            vehicle_id=self.vehicle,
            lease_type="daily",
            status="pending",
            total_cost=Decimal("1500.00")
        )

        # Create a payment for that lease
        self.payment = payment.objects.create(
            user_id=self.normal_user,
            lease_id=self.lease,
            amount=Decimal("1500.00"),
            payment_method="mobile_money",
            status="pending"
        )

    def test_list_payments_as_admin(self):
        url = reverse("payment-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_payments_as_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("payment-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only their payments should be visible
        for p in response.data:
            self.assertEqual(p["user_id"], self.normal_user.id)

    def test_create_payment_for_own_lease(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("payment-list-create")
        payload = {
            "lease_id": self.lease.id,
            "amount": "1500.00",
            "payment_method": "credit_card",
            "status": "pending"
        }
        response = self.client.post(url, payload, format="json")
        # Debugging: Print response data if not created
        if response.status_code != status.HTTP_201_CREATED:
            print("Response data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], "1500.00")
        self.assertEqual(response.data["payment_method"], "credit_card")
        self.assertEqual(response.data["lease_id"], self.lease.id)

    def test_create_payment_for_other_users_lease_forbidden(self):
        # Lease owned by admin
        admin_lease = lease.objects.create(
            user_id=self.admin_user,
            vehicle_id=self.vehicle,
            lease_type="hourly",
            total_cost=Decimal("800.00"),
        )

        self.client.force_authenticate(user=self.normal_user)
        url = reverse("payment-list-create")
        payload = {
            "lease_id": str(admin_lease.id),
            "amount": "500.00",
            "payment_method": "mobile_money",
            "status": "pending"
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_approve_payment_as_admin(self):
        url = reverse("payment-approve", args=[self.payment.payment_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, "completed")

    def test_reject_payment_as_admin(self):
        url = reverse("payment-reject", args=[self.payment.payment_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, "failed")

    def test_approve_payment_as_normal_user_forbidden(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("payment-approve", args=[self.payment.payment_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_payment_as_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse("payment-detail", args=[self.payment.payment_id])
        response = self.client.patch(url, {"amount": "2000.00"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
