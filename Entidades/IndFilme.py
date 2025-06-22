from Entidades.IndicacaoAbstract import IndicacaoAbstract
from Entidades.Filme import Filme
from Entidades.Categoria import Categoria

class IndFilme(IndicacaoAbstract):
    def __init__(self, id_indicacao: int, categoria: Categoria, filme_indicado: Filme):
        super().__init__(
            id_indicacao=id_indicacao,
            categoria=categoria,
            item_indicado_id=filme_indicado.id_filme,
            tipo_item_indicado="filme"
        )
        if not isinstance(filme_indicado, Filme):
            raise TypeError("item_indicado deve ser uma instância da classe Filme para IndFilme.")
        self.__item_indicado = filme_indicado

    @property
    def item_indicado(self) -> Filme:
        return self.__item_indicado

    @item_indicado.setter
    def item_indicado(self, filme_indicado: Filme):
        if not isinstance(filme_indicado, Filme):
            raise TypeError("item_indicado deve ser uma instância da classe Filme.")
        self.__item_indicado = filme_indicado

    def obter_detalhes_item_indicado(self) -> str:
        if self.item_indicado:
            return f"Filme: {self.item_indicado.titulo} (Ano: {self.item_indicado.ano})"
        return "Filme não especificado."

