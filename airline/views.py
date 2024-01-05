from rest_framework import viewsets
from .models import Airline
from .serializers import AirlineSerializer
from .permissions import CustomPermissions_1
from rest_framework.permissions import  AllowAny, IsAuthenticated , IsAdminUser

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [CustomPermissions_1,]