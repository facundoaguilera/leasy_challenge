from django.urls import path
from .views import ContractCreateView

urlpatterns = [
    path('nuevo/', ContractCreateView.as_view(), name='crear-contrato'),
]
