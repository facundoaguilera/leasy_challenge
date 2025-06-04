from django.db.models import OuterRef, Subquery, Q, Prefetch
from contracts.models import Contract
from clients.models import Client
from vehicles.models import Vehicle
import csv
from django.utils.dateparse import parse_date

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

class DashboardService:
    @staticmethod
    def get_filtered_clients(query=None):
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
        
        return clients
    
    @staticmethod
    def process_csv(file):
        decoded_file = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)
        headers = reader.fieldnames

        missing = [col for col in REQUIRED_COLUMNS if col not in headers]
        if missing:
            raise ValueError(f"Faltan columnas requeridas: {', '.join(missing)}")

        nuevos, duplicados = 0, 0
        for row in reader:
            doc = row["Número de documento"]

            client, created = Client.objects.get_or_create(
                document_number=doc,
                defaults={
                    "first_name": row["Nombres"],
                    "last_name": row["Apellidos"]
                }
            )
            nuevos += int(created)
            duplicados += int(not created)

            plate = row["Placa del auto"]
            vehicle, _ = Vehicle.objects.get_or_create(
                plate=plate,
                defaults={
                    "brand": row["Marca del auto"],
                    "model": row["Modelo del auto"],
                    "vin": row.get("VIN") or None,
                }
            )

            if not Contract.objects.filter(client=client).exists() and row["Inicio de contrato"]:
                ciclo = "weekly"
                for h in headers:
                    if "cuota" in h.lower():
                        if "semanal" in h.lower():
                            ciclo = "weekly"
                        elif "quincenal" in h.lower():
                            ciclo = "biweekly"
                        elif "mensual" in h.lower():
                            ciclo = "monthly"
                        break

                monto = row.get("Cuota semanal") or row.get("Cuota quincenal") or row.get("Cuota mensual")
                Contract.objects.create(
                    client=client,
                    vehicle=vehicle,
                    billing_cycle=ciclo,
                    amount=monto,
                    start_date=parse_date(row["Inicio de contrato"]),
                    active=True
                )
        return nuevos, duplicados