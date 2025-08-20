from rest_framework import serializers
from .models import lease

class LeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = lease
        fields = '__all__'
        read_only_fields = ('lease_id', 'vehicle_id', 'start_date', 'end_date')

    def validate(self, data):
        if data['status'] not in ['active', 'pending', 'returned', 'rejected']:
            raise serializers.ValidationError("Invalid status value. Should be one of: active, pending, returned, rejected.")
        if data['lease_type'] not in ['hourly', 'daily', 'weekly']:
            raise serializers.ValidationError("Invalid lease type. Should be one of: hourly, daily, weekly.")
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data
    
    def validate_total_cost(self, value):
        if value < self.initial_data.get('total_cost', 0):
            raise serializers.ValidationError("please provide a valid total cost.")
        return value