from rest_framework import viewsets
from .models import Flight
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from .filters import FlightFilter
from .serializers import FlightSerializer
from .permissions import FlightPermissions

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from ticket.models import Ticket
from ticket.serializers import TicketSerializer
from luggage.models import Luggage

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    ordering_fields = ['name', 'departure_time', 'arrival_time']
    filterset_class = FlightFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    permission_classes = [FlightPermissions,]
        
    @action(detail=True, methods=['get'])
    def current_price(self, request, pk=None):
        flight = self.get_object()
        return Response({f'current price = {flight.current_price}'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        user = request.user        
        flight = self.get_object()        

        # # Assuming the user cannot add the same flight to the cart more than once
        # if Ticket.objects.filter(user=user, flight=flight, is_purchased=False).exists():
        #     return Response({'message': 'This flight is already in your cart'}, status=status.HTTP_400_BAD_REQUEST)
        if flight.remaining_seats <= 0:
            return Response({'status': 'failed' , 'message': 'No tickets available'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            luggage_id = request.data.get('luggage')
            if luggage_id:
                luggage = Luggage.objects.get(id=luggage_id)
            else:
                luggage = Luggage.objects.get(id=1)         ## default luggage (eg, without luggage)
            
            ticket = Ticket.objects.create(user=user, flight=flight, is_purchased=False , luggage=luggage)
            serializer = TicketSerializer(ticket)
            return Response({'status': 'success' , 'message': 'Ticket added to cart successfully', 'ticket': serializer.data}, status=status.HTTP_200_OK)


    def get_serializer_context(self):
        context = super(FlightViewSet, self).get_serializer_context()
        context['luggage'] = self.request.query_params.get('luggage')
        return context