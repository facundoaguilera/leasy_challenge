from django.urls import path
from .views import VentasDashboardView,  ClientCreateView, ClientUpdateView

urlpatterns = [
    path("", VentasDashboardView.as_view(), name="ventas-dashboard"),
    path('nuevo/', ClientCreateView.as_view(), name='crear-cliente'),
    path('<int:pk>/editar/', ClientUpdateView.as_view(), name='editar-cliente'),
]