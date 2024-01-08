from django_filters import rest_framework as filters
from django_filters import RangeFilter, CharFilter
from .models import Luggage

class LuggageFilter(filters.FilterSet):
    class Meta:
        model = Luggage
        name = CharFilter(lookup_expr='icontains')
        unit = CharFilter(lookup_expr='icontains')
        size = RangeFilter(lookup_expr="range")
        fields = '__all__'
