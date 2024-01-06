from rest_framework import viewsets
# from .models import City        # -2dL (will delete later)
from cities_light.models import City
from .serializers import CitySerializer
from .permissions import CustomPermissions_1
from .pagination import CustomPagination, ConditionalPagination

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [CustomPermissions_1,]

    pagination_class = ConditionalPagination
    
    def get_queryset(self):
        queryset = City.objects.all()
        country_id = self.request.query_params.get('country_id', None)
        country_code = self.request.query_params.get('country_code', None)

        if country_id is not None:
            queryset = queryset.filter(country_id=country_id)
        elif country_code is not None:
            queryset = queryset.filter(country__code2=country_code.upper())

        return queryset
