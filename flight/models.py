from django.db import models
from airplane.models import Airplane
from airport.models import Airport
from luggage.models import Luggage
# Create your models here.
class Flight(models.Model):
    name = models.CharField(max_length = 255)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    source_airport = models.ForeignKey(Airport, on_delete=models.CASCADE , related_name='source_airport')
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE , related_name='destination_airport')
    luggage = models.ForeignKey(Luggage, on_delete=models.CASCADE , null = True) 