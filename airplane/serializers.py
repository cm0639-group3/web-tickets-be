from rest_framework import serializers
from airline.serializers import AirlineSerializer
from airline.models import Airline
from .models import Airplane

class AirplaneSerializer(serializers.ModelSerializer):
    airline = AirlineSerializer(read_only=True)

    class Meta:
        model = Airplane
        fields = '__all__'

    def get_airline_if_exists(self):
        request = self.context.get('request')
        airline_data = request.data.get('airline')

        if airline_data is None:
            raise serializers.ValidationError("Missing 'airline' data in request")

        try:
            return Airline.objects.filter(**airline_data).first()
        except ObjectDoesNotExist:
            raise serializers.ValidationError("airline does not exist")


    def create(self, validated_data):
        airline = self.get_airline_if_exists()
        airplane_instance = Airplane.objects.create(airline=airline, **validated_data)
        return airplane_instance
