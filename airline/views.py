from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Airline
from .serializers import AirlineSerializer
from .permissions import AirlinePermissions

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [AirlinePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_succsdess_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class AirlineListAPIView(generics.ListAPIView):
    serializer_class = AirlineSerializer

    def get_queryset(self):
        city_name = self.request.query_params.get('city', '')
        if city_name:
            return Airline.objects.filter(city__name__icontains=city_name)
        return Airline.objects.all()
