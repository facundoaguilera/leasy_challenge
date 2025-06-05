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
from operaciones.repositories.vehicle_repository import VehicleRepository
from operaciones.services.vehicle_status_service import VehicleStatusService

class OperacionesDashboardView(RoleRequiredMixin, ListView):
    model = Vehicle
    template_name = "operaciones/dashboard.html"
    paginate_by = 20
    required_role = 'operaciones'

    def get_queryset(self):
        vehicles = VehicleRepository.get_vehicles_with_contracts()
        return VehicleStatusService.annotate_vehicle_status(vehicles)
       
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