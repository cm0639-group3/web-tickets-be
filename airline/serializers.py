from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from cities_light.models import Country
from cities_light.contrib.restframework3 import CountrySerializer
from .models import Airline

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'
