from rest_framework import serializers
# from .models import City    # -2dL (will delete later)
from cities_light.models import City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        fields = ('id', 'name', 'country')
