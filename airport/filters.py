from django_filters import rest_framework as filters
from django_filters import RangeFilter, CharFilter, NumberFilter
from .models import Airport

class AirportFilter(filters.FilterSet):
    class Meta:
        model = Airport
        name = CharFilter(lookup_expr='icontains')
        model_number = CharFilter(lookup_expr='icontains')
        airport = NumberFilter(lookup_expr='exact')
        seats = RangeFilter(min=30)
        fields = '__all__'