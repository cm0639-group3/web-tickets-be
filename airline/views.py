from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from .models import Airline
from .filters import AirlineFilter
from .serializers import AirlineSerializer
from .permissions import AirlinePermissions

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    ordering_fields = ['name', 'country']
    filterset_class = AirlineFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    permission_classes = [AirlinePermissions]
