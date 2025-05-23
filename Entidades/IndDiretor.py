from Entidades.IndicacaoAbstract import IndicacaoAbstract
from Entidades.Categoria import Categoria

class IndDiretor(IndicacaoAbstract):
    def __init__(self, id_indicacao: int, membro_id: int, categoria: Categoria, diretor_indicado: dict):
        if not isinstance(diretor_indicado, dict) or 'id' not in diretor_indicado or 'nome' not in diretor_indicado:
            raise TypeError("diretor_indicado deve ser um dicionário contendo 'id' e 'nome'.")

        super().__init__(
            id_indicacao=id_indicacao,
            membro_id=membro_id,
            categoria=categoria,
            item_indicado_id=diretor_indicado.get('id'),
            tipo_item_indicado="diretor"
        )
        self.__item_indicado = diretor_indicado

    @property
    def item_indicado(self) -> dict:
        return self.__item_indicado

    @item_indicado.setter
    def item_indicado(self, diretor_indicado: dict):
        if not isinstance(diretor_indicado, dict) or 'id' not in diretor_indicado or 'nome' not in diretor_indicado:
            raise TypeError("diretor_indicado deve ser um dicionário contendo 'id' e 'nome'.")
        self.__item_indicado = diretor_indicado

    def obter_detalhes_item_indicado(self) -> str:
        if self.item_indicado and self.item_indicado.get('nome'):
            return f"Diretor: {self.item_indicado.get('nome')}"
        elif self.item_indicado and self.item_indicado.get('id'):
            return f"Diretor ID: {self.item_indicado.get('id')}"
        return "Diretor não especificado."