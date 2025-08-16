from rest_framework import serializers
from .models import Vehicle
from decimal import Decimal

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ('vehicle_id', 'created_at', 'status')

    def validate_hourly_rate(self, hourly_rate):
        if hourly_rate <= Decimal('0.00'):
            raise serializers.ValidationError("Please enter a valid hourly rate greater than zero.")
        if hourly_rate > Decimal('5000.00'):
            raise serializers.ValidationError("Hourly rate seems to be very high. cannot exceed 5000.00.")
        return hourly_rate

    def validate_licence_plate(self, licence_plate):
        if not licence_plate:
            raise serializers.ValidationError("Licence plate is required.")
        return licence_plate
    
    
    
    def validate_status(self, data):
       allowed_statuses = ['available', 'leased', 'maintenance',]
       if data['status'] not in allowed_statuses:
           raise serializers.ValidationError(f"Invalid status value. Should be one of: {', '.join(allowed_statuses)}.")
       return data
    
    def validate_type(self, data):
        allowed_types = ['matatu', 'motorcycle']
        if data['type'] not in allowed_types:
            raise serializers.ValidationError(f"Invalid vehicle type. Should be one of: {', '.join(allowed_types)}.")
        return data
   