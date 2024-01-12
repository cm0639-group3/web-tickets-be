from django_filters import rest_framework as filters
from django_filters import CharFilter, DateTimeFilter
from .models import Flight

class FlightFilter(filters.FilterSet):
    class Meta:
        model = Flight
        name = CharFilter(lookup_expr='icontains')
        source_airport = CharFilter(lookup_expr='icontains')
        destination_airport = CharFilter(lookup_expr='icontains')
        departure_time = DateTimeFilter(lookup_expr='range')
        arrival_time = DateTimeFilter(lookup_expr='range')
        fields = '__all__'
