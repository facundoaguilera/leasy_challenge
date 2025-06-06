from django.db import models

# Create your models here.

class Vehicle(models.Model):
    brand = models.CharField("Marca", max_length=100)
    model = models.CharField("Modelo", max_length=100)
    plate = models.CharField("Placa", max_length=20, unique=True)
    vin = models.CharField("VIN", max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.plate}"