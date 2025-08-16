from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import VehicleSerializer
from .models import Vehicle
from rest_framework.exceptions import PermissionDenied


# Create your views here.
# Get all vehicles (public, filter by type, status)
class VehicleListView(generics.ListAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        vehicle_type = self.request.query_params.get('type', None)
        status = self.request.query_params.get('status', None)

        if vehicle_type:
            queryset = queryset.filter(type=vehicle_type)
        if status:
            queryset = queryset.filter(status=status)

        return queryset
    
# POST a new vehicle (admin only)
class VehicleCreateView(generics.CreateAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def create(self, request, *args, **kwargs):
       if not request.user.is_admin:
            raise PermissionDenied("You do not have permission to add vehicles.")
       return super().create(request, *args, **kwargs)
    
# PUT/vehicle/<vehicle_id> (admin only, update vehicle details, status, soft delete)
class VehicleUpdateView(generics.UpdateAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    lookup_field = 'vehicle_id'

    def get_queryset(self):
        return Vehicle.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if "soft_delete" in request.data and request.data["soft_delete"] is True:
            instance.status = "maintenance"
            instance.save()
            return Response({"message": "Vehicle soft-deleted (set to maintenance)."}, status=status.HTTP_200_OK)

        return super().update(request, *args, **kwargs)