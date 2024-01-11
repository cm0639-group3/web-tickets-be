from django_filters import rest_framework as filters
from django_filters import CharFilter
from .models import Airport

class AirportFilter(filters.FilterSet):
    class Meta:
        model = Airport
        name = CharFilter(lookup_expr='icontains')
        code = CharFilter(lookup_expr='icontains')
        city = CharFilter(lookup_expr='icontains')
        fields = '__all__'
