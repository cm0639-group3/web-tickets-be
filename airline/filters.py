from django_filters import rest_framework as filters
from .models import Airline

class AirlineFilter(filters.FilterSet):
    class Meta:
        model = Airline
        fields = {
            'name': ['icontains'],
            'country__code2': ['icontains']
        }
