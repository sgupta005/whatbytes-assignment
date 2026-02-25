from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for the Doctor model."""

    class Meta:
        model = Doctor
        fields = (
            'id',
            'name',
            'specialization',
            'phone',
            'email',
            'experience_years',
            'created_by',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
