from django.db import models
from airline.models import Airline
# Create your models here.
class Airplane(models.Model):
    name = models.CharField(max_length=255)
    seats = models.IntegerField()
    model_number = models.CharField(max_length=10, unique=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)