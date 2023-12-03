from django.db import models
from airplane.models import Airplane
from airport.models import Airport
from luggage.models import Luggage
# Create your models here.
class Flight(models.Model):
    name = models.CharField(255)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    source_airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    luggage = models.ForeignKey(Luggage, on_delete=models.CASCADE)