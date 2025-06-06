from django.urls import path
from .views import OperacionesDashboardView, VehicleCreateView, VehicleUpdateView

urlpatterns = [
    path('', OperacionesDashboardView.as_view(), name='operaciones-dashboard'),
    path('nuevo/', VehicleCreateView.as_view(), name='crear-vehiculo'),
    path('<int:pk>/editar/', VehicleUpdateView.as_view(), name='editar-vehiculo'),
]