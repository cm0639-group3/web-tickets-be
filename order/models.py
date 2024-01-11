from django.db import models
from user.models import User
class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fulfilled = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'Order {self.id}, Total: {str(self.total)}'
