from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return all doctors — listing is not restricted by ownership."""
        return Doctor.objects.all()

    def perform_create(self, serializer):
        """Auto-set created_by to the current user on creation."""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Only the doctor's creator may update it."""
        if serializer.instance.created_by != self.request.user:
            raise PermissionDenied("You do not have permission to update this doctor.")
        serializer.save()

    def perform_destroy(self, instance):
        """Only the doctor's creator may delete it."""
        if instance.created_by != self.request.user:
            raise PermissionDenied("You do not have permission to delete this doctor.")
        instance.delete()
