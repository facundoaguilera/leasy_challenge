from openpyxl import Workbook
from django.core.mail import EmailMessage
from django.db.models import OuterRef, Subquery
from contracts.models import Contract
from clients.models import Client
import tempfile, os
from .forms import COLUMN_CHOICES

def generate_report_and_send_email(email, selected_columns):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte de Clientes"

    # Títulos de columna legibles
    ws.append([dict(COLUMN_CHOICES).get(col, col.replace("__", " ").title()) for col in selected_columns])
    
    # Subquery para obtener contrato activo o más reciente
    latest_contract = Contract.objects.filter(
        client=OuterRef('pk')
    ).order_by('-active', '-start_date')

    clients = Client.objects.annotate(
        latest_contract_id=Subquery(latest_contract.values('id')[:1])
    )

    # Traer contratos y vehículos relacionados
    contracts = Contract.objects.select_related("vehicle", "client")
    contracts_by_id = {c.id: c for c in contracts}

    def resolve(obj, attr_path):
        for part in attr_path.split("__"):
            if obj is None:
                return ""
            obj = getattr(obj, part, "")
        return obj

    for client in clients:
        contract = contracts_by_id.get(client.latest_contract_id)

        row = []
        for col in selected_columns:
            if col.startswith("contract__"):
                row.append(resolve(contract, col.replace("contract__", "")))
            else:
                row.append(resolve(client, col))
            
        ws.append(row)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        wb.save(tmp.name)
        tmp_path = tmp.name

    # Enviar por email
    mail = EmailMessage(
        subject="Tu reporte de clientes",
        body="Adjunto encontrarás tu archivo Excel.",
        to=[email],
    )
    mail.attach_file(tmp_path)
    mail.send()
    os.remove(tmp_path)
