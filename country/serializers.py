from rest_framework import serializers
# from .models import Country       # -2dL (will delete later)
from cities_light.models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
