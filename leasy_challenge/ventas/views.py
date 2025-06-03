from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView, UpdateView, ListView
from clients.models import Client
from users.mixins import RoleRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

class VentasDashboardView(RoleRequiredMixin, ListView):
    model = Client
    template_name = "ventas/dashboard.html"
    paginate_by = 20
    required_role = 'ventas'

    def get_queryset(self):
        return Client.objects.all().order_by("last_name", "first_name")

class ClientCreateView(RoleRequiredMixin, CreateView):
    model = Client
    fields = ['first_name', 'last_name', 'document_number']
    template_name = 'ventas/client_form.html'
    success_url = reverse_lazy('ventas-dashboard')
    required_role = 'ventas'

    def form_valid(self, form):
        messages.success(self.request, "Cliente creado exitosamente.")
        return super().form_valid(form)

class ClientUpdateView(RoleRequiredMixin, UpdateView):
    model = Client
    fields = ['first_name', 'last_name', 'document_number']
    template_name = 'ventas/client_form.html'
    success_url = reverse_lazy('ventas-dashboard')
    required_role = 'ventas'

    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente.")
        return super().form_valid(form)