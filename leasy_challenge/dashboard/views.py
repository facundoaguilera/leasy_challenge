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
from django.views.generic import ListView

REQUIRED_COLUMNS = [
    "Nombres",
    "Apellidos",
    "Número de documento",
    "Inicio de contrato",
    "Cuota semanal",
    "Marca del auto",
    "Modelo del auto",
    "Placa del auto"
]

class DashboardView(LoginRequiredMixin, View):
    template_name = "dashboard/home.html"

    def get(self, request):
        query = request.GET.get("q", "").strip()

        latest_contract = Contract.objects.filter(
            client=OuterRef("pk")
        ).order_by('-active', '-start_date')

        clients = Client.objects.annotate(
            latest_contract_id=Subquery(latest_contract.values("id")[:1])
        ).prefetch_related(
            Prefetch("contracts", queryset=Contract.objects.select_related("vehicle"), to_attr="all_contracts")
        ).order_by("last_name", "first_name")

        if query:
            clients = clients.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(document_number__icontains=query) |
                Q(contracts__vehicle__brand__icontains=query) |
                Q(contracts__vehicle__model__icontains=query) |
                Q(contracts__vehicle__plate__icontains=query)
            ).distinct()

        paginator = Paginator(clients, 20)
        page_obj = paginator.get_page(request.GET.get("page"))

        context = {
            "page_obj": page_obj,
            "query": query,
        }
        return render(request, self.template_name, context)

         
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return render(request, self.template_name, {"error": "Debes subir un archivo."})

        if not file.name.endswith(".csv"):
            return render(request, self.template_name, {"error": "Solo se permiten archivos .csv por ahora."})

        if file.size > 5 * 1024 * 1024:
            return render(request, self.template_name, {"error": "El archivo excede los 5 MB. Usa carga por lotes."})

        try:
            decoded_file = file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            headers = reader.fieldnames

            missing = [col for col in REQUIRED_COLUMNS if col not in headers]
            if missing:
                return render(request, self.template_name, {
                    "error": f"Faltan columnas requeridas: {', '.join(missing)}"
                })

            nuevos = 0
            duplicados = 0
            for row in reader:
                doc = row["Número de documento"]

                # Cliente
                client, created = Client.objects.get_or_create(
                    document_number=doc,
                    defaults={
                        "first_name": row["Nombres"],
                        "last_name": row["Apellidos"]
                    }
                )
                if created:
                    nuevos += 1
                else:
                    duplicados += 1

                # Vehículo
                plate = row["Placa del auto"]
                vehicle, _ = Vehicle.objects.get_or_create(
                    plate=plate,
                    defaults={
                        "brand": row["Marca del auto"],
                        "model": row["Modelo del auto"],
                        "vin": row.get("VIN") or None,
                    }
                )

                # Contrato
                if not Contract.objects.filter(client=client).exists() and row["Inicio de contrato"]:
                    # Detectar ciclo
                    ciclo = "weekly"  # si viniera una columna ciclo seria ciclo = row["ciclo"]
                    
                    for h in headers:
                        h_lower = h.lower()
                        if "cuota" in h_lower:
                            if "semanal" in h_lower:
                                ciclo = "weekly"
                                break
                            elif "quincenal" in h_lower:
                                ciclo = "biweekly"
                                break
                            elif "mensual" in h_lower:
                                ciclo = "monthly"
                                break
                            
                    fecha_inicio = parse_date(row["Inicio de contrato"])

                    monto = (
                        row.get("Cuota semanal") or
                        row.get("Cuota quincenal") or
                        row.get("Cuota mensual")
                    )
                    #active = row["activo"] si viniera una una columna activo
                    active = True #default
                    Contract.objects.create(
                        client=client,
                        vehicle=vehicle,
                        billing_cycle=ciclo,
                        amount=monto,
                        start_date=fecha_inicio,
                        active= active
                    )

            messages.success(request, f"{nuevos} clientes cargados. {duplicados} ya existían.")

            return redirect("default-dashboard")

        except Exception as e:
                return render(request, self.template_name, {
                            "error": f"Ocurrió un error procesando el archivo: {str(e)}"
                        })
        
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