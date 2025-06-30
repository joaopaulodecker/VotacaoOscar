from Entidades.IndicacaoAbstract import IndicacaoAbstract
from Entidades.Categoria import Categoria
from Entidades.Ator import Ator

class IndAtor(IndicacaoAbstract):
    def __init__(self, id_indicacao: int, categoria: Categoria, membro_id: int, ator_indicado: Ator):
        super().__init__(
            id_indicacao=id_indicacao,
            categoria=categoria,
            item_indicado_id=ator_indicado.id,
            tipo_item_indicado="ator",
            membro_id=membro_id
        )
        self.__item_indicado = ator_indicado
        if not isinstance(ator_indicado, Ator):
            raise TypeError("ator_indicado deve ser uma instância da classe Ator.")
        self.__item_indicado = ator_indicado

    @property
    def item_indicado(self) -> Ator:
        return self.__item_indicado

    @item_indicado.setter
    def item_indicado(self, ator_indicado: Ator):
        if not isinstance(ator_indicado, Ator):
            raise TypeError("ator_indicado deve ser uma instância da classe Ator.")
        self.__item_indicado = ator_indicado

    def obter_detalhes_item_indicado(self) -> str:
        if self.item_indicado and self.item_indicado.nome:
            return f"Ator/Atriz: {self.item_indicado.nome}"
        elif self.item_indicado and self.item_indicado.id:
            return f"Ator/Atriz ID: {self.item_indicado.id}"
        return "Ator/Atriz não especificado."