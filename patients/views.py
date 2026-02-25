from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):

    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only patients belonging to the authenticated user."""
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """Auto-set created_by to the current user on creation."""
        serializer.save(created_by=self.request.user)
