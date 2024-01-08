from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from cities_light.models import Country
from cities_light.contrib.restframework3 import CountrySerializer
from .models import Airline

class AirlineSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    class Meta:
        model = Airline
        fields = '__all__'

    def get_country_if_exists(self):
        request = self.context.get('request')
        country_data = request.data.get('country')

        if country_data is None:
            raise serializers.ValidationError("Missing 'country' data in request")

        try:
            return Country.objects.filter(**country_data).first()
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Country does not exist")


    def create(self, validated_data):
        country = self.get_country_if_exists()
        airline_instance = Airline.objects.create(country=country, **validated_data)
        return airline_instance
