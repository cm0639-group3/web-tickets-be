from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from .models import Airplane
from .serializers import AirplaneSerializer
from .filters import AirplaneFilter
from .permissions import AirplanePermissions

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    ordering_fields = ['name', 'seats']
    filterset_class = AirplaneFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    permission_classes = [AirplanePermissions]
