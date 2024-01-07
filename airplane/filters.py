from django_filters import rest_framework as filters
from django_filters import RangeFilter, CharFilter, NumberFilter
from .models import Airplane

class AirplaneFilter(filters.FilterSet):
    class Meta:
        model = Airplane
        name = CharFilter(lookup_expr='icontains')
        model_number = CharFilter(lookup_expr='icontains')
        airline = NumberFilter(lookup_expr='exact')
        seats = RangeFilter(min=30, max=150)
        fields = '__all__'
