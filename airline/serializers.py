from rest_framework import serializers
from cities_light.models import Country
from .models import Airline

class AirlineSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        slug_field='code2',
        queryset=Country.objects.all(),
        error_messages={
            'does_not_exist': 'Country with 2-letter ISO code={value} does not exist.',
        }
    )
    class Meta:
        model = Airline
        fields = ('id', 'name', 'country')
