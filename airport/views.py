from rest_framework import viewsets

from .models import Airport
from .permissions import CustomPermissions_1
from .serializers import AirportSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [
        CustomPermissions_1,
    ]
