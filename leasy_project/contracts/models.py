from django.db import models

# Create your models here.
from clients.models import Client
from vehicles.models import Vehicle
from django.db.models import Q, UniqueConstraint

class Contract(models.Model):
    BILLING_CYCLES = [
        ("weekly", "Semanal"),
        ("biweekly", "Quincenal"),
        ("monthly", "Mensual"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name= "contracts") 
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name= "contracts")
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CYCLES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['client'], condition=Q(active=True), name='unique_active_contract_per_client'),
            UniqueConstraint(fields=['vehicle'], condition=Q(active=True), name='unique_active_contract_per_vehicle'),
        ]
    def __str__(self):
        return f"{self.client} - {self.vehicle} ({self.billing_cycle})"