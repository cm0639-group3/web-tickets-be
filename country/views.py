from rest_framework import viewsets
# from .models import Country     # -2dL (will delete later)
from cities_light.models import Country
from .serializers import CountrySerializer
from .permissions import CustomPermissions_1
from rest_framework.permissions import  AllowAny, IsAuthenticated , IsAdminUser
from .pagination import CustomPagination, ConditionalPagination

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [CustomPermissions_1,]

    pagination_class = ConditionalPagination
