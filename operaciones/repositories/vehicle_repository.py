from vehicles.models import Vehicle
from django.db.models import Prefetch
from contracts.models import Contract

class VehicleRepository:
    @staticmethod
    def get_vehicles_with_contracts():
        return Vehicle.objects.prefetch_related(
            Prefetch('contracts', queryset=Contract.objects.all())
        ).order_by('brand')