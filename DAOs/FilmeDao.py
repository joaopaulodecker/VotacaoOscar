# Em DAOs/FilmeDao.py
from DAOs.Dao import DAO
from Entidades.Filme import Filme

class FilmeDAO(DAO):
    """DAO específico para a persistência dos Filmes."""
    def __init__(self):
        super().__init__('filmes.pkl')

    def add(self, key: int, filme: Filme):
        """Adiciona um filme ao cache, validando o tipo do objeto."""
        if filme is not None and isinstance(filme, Filme):
            super().add(key, filme)

    def get(self, key: int):
        """Busca um filme pelo seu ID (chave)."""
        return super().get(key)

    def remove(self, key: int):
        """Remove um filme pelo seu ID (chave)."""
        return super().remove(key)