from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from .serializers import PaymentSerializer
from .models import payment


# GET /payments and POST /payments
class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Admins see all payments, users see only their own
        if self.request.user.is_staff:
            return payment.objects.all()
        return payment.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the current user
        lease = serializer.validated_data.get("lease_id")

        if lease.user_id != self.request.user:
            raise PermissionDenied("You can only make payments for your own leases.")

        serializer.save(user_id=self.request.user)


# GET one payment, update/delete (staff only)
class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Admins see all, users see only their own
        if self.request.user.is_staff:
            return payment.objects.all()
        return payment.objects.filter(user_id=self.request.user)

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admins can update payments.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admins can delete payments.")
        instance.delete()


# Approve payment (staff only)
class PaymentApprove(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, payment_id):
        payment_instance = get_object_or_404(payment, payment_id=payment_id)

        if not request.user.is_staff:
            raise PermissionDenied("Only admins can approve payments.")

        payment_instance.status = "completed"
        payment_instance.save()
        return Response({"message": "Payment approved successfully."}, status=status.HTTP_200_OK)


# Reject payment (staff only)
class PaymentReject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, payment_id):
        payment_instance = get_object_or_404(payment, payment_id=payment_id)

        if not request.user.is_staff:
            raise PermissionDenied("Only admins can reject payments.")

        payment_instance.status = "failed"
        payment_instance.save()
        return Response({"message": "Payment rejected successfully."}, status=status.HTTP_200_OK)