from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from contracts.models import Contract
from contracts.forms import ContractForm
from django.contrib import messages

class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contract_form.html"
    success_url = reverse_lazy("default-dashboard")  # o una URL de éxito específica

    def form_valid(self, form):
        print("Formulario válido:", form.cleaned_data)
        messages.success(self.request, "Contrato creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al registrar el contrato. Verifica los datos.")
        return super().form_invalid(form)
    