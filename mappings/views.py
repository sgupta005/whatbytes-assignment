from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import PatientDoctorMapping
from .serializers import MappingSerializer
from patients.models import Patient


class MappingViewSet(viewsets.ModelViewSet):

    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        """Return mappings for patients owned by the authenticated user."""
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user
        ).select_related('patient', 'doctor')

    def perform_destroy(self, instance):
        """Only the patient's creator may delete a mapping."""
        if instance.patient.created_by != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this mapping."
            )
        instance.delete()


class PatientMappingListView(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, patient_id=None):
        # Verify patient exists and belongs to the user
        try:
            patient = Patient.objects.get(
                pk=patient_id, created_by=request.user
            )
        except Patient.DoesNotExist:
            return Response(
                {"detail": "Patient not found or you do not have access."},
                status=status.HTTP_404_NOT_FOUND,
            )

        mappings = PatientDoctorMapping.objects.filter(
            patient=patient
        ).select_related('patient', 'doctor')

        serializer = MappingSerializer(mappings, many=True, context={'request': request})
        return Response(serializer.data)
