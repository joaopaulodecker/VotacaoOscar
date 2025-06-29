from DAOs.Dao import DAO
from Entidades.Categoria import Categoria

class CategoriaDAO(DAO):
    """DAO específico para a persistência das Categorias."""
    def __init__(self):
        super().__init__('categorias.pkl')

    def add(self, key: int, categoria: Categoria):
        """Adiciona uma categoria ao cache, validando o tipo do objeto."""
        if categoria is not None and isinstance(categoria, Categoria):
            super().add(key, categoria)

    def get(self, key: int):
        """Busca uma categoria pelo seu ID (chave)."""
        return super().get(key)

    def remove(self, key: int):
        """Remove uma categoria pelo seu ID (chave)."""
        return super().remove(key)