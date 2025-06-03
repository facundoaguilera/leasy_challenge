from django import forms

COLUMN_CHOICES = [
    # Campos del modelo Client
    ('first_name', 'Nombre'),
    ('last_name', 'Apellido'),
    ('document_number', 'Documento'),

    # Campos del modelo Contract (relación: contract)
    ('contract__start_date', 'Inicio del Contrato'),
    ('contract__billing_cycle', 'Ciclo de Facturación'),
    ('contract__amount', 'Monto del Contrato'),

    # Campos del modelo Vehicle (relación: contract → vehicle)
    ('contract__vehicle__brand', 'Marca del Vehículo'),
    ('contract__vehicle__model', 'Modelo del Vehículo'),
    ('contract__vehicle__plate', 'Placa'),
    ('contract__vehicle__vin', 'VIN'),
]

class ReportForm(forms.Form):
    columns = forms.MultipleChoiceField(
        choices=COLUMN_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecciona las columnas para el reporte"
    )
