from rest_framework import viewsets
from .models import Flight
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from .filters import FlightFilter
from .serializers import FlightSerializer
from .permissions import FlightPermissions

import operator
from django.db.models import Q
from functools import reduce
from datetime import datetime

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    ordering_fields = ['name', 'departure_time', 'arrival_time']
    filterset_class = FlightFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    permission_classes = [FlightPermissions,]

    def get_queryset(self):
        q_list = []

        airplane = self.request.query_params.get('airplane', None)
        if airplane:
            q_list.append(Q(airplane=airplane))

        source_airport = self.request.query_params.get('source_airport', None)
        if source_airport:
            q_list.append(Q(source_airport=source_airport))

        destination_airport = self.request.query_params.get('destination_airport', None)
        if destination_airport:
            q_list.append(Q(destination_airport=destination_airport))

        departure_time = self.request.query_params.get('departure_time', None)
        if departure_time:
            try:
                departure_datetime = datetime.fromisoformat(departure_time.rstrip("Z"))
            except ValueError:
                return queryset.none()
            # Filter by date part
            departure_time_queryset = Q(
                departure_time__year=departure_datetime.year,
                departure_time__month=departure_datetime.month,
                departure_time__day=departure_datetime.day
            )
            q_list.append(departure_time_queryset)

        arrival_time = self.request.query_params.get('arrival_time', None)
        if arrival_time:
            try:
                arrival_datetime = datetime.fromisoformat(arrival_time.rstrip("Z"))
            except ValueError:
                return queryset.none()
            # Filter by date part
            arrival_time_queryset = Q(
                arrival_time__year=arrival_datetime.year,
                arrival_time__month=arrival_datetime.month,
                arrival_time__day=arrival_datetime.day
            )
            q_list.append(arrival_time_queryset)


        if q_list:
            queryset = Flight.objects.filter(reduce(operator.and_, q_list))
        else:
            queryset = Flight.objects.all()

        return queryset
