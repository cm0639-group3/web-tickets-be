from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from .models import Airport
from .serializers import AirportSerializer
from .filters import AirportFilter
from .permissions import CustomPermissions_1

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    ordering_fields = ['name', 'code', 'city']
    filterset_class = AirportFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    permission_classes = [CustomPermissions_1,]
