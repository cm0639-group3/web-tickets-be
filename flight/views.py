from rest_framework import viewsets
from .models import Flight
from .serializers import FlightSerializer
from .permissions import FlightPermissions

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [FlightPermissions,]