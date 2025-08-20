from rest_framework import serializers
from .models import payment
from leases.models import lease



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
    
    def validate(self, data):
        lease = data.get('lease_id')
        user = data.get('user_id')
        amount = data.get('amount')

        if not lease:
            raise serializers.ValidationError("lease is required.")
        
        if lease.user_id != user:
            raise serializers.ValidationError("User does not have permission to make this payment for the lease.")
        
        if hasattr(lease, 'total_cost') and amount < lease.total_cost:
            raise serializers.ValidationError("Payment amount cannot be less than the total cost of the lease.")
        
        return data
    
    def create(self, validated_data):
        lease = validated_data.get('lease_id')
        user = validated_data.get('user_id')
        
        if not lease or not user:
            raise serializers.ValidationError("Lease and User are required to create a payment.")
        
        # Ensure the user is associated with the lease
        if lease.user_id != user:
            raise serializers.ValidationError("User does not have permission to make this payment for the lease.")
        
        return super().create(validated_data)
    
        
    
    