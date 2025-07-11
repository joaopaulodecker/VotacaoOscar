from Entidades.IndicacaoAbstract import IndicacaoAbstract
from Entidades.Categoria import Categoria
from Entidades.Diretor import Diretor

class IndDiretor(IndicacaoAbstract):
    def __init__(self, id_indicacao: int, membro_id: int, categoria: Categoria, diretor_indicado: Diretor):
        super().__init__(id_indicacao, membro_id, categoria, "diretor")
        self.__item_indicado = diretor_indicado

    @property
    def item_indicado(self) -> Diretor:
        return self.__item_indicado

    @property
    def item_indicado_id(self):
        return self.item_indicado.id

    def obter_detalhes_item_indicado(self) -> str:
        return f"Diretor(a): {self.item_indicado.nome}"