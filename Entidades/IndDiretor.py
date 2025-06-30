from Entidades.IndicacaoAbstract import IndicacaoAbstract
from Entidades.Categoria import Categoria
from Entidades.Diretor import Diretor

class IndDiretor(IndicacaoAbstract):
    def __init__(self, id_indicacao: int, categoria: Categoria, membro_id: int, diretor_indicado: Diretor):
        super().__init__(
            id_indicacao=id_indicacao,
            categoria=categoria,
            item_indicado_id=diretor_indicado.id,
            tipo_item_indicado="diretor",
            membro_id= membro_id
        )
        self.__item_indicado = diretor_indicado

        if not isinstance(diretor_indicado, Diretor):
            raise TypeError("diretor_indicado deve ser uma instância da classe Diretor.")
        self.__item_indicado = diretor_indicado

    @property
    def item_indicado(self) -> Diretor:
        return self.__item_indicado

    @item_indicado.setter
    def item_indicado(self, diretor_indicado: Diretor):
        if not isinstance(diretor_indicado, Diretor):
            raise TypeError("diretor_indicado deve ser uma instância da classe Diretor.")
        self.__item_indicado = diretor_indicado

    def obter_detalhes_item_indicado(self) -> str:
        if self.item_indicado and self.item_indicado.nome:
            return f"Diretor: {self.item_indicado.nome}"
        elif self.item_indicado and self.item_indicado.id:
            return f"Diretor ID: {self.item_indicado.id}"
        return "Diretor não especificado."