from django.db import models

class Branch(models.Model):
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.city