from rest_framework import serializers
from .models import Flight
from luggage.models import Luggage  

class FlightSerializer(serializers.ModelSerializer):
    current_price = serializers.SerializerMethodField()
    class Meta:
        model = Flight
        fields = '__all__'
        extra_kwargs = {'base_price': {'required': True}} 

    current_price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    def get_current_price(self, obj):
        base_price = obj.current_price
        luggage_id = self.context.get('luggage')
        if luggage_id:
            luggage = Luggage.objects.get(id=luggage_id)
            additional_price = luggage.size
            return base_price + additional_price
        return base_price

    def get_is_available(self, obj):
        return obj.is_available
