from django.db import models
from django.contrib.auth.models import AbstractUser
from roles.models import Role
# Create your models here.
class User(AbstractUser):
    # role = models.ForeignKey(Role, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username