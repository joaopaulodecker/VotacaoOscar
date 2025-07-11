from Entidades.IndicacaoAbstract import IndicacaoAbstract
from Entidades.Categoria import Categoria
from Entidades.Filme import Filme

class IndFilme(IndicacaoAbstract):
    def __init__(self, id_indicacao: int, membro_id: int, categoria: Categoria, filme_indicado: Filme):
        super().__init__(id_indicacao, membro_id, categoria, "filme")
        self.__item_indicado = filme_indicado

    @property
    def item_indicado(self) -> Filme:
        return self.__item_indicado

    @property
    def item_indicado_id(self):
        return self.item_indicado.id_filme

    def obter_detalhes_item_indicado(self) -> str:
        return f"Filme: {self.item_indicado.titulo}"