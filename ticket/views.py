from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Ticket
from .serializers import TicketSerializer
from .permissions import TicketPermissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [TicketPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():     
            ## check if there's remaining seat available.
            if serializer.validated_data['flight'].remaining_seats <= 0:
                return Response({"error": "No seats available for this flight."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user , is_purchased=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        ticket = self.get_object()        
        if ticket.is_purchased:
            return Response({"error": "Purchased tickets cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        return super(TicketViewSet, self).destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user

        # to allow admin to retrieve all users tickets or not
        all_users_str = self.request.query_params.get('all_users', False)  
        all_users_bool = str(all_users_str).lower() in ['true', '1', 'yes']

        if all_users_bool and (user.is_staff or user.is_superuser):
            return Ticket.objects.all()
        else:
            # or only retrieve the user's tickets 
            return Ticket.objects.filter(user=user)
        
    @action(detail=True, methods=['get'])
    def current_price(self, request, pk=None):
        flight = self.get_object().flight
        return Response({f'current price = {flight.current_price}'}, status=status.HTTP_200_OK)