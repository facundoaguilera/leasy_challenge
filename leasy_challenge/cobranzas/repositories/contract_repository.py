from contracts.models import Contract
from django.db.models import Q, Sum, Count, Min, F, ExpressionWrapper
from django.db.models.functions import Now
from django.db.models import DurationField
from datetime import date

class ContractRepository:
    def get_active_contracts_with_annotations():
        return (
            Contract.objects.filter(active=True).order_by("-start_date")
            .select_related("client", "vehicle")  # para evitar consultas extra por cliente y vehículo
            .prefetch_related("invoice")        # para cargar todas las invoices del contrato
            .annotate(
                cuotas_pendientes=Count("invoice", filter=Q(invoice__paid=False)),
                monto_pendiente=Sum("invoice__amount", filter=Q(invoice__paid=False)),
                fecha_mas_antigua=Min("invoice__due_date", filter=Q(invoice__paid=False)),
                    )
           
            )
    