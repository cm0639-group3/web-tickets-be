from rest_framework import viewsets
from .serializers import OrderSerializer
from .permissions import OrderPermissions
from ticket.models import Ticket

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermissions,]

    def get_queryset(self):
        user = self.request.user

        # to allow admin to retrieve all users tickets or not
        all_users_str = self.request.query_params.get('all_users', False)  
        all_users_bool = str(all_users_str).lower() in ['true', '1', 'yes']

        if all_users_bool and (user.is_staff or user.is_superuser):
            return Ticket.objects.filter(is_purchased=True)
        else:
            # or only retrieve the user's tickets 
            return Ticket.objects.filter(user=user, is_purchased=True)