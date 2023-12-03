from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(255)
    # flag = models.ImageField(upload_to='media/flags')