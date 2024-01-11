from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import serializers
from cities_light.models import City
from cities_light.contrib.restframework3 import CitySerializer
from .models import Airport

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'
