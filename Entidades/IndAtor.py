from Entidades.IndicacaoAbstract import IndicacaoAbstract
from Entidades.Categoria import Categoria


class IndAtor(IndicacaoAbstract):
    def __init__(self, id_indicacao: int, membro_id: int, categoria: Categoria, ator_indicado: dict):
        if not isinstance(ator_indicado, dict) or 'id' not in ator_indicado or 'nome' not in ator_indicado:
            raise TypeError("ator_indicado deve ser um dicionário contendo 'id' e 'nome'.")

        super().__init__(
            id_indicacao=id_indicacao,
            membro_id=membro_id,
            categoria=categoria,
            item_indicado_id=ator_indicado.get('id'),
            tipo_item_indicado="ator"
        )
        self.__item_indicado = ator_indicado

    @property
    def item_indicado(self) -> dict:
        return self.__item_indicado

    @item_indicado.setter
    def item_indicado(self, ator_indicado: dict):
        if not isinstance(ator_indicado, dict) or 'id' not in ator_indicado or 'nome' not in ator_indicado:
            raise TypeError("ator_indicado deve ser um dicionário contendo 'id' e 'nome'.")
        self.__item_indicado = ator_indicado

    def obter_detalhes_item_indicado(self) -> str:
        if self.item_indicado and self.item_indicado.get('nome'):
            return f"Ator/Atriz: {self.item_indicado.get('nome')}"
        elif self.item_indicado and self.item_indicado.get('id'):
            return f"Ator/Atriz ID: {self.item_indicado.get('id')}"
        return "Ator/Atriz não especificado."