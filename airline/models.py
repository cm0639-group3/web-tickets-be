from django.db import models
from cities_light.models import Country
class Airline(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)