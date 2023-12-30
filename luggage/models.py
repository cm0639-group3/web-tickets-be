from django.db import models


# Create your models here.
class Luggage(models.Model):
    name = models.CharField(max_length=20)
    size = models.IntegerField()
    unit = models.CharField(max_length=10)
