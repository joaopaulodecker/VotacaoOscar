from Entidades.IndicacaoAbstract import IndicacaoAbstract
from Entidades.Categoria import Categoria
from Entidades.Ator import Ator


class IndAtor(IndicacaoAbstract):
    def __init__(self, id_indicacao: int, membro_id: int, categoria: Categoria, ator_indicado: Ator):
        # A lógica inteligente foi movida para o __init__.
        tipo_correto = "atriz" if ator_indicado.genero_artistico == 'Atriz' else "ator"

        super().__init__(id_indicacao, membro_id, categoria, tipo_correto)
        self.__item_indicado = ator_indicado

    @property
    def item_indicado(self) -> Ator:


        return self.__item_indicado

    @property
    def item_indicado_id(self):
        return self.item_indicado.id

    def obter_detalhes_item_indicado(self) -> str:
        return f"Ator/Atriz: {self.item_indicado.nome}"