from rest_framework import serializers
from supplier.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['phone', 'name']

        def validate_phone(self, value):
            if not value.isdigit():
                raise serializers.ValidationError('Phone number must contain only digits.')
            if not value.startswith('0'):
                raise serializers.ValidationError('Phone number must start with 0.')
            if len(value) != 11:
                raise serializers.ValidationError('Phone number must be exactly 11 digits.')
            return value
