from django.db import models
from django.utils.timezone import now
# Create your models here.
from contracts.models import Contract

class Invoice(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name= 'invoice')
    issue_date = models.DateField(null=True)
    period_start = models.DateField(null=True)
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['contract', 'created_at', 'due_date']

    def __str__(self):
        return f"Factura #{self.id} - {self.contract} ({self.created_at} a {self.due_date})"