from rest_framework import serializers

from .models import PatientDoctorMapping
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer


class MappingSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = (
            'id',
            'patient',
            'doctor',
            'patient_detail',
            'doctor_detail',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def validate(self, data):
        """Ensure the patient belongs to the requesting user."""
        request = self.context.get('request')
        patient = data.get('patient')
        if patient and request and patient.created_by != request.user:
            raise serializers.ValidationError(
                {"patient": "You can only create mappings for your own patients."}
            )
        return data
