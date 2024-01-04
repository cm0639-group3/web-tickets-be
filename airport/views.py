from rest_framework import viewsets
from .models import Airport
from .serializers import AirportSerializer
from .permissions import CustomPermissions_1

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [CustomPermissions_1,]