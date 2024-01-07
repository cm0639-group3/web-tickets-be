from rest_framework import viewsets
from rest_framework.response import Response
from .models import Airplane
from rest_framework import status
from .serializers import AirplaneSerializer
from .permissions import AirplanePermissions

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [AirplanePermissions]
