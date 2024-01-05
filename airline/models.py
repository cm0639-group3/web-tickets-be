from django.db import models
# from country.models import Country    # -2dL
from cities_light.models import Country
# Create your models here.
class Airline(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)