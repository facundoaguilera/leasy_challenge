from datetime import date
from cobranzas.repositories.contract_repository import ContractRepository

class ContractService:
    @staticmethod
    def get_contracts_with_extra_data():
        contracts = ContractRepository.get_active_contracts_with_annotations()
        for contract in contracts:
            fecha = contract.fecha_mas_antigua
            if fecha and date.today() > fecha:
                contract.dias_desde_mas_antigua = (date.today() - fecha).days
            else:
                contract.dias_desde_mas_antigua = 0
        return contracts
