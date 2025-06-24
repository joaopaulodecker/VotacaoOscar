from DAOs.dao import DAO
from Entidades.Categoria import Categoria


class CategoriaDAO(DAO):

    def __init__(self):
        super().__init__('categorias.pkl')

    def add(self, categoria: Categoria):
        if isinstance(categoria, Categoria) and hasattr(categoria, 'id'):
            super().add(categoria)

    def get(self, key: int):
        if isinstance(key, int):
            for categoria in self.get_all():
                if categoria.id == key:
                    return categoria
        return None

    def remove(self, key: int):
        if isinstance(key, int):
            lista_completa = self.get_all()
            nova_lista = [categoria for categoria in lista_completa if categoria.id != key]
            self._DAO__dump(nova_lista)

