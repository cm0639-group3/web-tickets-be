from django_filters import rest_framework as filters
from django_filters import CharFilter, DateTimeFilter
from .models import Flight
from datetime import datetime

class FlightFilter(filters.FilterSet):
    departure_time = CharFilter(method='filter_departure_time')
    arrival_time = CharFilter(method='filter_arrival_time')
    
    # Custom departure time filter
    def filter_departure_time(self, queryset, name, value):
        try:
            departure_datetime = datetime.fromisoformat(value.rstrip("Z"))
        except ValueError:
            return queryset.none()

        return queryset.filter(
            departure_time__year=departure_datetime.year,
            departure_time__month=departure_datetime.month,
            departure_time__day=departure_datetime.day
        )
    
    # Custom arrival time filter
    def filter_arrival_time(self, queryset, name, value):
        try:
            arrival_datetime = datetime.fromisoformat(value.rstrip("Z"))
        except ValueError:
            return queryset.none()

        return queryset.filter(
            arrival_time__year=arrival_datetime.year,
            arrival_time__month=arrival_datetime.month,
            arrival_time__day=arrival_datetime.day
        )

    class Meta:
        model = Flight
        name = CharFilter(lookup_expr='icontains')
        airplane = CharFilter(lookup_expr='icontains')
        source_airport = CharFilter(lookup_expr='icontains')        
        destination_airport = CharFilter(lookup_expr='icontains')
        fields = '__all__'
