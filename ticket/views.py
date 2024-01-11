from rest_framework import viewsets
from .models import Ticket
from .serializers import TicketSerializer
from .permissions import TicketPermissions

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [TicketPermissions]
