import operator
from datetime import datetime
from functools import reduce

from django.db.models import Q
from rest_framework import viewsets

from .models import Flight
from .permissions import FlightPermissions
from .serializers import FlightSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [
        FlightPermissions,
    ]

    def get_queryset(self):
        q_list = []

        airplane = self.request.query_params.get("airplane", None)
        if airplane:
            q_list.append(Q(airplane=airplane))

        source_airport = self.request.query_params.get("source_airport", None)
        if source_airport:
            q_list.append(Q(source_airport=source_airport))

        destination_airport = self.request.query_params.get("destination_airport", None)
        if destination_airport:
            q_list.append(Q(destination_airport=destination_airport))

        departure_time = self.request.query_params.get("departure_time", None)
        if departure_time:
            try:
                departure_datetime = datetime.fromisoformat(departure_time.rstrip("Z"))
            except ValueError:
                return queryset.none()
            # Filter by date part
            departure_time_queryset = Q(
                departure_time__year=departure_datetime.year,
                departure_time__month=departure_datetime.month,
                departure_time__day=departure_datetime.day,
            )
            q_list.append(departure_time_queryset)

        arrival_time = self.request.query_params.get("arrival_time", None)
        if arrival_time:
            try:
                arrival_datetime = datetime.fromisoformat(arrival_time.rstrip("Z"))
            except ValueError:
                return queryset.none()
            # Filter by date part
            arrival_time_queryset = Q(
                arrival_time__year=arrival_datetime.year,
                arrival_time__month=arrival_datetime.month,
                arrival_time__day=arrival_datetime.day,
            )
            q_list.append(arrival_time_queryset)

        if q_list:
            queryset = Flight.objects.filter(reduce(operator.and_, q_list))
        else:
            queryset = Flight.objects.all()

        return queryset
