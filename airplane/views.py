from rest_framework import viewsets
from .models import Airplane
from .serializers import AirplaneSerializer
from .permissions import CustomPermissions_1
from rest_framework.permissions import  AllowAny, IsAuthenticated , IsAdminUser

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [CustomPermissions_1,]