from rest_framework import serializers
from .models import payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = payment
        fields = '__all__'
        read_only_fields = ('payment_id', 'payment_date', 'user_id')  

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Please enter a valid amount greater than zero.")
        return amount

    def validate(self, data):
        lease = data.get('lease_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method')
        status_value = data.get('status')

        if not lease:
            raise serializers.ValidationError("Lease is required.")

        if status_value not in ['pending', 'completed', 'failed']:
            raise serializers.ValidationError("Invalid status value. Should be one of: pending, completed, failed.")

        if payment_method not in ['credit_card', 'mobile_money', 'bank_transfer']:
            raise serializers.ValidationError("Invalid payment method.")

        # check lease cost
        if hasattr(lease, 'total_cost') and amount < lease.total_cost:
            raise serializers.ValidationError("Payment amount cannot be less than the total cost of the lease.")

        return data
        
    
    