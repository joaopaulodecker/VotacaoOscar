from DAOs.Dao import DAO
from Entidades.Voto import Voto

class VotoDAO(DAO):
    """DAO específico para a persistência dos Votos."""
    def __init__(self):
        # Garante que os dados sejam salvos no arquivo 'votos.pkl'
        super().__init__('votos.pkl')

    def add(self, key: int, voto: Voto):
        """Adiciona um voto ao cache, validando o tipo do objeto."""
        if voto is not None and isinstance(voto, Voto):
            super().add(key, voto)

    def get(self, key: int):
        """Busca um voto pelo seu ID (chave)."""
        return super().get(key)

    def remove(self, key: int):
        """Remove um voto pelo seu ID (chave)."""
        return super().remove(key)