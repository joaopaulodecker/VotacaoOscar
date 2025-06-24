from DAOs.dao import DAO

class IndicacaoDAO(DAO):
    def __init__(self):
        super().__init__('indicacoes.pkl')

    def add(self, indicacao):
        if hasattr(indicacao, 'id_indicacao') and (indicacao.id_indicacao is not None):
            super().add(indicacao.id_indicacao, indicacao)

    def get(self, key: int):
        return super().get(key)

    def remove(self, key: int):
        return super().remove(key)