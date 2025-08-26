
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from .models import Qualification
import datetime
import uuid


class QualificationTests(APITestCase):

    def setUp(self):
        # Create a normal user
        self.user = User.objects.create_user(
            email="user@gmail.com",
            password="password123",
            name="normal User",
            phone_number="0712345678"
        )

        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            email="admin@gmail.com",
            password="adminpass123",
            name="Admin User",
            phone_number="0787654321",
            is_admin=True,
            is_staff=True
        )

        # Authenticate as the normal user for tests
        self.client.force_authenticate(user=self.user)

        # Default qualification payload
        self.valid_payload = {
            "user_id": str(self.user.user_id),  # ForeignKey requires user id
            "qualification_type": "driving_license",
            "issue_date": datetime.date(2023, 8, 21),
            "expiry_date": datetime.date(2025, 8, 21),
        }

    def test_create_qualification(self):
        # test for creating a qualification
        """Test creating a new qualification"""
        url = reverse("qualification-list")
        response = self.client.post(url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Qualification.objects.count(), 1)

    def test_list_qualifications(self):
        # test for listing qualifications
        """Test listing qualifications"""
        Qualification.objects.create(
            user_id=self.user,
            qualification_type="driving_license",
            issue_date=datetime.date(2023, 1, 1),
            expiry_date=datetime.date(2025, 1, 1)
        )
        url = reverse("qualification-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_qualification(self):
        # test for retrieving a single qualification
        """Test retrieving a single qualification"""
        qualification = Qualification.objects.create(
            user_id=self.user,
            qualification_type="driving_license",
            issue_date=datetime.date(2023, 1, 1),
            expiry_date=datetime.date(2025, 1, 1)
        )
        url = reverse("qualification-detail", args=[qualification.qualification_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["qualification_type"], "driving_license")

    def test_update_qualification(self):
        """Test updating a qualification"""
        qualification = Qualification.objects.create(
            user_id=self.user,
            qualification_type="driving_license",
            issue_date=datetime.date(2023, 1, 1),
            expiry_date=datetime.date(2025, 1, 1)
        )
        url = reverse("qualification-detail", args=[qualification.qualification_id])
        update_data = {
            "user_id": str(self.user.user_id),
            "qualification_type": "PSV_license",
            "issue_date": datetime.date(2023, 1, 1),
            "expiry_date": datetime.date(2026, 1, 1),
        }
        response = self.client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["qualification_type"], "PSV_license")

    def test_delete_qualification(self):
        """Test deleting a qualification"""
        qualification = Qualification.objects.create(
            user_id=self.user,
            qualification_type="driving_license",
            issue_date=datetime.date(2023, 1, 1),
            expiry_date=datetime.date(2025, 1, 1)
        )
        url = reverse("qualification-detail", args=[qualification.qualification_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Qualification.objects.count(), 0)

    def test_approve_qualification_admin_only(self):
        """Test approving a qualification (only admin allowed)"""
        qualification = Qualification.objects.create(
            user_id=self.user,
            qualification_type="driving_license",
            issue_date=datetime.date(2023, 1, 1),
            expiry_date=datetime.date(2025, 1, 1)
        )

        url = reverse("qualification-approve", args=[qualification.qualification_id])

        # Normal user should fail
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin should succeed
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        qualification.refresh_from_db()
        self.assertTrue(qualification.approved)