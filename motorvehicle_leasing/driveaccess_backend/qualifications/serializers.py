from rest_framework import serializers
from .models import Qualification

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'
        read_only_fields = ('qualification_id', 'approved')


    def validate_qualification_type(self, value):
        allowed_types = ['driving_license', 'PSV_license']
        if value not in allowed_types:
            raise serializers.ValidationError(f"Invalid qualification type. Should be one of: {', '.join(allowed_types)}.")
        return value
    
    def validate(self, data):
        issue_date = data.get('issue_date')
        expiry_date = data.get('expiry_date')

        if issue_date and expiry_date and issue_date >= expiry_date:
            raise serializers.ValidationError("Issue date must be before expiry date.")

        return data
