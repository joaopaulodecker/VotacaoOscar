from DAOs.dao import DAO
from Entidades.Filme import Filme


class FilmeDAO(DAO):

    def __init__(self):
        super().__init__('filmes.pkl')

    def add(self, filme: Filme):
        if isinstance(filme, Filme):
            super().add(filme)

    def get(self, key: int):
        if isinstance(key, int):
            for filme in self.get_all():
                if filme.id_filme == key:
                    return filme
        return None

    def remove(self, key: int):
        if isinstance(key, int):
            lista_completa = self.get_all()
            nova_lista = [filme for filme in lista_completa if filme.id_filme != key]
            self._DAO__dump(nova_lista)

