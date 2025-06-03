from django.views.generic import ListView, CreateView
from contracts.models import Contract
from invoices.models import Invoice
from contracts.forms import ContractForm
from users.mixins import RoleRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Sum, Min, Q, F, ExpressionWrapper, IntegerField
from django.db.models.functions import Now, ExtractDay
from datetime import date

class CobranzasDashboardView(RoleRequiredMixin, ListView):
    model = Contract
    template_name = "cobranzas/dashboard.html"
    paginate_by = 20
    required_role = 'cobranzas'
    context_object_name = "contracts"

    def get_queryset(self):
        return (
            Contract.objects.filter(active=True)
            .select_related("client", "vehicle")  # para evitar consultas extra por cliente y vehículo
            .prefetch_related("invoice")        # para cargar todas las invoices del contrato
            .annotate(
                cuotas_pendientes=Count("invoice", filter=Q(invoice__paid=False)),
                monto_pendiente=Sum("invoice__amount", filter=Q(invoice__paid=False)),
                fecha_mas_antigua=Min("invoice__due_date", filter=Q(invoice__paid=False)),
                    )
           
            )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for contract in context['contracts']:
            
            if contract.fecha_mas_antigua:
                if date.today()>contract.fecha_mas_antigua:
                    delta = date.today() - contract.fecha_mas_antigua
                    contract.dias_desde_mas_antigua = delta.days
                else:  contract.dias_desde_mas_antigua = 0
                # print("today",date.today() , "-", contract.fecha_mas_antigua)
                # print("dias desde mas antigua",delta.days )
            else:
                contract.dias_desde_mas_antigua = 0
        return context  

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

