from DAOs.Dao import DAO
from Entidades.IndicacaoAbstract import IndicacaoAbstract


class IndicacaoDAO(DAO):
    """DAO específico para a persistência das Indicações."""
    def __init__(self):
        super().__init__('indicacoes.pkl')

    def add(self, key: int, indicacao: IndicacaoAbstract):
        """Adiciona uma indicação ao cache, validando o tipo do objeto."""
        if indicacao is not None and isinstance(indicacao, IndicacaoAbstract):
            super().add(key, indicacao)

    def get(self, key: int):
        """Busca uma indicação pelo seu ID (chave)."""
        return super().get(key)

    def remove(self, key: int):
        """Remove uma indicação do arquivo usando seu ID."""
        return super().remove(key)