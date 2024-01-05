from django.db import models
from airplane.models import Airplane
from airport.models import Airport
from luggage.models import Luggage

class Flight(models.Model):
    name = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    source_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='+')
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='+')
    luggage = models.ForeignKey(Luggage, on_delete=models.CASCADE)

    def clean(self):
        if self.departure_time and self.arrival_time and self.departure_time >= self.arrival_time:
            raise ValueError("Departure time must be before arrival time.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Flight {self.id} - Name: {self.name}, Departure: {str(self.departure_time)}, Arrival: {str(self.arrival_time)}, Airplane: {str(self.airplane)}, Source: {str(self.source_airport)}, Destination: {str(self.destination_airport)}, Luggage: {str(self.luggage)}'