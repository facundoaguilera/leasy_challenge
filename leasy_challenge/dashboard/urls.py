from dashboard.views import ReportRequestView, DashboardView
from django.urls import path

urlpatterns = [
    path('', DashboardView.as_view(), name="default-dashboard"),
    path('reporte/', ReportRequestView.as_view(), name='reporte-clientes'),
]
