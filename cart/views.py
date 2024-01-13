from rest_framework import viewsets
from .permissions import CartPermissions
from ticket.models import Ticket
from ticket.serializers import TicketSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class CartViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [CartPermissions,]

    def get_queryset(self):
        user = self.request.user

        # to allow admin to retrieve all users tickets or not
        all_users_str = self.request.query_params.get('all_users', False)  
        all_users_bool = str(all_users_str).lower() in ['true', '1', 'yes']

        if all_users_bool and (user.is_staff or user.is_superuser):
            return Ticket.objects.filter(is_purchased=False)
        else:
            # or only retrieve the user's tickets 
            return Ticket.objects.filter(user=user, is_purchased=False)

    @action(detail=False, methods=['post'])
    def buy_tickets(self, request):
        user = request.user
        tickets_to_purchase = Ticket.objects.filter(user=user, is_purchased=False )

        if not tickets_to_purchase.exists():
            return Response({'status': 'failed' , "message": "No unpurchased tickets to buy."}, status=400)
        
        total_price = 0
        is_available= True      # to check for any not available ticket

        for ticket in tickets_to_purchase:
            total_price += ticket.current_price            
            if not ticket.is_available:
                is_available = False
                break
        ## if not available, response by failed, otherwise continue
        if is_available == False:
            return Response({'status': 'failed' , "message": "Not enough seats available."}, status=400)

        # check for payment
        payment_check = True
        if payment_check:
            for ticket in tickets_to_purchase:
                ticket.buy()
            return Response({"status": "success", "message": f"All unpurchased tickets purchased successfully with total price =  {total_price}"})
        else:
            return Response({'status': 'failed' , "message": "Payment failed."}, status=400)
        
    @action(detail=False, methods=['delete'])
    def clear_cart(self, request, *args, **kwargs):
            user = request.user
            tickets_to_delete = Ticket.objects.filter(user=user, is_purchased=False)
            if tickets_to_delete.exists():
                tickets_to_delete.delete()
                return Response({'status': 'success' , 'message': 'All cart tickets had been deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'status': 'failed' , 'message': 'No unpurchased tickets found for the user.'}, status=status.HTTP_404_NOT_FOUND)


