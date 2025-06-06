from django import forms
from contracts.models import Contract
from clients.models import Client
from vehicles.models import Vehicle
from django.db.models import Q

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['client', 'vehicle', 'billing_cycle', 'amount', 'start_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['client'].queryset = Client.objects.exclude(contracts__active=True)
    
        self.fields['vehicle'].queryset = Vehicle.objects.exclude(contracts__active=True)

        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})
