from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .serializers import LeaseSerializer
from .models import lease
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView


class LeaseList(generics.ListCreateAPIView):
    queryset = lease.objects.all()
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to create a lease.")
        serializer.save()


class LeaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = lease.objects.all()
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'lease_id'

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to update this lease.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this lease.")
        instance.delete()

class LeaseApprove(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lease_id):
        lease_instance = lease.objects.get(lease_id=lease_id)
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to approve this lease.")
        
        # Logic to approve the lease
        lease_instance.status = 'active'
        lease_instance.save()
        
        return Response({"message": "Lease approved successfully."}, status=status.HTTP_200_OK)
    
class LeaseReject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lease_id):
        lease_instance = lease.objects.get(lease_id=lease_id)
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to reject this lease.")
        
        # Logic to reject the lease
        lease_instance.status = 'rejected'
        lease_instance.save()

        return Response({"message": "You are not qualified for this lease."}, status=status.HTTP_200_OK)
    
class LeaseReturn(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lease_id):
        lease_instance = lease.objects.get(lease_id=lease_id)
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to return this lease.")
        
        # Logic to mark the lease as returned
        lease_instance.status = 'returned'
        lease_instance.save()

        return Response({"message": "Lease returned successfully."}, status=status.HTTP_200_OK)
    
class LeaseStatusList(generics.ListAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        if status:
            return lease.objects.filter(status=status)
        return lease.objects.all()


