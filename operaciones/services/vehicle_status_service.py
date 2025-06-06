# vehicles/services/vehicle_status_service.py
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from django.utils.timezone import now

class VehicleStatusService:
    @staticmethod
    def annotate_vehicle_status(vehicles):
        today = now().date()

        for v in vehicles:
            contratos = sorted(v.contracts.all(), key=lambda c: c.start_date, reverse=True)
            v.tiene_contrato_activo = any(c.active for c in contratos)

            v.ultima_fecha_fin = None
            v.dias_desde_ultimo = None

            if not v.tiene_contrato_activo and contratos:
                ultimo = contratos[0]
                ciclo = ultimo.billing_cycle

                if ciclo == "weekly":
                    fecha_fin = ultimo.start_date + timedelta(weeks=1)
                elif ciclo == "biweekly":
                    fecha_fin = ultimo.start_date + timedelta(weeks=2)
                elif ciclo == "monthly":
                    fecha_fin = ultimo.start_date + relativedelta(months=1)
                else:
                    fecha_fin = None

                v.ultima_fecha_fin = fecha_fin
                if fecha_fin:
                    v.dias_desde_ultimo = (today - fecha_fin).days

        return vehicles