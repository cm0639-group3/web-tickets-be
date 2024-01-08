from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from .models import Luggage
from .filters import LuggageFilter
from .serializers import LuggageSerializer
from .permissions import LuggagePermissions

class LuggageViewSet(viewsets.ModelViewSet):
    queryset = Luggage.objects.all()
    serializer_class = LuggageSerializer
    ordering_fields = ['name', 'unit', 'size']

    filterset_class = LuggageFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)

    permission_classes = [LuggagePermissions]
