from rest_framework import serializers
from .models import vehiclequalification

class VehiclequalificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehiclequalification
        fields = '__all__'
        read_only_fields = ('qualification_id', 'vehicle_id', 'vehiclequalification_id')


    def validate(self, data):
        if vehiclequalification.objects.filter(
            vehicle=data['vehicle'],
            qualification=data['qualification']
        ).exists():
            raise serializers.ValidationError("This qualification is already assigned to this vehicle")
        return data

   