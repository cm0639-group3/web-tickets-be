from django.db import models
from city.models import City
# Create your models here.
class Airport(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3)
    city = models.ForeignKey(City, on_delete=models.CASCADE)