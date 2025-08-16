from rest_framework import serializers
from .models import payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = payment
        fields = '__all__'
        read_only_fields = ('payment_id', 'lease_id', 'payment_date')

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Please enter a valid amount greater than zero.")
        return amount
    
    def validate(self, data):
        if data['status'] not in ['pending', 'completed', 'failed']:
            raise serializers.ValidationError("Invalid status value. Should be one of: pending, completed, failed.")
        if data['payment_method'] not in ['credit_card', 'mobile_money', 'bank_transfer']:
            raise serializers.ValidationError("Invalid payment method.")
        return data