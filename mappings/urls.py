from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MappingViewSet, PatientMappingListView

router = DefaultRouter()
router.register('', MappingViewSet, basename='mapping')

urlpatterns = [
    # Custom route: GET /api/mappings/<patient_id>/ — doctors for a patient
    path(
        '<int:patient_id>/',
        PatientMappingListView.as_view({'get': 'list'}),
        name='patient-mapping-list',
    ),
    # Standard CRUD routes (list, create, delete)
    path('', include(router.urls)),
]
