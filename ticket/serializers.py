from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        current_price = serializers.SerializerMethodField()
        is_available = serializers.SerializerMethodField()
        model = Ticket
        # fields = '__all__' 
        fields = ['id', 'user', 'flight', 'current_price' , 'is_purchased', 'is_available']
        read_only_fields = ('user',) 

        def get_current_price(self, obj):
            return obj.current_price
        def get_is_available(self, obj):
            return obj.is_available

