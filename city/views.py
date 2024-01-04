from rest_framework import viewsets
from .models import City
from .serializers import CitySerializer
from .permissions import CustomPermissions_1


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [CustomPermissions_1,]