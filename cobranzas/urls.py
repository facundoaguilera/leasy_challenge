from django.urls import path
from .views import (
    CobranzasDashboardView,
    ContractCreateView,
    InvoiceListView,
)

urlpatterns = [
    path('', CobranzasDashboardView.as_view(), name='cobranzas-dashboard'),
    path('nuevo-contrato/', ContractCreateView.as_view(), name='crear-contrato'),
    path('facturas/', InvoiceListView.as_view(), name='listar-facturas'),
]
