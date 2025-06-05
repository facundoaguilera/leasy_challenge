import csv
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from clients.models import Client
from vehicles.models import Vehicle
from contracts.models import Contract
from django.db.models import Q
from django.shortcuts import redirect
from dashboard.forms import ReportForm
from django_rq import enqueue
import tempfile
from openpyxl import Workbook
import os
from .tasks import generate_report_and_send_email
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta 
from django.utils.dateparse import parse_date
from django.db.models import Prefetch, Subquery, OuterRef, DateField, Q
from clients.models import Client
from dashboard.services.dashboard_service import DashboardService


class DashboardView(LoginRequiredMixin, View):
    template_name = "dashboard/home.html"

    def get(self, request):
        query = request.GET.get("q", "").strip()
        clients = DashboardService.get_filtered_clients(query)
        page_obj = Paginator(clients, 20).get_page(request.GET.get("page"))
        return render(request, self.template_name, {"page_obj": page_obj, "query": query})
                 
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return render(request, self.template_name, {"error": "Debes subir un archivo."})
        
        if file.size > 5 * 1024 * 1024:
            return render(request, self.template_name, {"error": "Archivo inválido o demasiado grande."})
        try: 
                nuevos, duplicados = DashboardService.process_file(file)
                messages.success(request, f"{nuevos} clientes cargados. {duplicados} ya existían.")
                return redirect("default-dashboard")

        except Exception as e:
            return render(request, self.template_name, {"error": str(e)})
        
        
class ReportRequestView(LoginRequiredMixin, View):
    template_name = "dashboard/report_form.html"

    def get(self, request):
        form = ReportForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ReportForm(request.POST)
        if form.is_valid():
            selected_columns = form.cleaned_data['columns']
            enqueue(generate_report_and_send_email, request.user.email, selected_columns)
            messages.success(request, "Tu reporte está siendo generado. Recibirás un correo en breve.")
            return redirect("default-dashboard")
        return render(request, self.template_name, {"form": form})