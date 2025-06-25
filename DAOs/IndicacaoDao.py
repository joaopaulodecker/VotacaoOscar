from DAOs.Dao import DAO
from Entidades.IndicacaoAbstract import IndicacaoAbstract


class IndicacaoDAO(DAO):
    """DAO responsável por toda a persistência de dados das Indicações."""

    def __init__(self):
        super().__init__('indicacoes.pkl')

    def add(self, key: int, indicacao: IndicacaoAbstract):
        """Adiciona uma nova indicação ao arquivo, após validar o objeto."""
        if (indicacao is not None and isinstance(indicacao, IndicacaoAbstract)
                and hasattr(indicacao, 'id_indicacao')):
            # Chama o 'add' do pai para fazer o trabalho pesado
            super().add(key, indicacao)

    def get(self, key: int):
        """Busca uma indicação específica no arquivo pelo seu ID."""
        if isinstance(key, int):
            return super().get(key)
        return None

    def remove(self, key: int):
        """Remove uma indicação do arquivo usando seu ID."""
        if isinstance(key, int):
            return super().remove(key)