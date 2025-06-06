from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

from contracts.models import Contract
from invoices.models import Invoice


class Command(BaseCommand):
    help = "Genera invoices para contratos activos si aún no fueron generadas en el período actual."

    def handle(self, *args, **options):
        hoy = date.today()
        generadas = 0

        for contract in Contract.objects.filter(active=True):
            #period_start = self.get_next_period_start(contract)
            start_dates = self.get_next_period_start(contract)
            
            for period_start in start_dates:
                due_date = self.get_due_date(period_start, contract.billing_cycle)
          
                Invoice.objects.create(
                    contract=contract,
                    period_start=period_start,
                    issue_date=hoy,
                    due_date=due_date,
                    amount=contract.amount,
                    paid=False
                )
                generadas += 1
                self.stdout.write(self.style.SUCCESS(f"Invoice creada para contrato {contract.id} - Periodo: {period_start}"))

            self.stdout.write(self.style.SUCCESS(f"Total de invoices generadas: {generadas}"))

    def get_next_period_start(self, contract):
        """
        Itera desde el start_date del contrato hasta hoy y devuelve el primer período
        para el cual no existe una invoice.
        """
        current = contract.start_date
        today = date.today()

        delta = {
            'weekly': timedelta(weeks=1),
            'biweekly': timedelta(weeks=2),
            'monthly': relativedelta(months=1),
        }[contract.billing_cycle]
        start_dates = []
        while current <= today:
            existe = Invoice.objects.filter(contract=contract, period_start=current).exists()
            if not existe:
                start_dates.append(current)
            current += delta
                
        return start_dates
            

    def get_due_date(self, period_start, billing_cycle):
        """
        Calcula la fecha de vencimiento como el último día del período según el ciclo.
        """
        if billing_cycle == 'weekly':
            return period_start + timedelta(days=6)
        elif billing_cycle == 'biweekly':
            return period_start + timedelta(days=13)
        elif billing_cycle == 'monthly':
            return period_start + relativedelta(months=1) - timedelta(days=1)
        return period_start

