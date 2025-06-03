from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView
from vehicles.models import Vehicle
from contracts.models import Contract
from users.mixins import RoleRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class OperacionesDashboardView(RoleRequiredMixin, ListView):
    model = Vehicle
    template_name = "operaciones/dashboard.html"
    paginate_by = 20
    required_role = 'operaciones'

    def get_queryset(self):
        vehicles = Vehicle.objects.prefetch_related("contracts")
        today = now().date()

        for v in vehicles:
            contratos = sorted(v.contracts.all(), key=lambda c: c.start_date, reverse=True)
            v.tiene_contrato_activo = any(c.active for c in contratos)

            v.ultima_fecha_fin = None
            v.dias_desde_ultimo = None

            if not v.tiene_contrato_activo and contratos:
                ultimo = contratos[0]
                # Calcular fecha fin estimada según ciclo
                if ultimo.billing_cycle == "weekly":
                    fecha_fin = ultimo.start_date + timedelta(weeks=1)
                elif ultimo.billing_cycle == "biweekly":
                    fecha_fin = ultimo.start_date + timedelta(weeks=2)
                elif ultimo.billing_cycle == "monthly":
                    fecha_fin = ultimo.start_date + relativedelta(months=1)
                else:
                    fecha_fin = None

                v.ultima_fecha_fin = fecha_fin
                if fecha_fin:
                    v.dias_desde_ultimo = (today - fecha_fin).days

        return vehicles
class VehicleCreateView(RoleRequiredMixin, CreateView):
    model = Vehicle
    fields = ['brand', 'model', 'plate', 'vin']
    template_name = 'operaciones/vehicle_form.html'
    success_url = reverse_lazy('operaciones-dashboard')
    required_role = 'operaciones'

    def form_valid(self, form):
        messages.success(self.request, "Vehículo registrado exitosamente.")
        return super().form_valid(form)
    
class VehicleUpdateView(RoleRequiredMixin, UpdateView):
    model = Vehicle
    fields = ['brand', 'model', 'plate', 'vin']
    template_name = 'operaciones/vehicle_form.html'
    success_url = reverse_lazy('operaciones-dashboard')
    required_role = 'operaciones'

    def form_valid(self, form):
        messages.success(self.request, "Vehículo actualizado correctamente.")
        return super().form_valid(form)