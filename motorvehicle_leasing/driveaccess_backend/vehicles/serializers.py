from rest_framework import serializers
from .models import Vehicle
from decimal import Decimal

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ('vehicle_id', 'created_at',)

    def get_fields(self):
        fields = super().get_fields()

        request = self.context.get('request')
        user = getattr(request, "user", None)

        # Make status read-only if:
        # - user is not authenticated
        # - OR user is not an admin
        if not (user and user.is_authenticated and getattr(user, "is_admin", False)):
            fields['status'].read_only = True

        return fields
    
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
       if data not in allowed_statuses:
           raise serializers.ValidationError(f"Invalid status value. Should be one of: {', '.join(allowed_statuses)}.")
       return data
    
    def validate_type(self, value):
        allowed_types = ['matatu', 'motorcycle']
        if value not in allowed_types:
            raise serializers.ValidationError(f"Invalid vehicle type. Should be one of: {', '.join(allowed_types)}.")
        return value
