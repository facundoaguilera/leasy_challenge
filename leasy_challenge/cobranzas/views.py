from django.views.generic import ListView, CreateView
from contracts.models import Contract
from invoices.models import Invoice
from contracts.forms import ContractForm
from users.mixins import RoleRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from cobranzas.services.contract_service import ContractService

class CobranzasDashboardView(RoleRequiredMixin, ListView):
    model = Contract
    template_name = "cobranzas/dashboard.html"
    paginate_by = 20
    required_role = 'cobranzas'
    context_object_name = "contracts"

    def get_queryset(self):
        return ContractService.get_contracts_with_extra_data()
    

class ContractCreateView(RoleRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'cobranzas/contract_form.html'
    success_url = reverse_lazy('cobranzas-dashboard')
    required_role = 'cobranzas'

    def form_valid(self, form):
        messages.success(self.request, "Contrato registrado correctamente.")
        return super().form_valid(form)

class InvoiceListView(RoleRequiredMixin, ListView):
    model = Invoice
    template_name = "cobranzas/invoices.html"
    paginate_by = 20
    required_role = 'cobranzas'

    def get_queryset(self):
        return Invoice.objects.select_related('contract__client')

