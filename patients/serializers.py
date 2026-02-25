from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for the Patient model."""

    class Meta:
        model = Patient
        fields = (
            'id',
            'name',
            'age',
            'gender',
            'phone',
            'email',
            'address',
            'medical_history',
            'created_by',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
