from rest_framework import serializers
from .models import Luggage

class LuggageSerializer(serializers.ModelSerializer):
    """ Serializer for luggage type"""
    class Meta:
        model = Luggage
        fields = '__all__'
