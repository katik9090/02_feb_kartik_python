from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    
    # Filtering fields
    filterset_fields = ['specialization', 'city']
    
    # Search fields (optional addition for better usability)
    search_fields = ['name', 'specialization', 'city']
    
    # Ordering fields
    ordering_fields = ['name']
    ordering = ['name']  # Default ordering

    @transaction.atomic
    def perform_create(self, serializer):
        # Wrap database save in atomic transaction
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        # Wrap database save in atomic transaction
        serializer.save()
