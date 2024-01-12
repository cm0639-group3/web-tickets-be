from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Airport
from .filters import AirportFilter
from .serializers import AirportSerializer
from .permissions import CustomPermissions_1

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    ordering_fields = ['city']
    filterset_class = AirportFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter,)    # Enabel filtering and ordering
    permission_classes = [CustomPermissions_1,]
