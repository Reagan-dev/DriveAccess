from rest_framework import serializers
from .models import lease
from decimal import Decimal, InvalidOperation
from django.utils import timezone

class LeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = lease
        fields = '__all__'


    def validate(self, data):


        start_time = self.instance.start_time if self.instance else timezone.now()
        end_time = data.get('end_time')


        if data['status'] not in ['active', 'pending', 'returned', 'rejected']:
            raise serializers.ValidationError("Invalid status value. Should be one of: active, pending, returned, rejected.")
        if data['lease_type'] not in ['hourly', 'daily', 'weekly']:
            raise serializers.ValidationError("Invalid lease type. Should be one of: hourly, daily, weekly.")
       
        if end_time and start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        return data
    
    def validate_total_cost(self, value):
        raw_total_cost = self.initial_data.get('total_cost', "0")

        try:
            total_cost_decimal = Decimal(raw_total_cost)
        except (InvalidOperation, TypeError):
            raise serializers.ValidationError("Invalid total_cost format.")

        if value < total_cost_decimal:
            raise serializers.ValidationError("Value cannot be less than total cost.")

        return value