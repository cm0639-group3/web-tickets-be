from rest_framework import serializers
# from .models import Order
from ticket.models import Ticket

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        # fields = '__all__' 
        fields = ['id', 'user', 'flight', 'final_price' , 'purchased_at', 'is_purchased']
        read_only_fields = ('user',) 
