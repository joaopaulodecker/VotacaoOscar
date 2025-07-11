from abc import ABC, abstractmethod
from Entidades.Categoria import Categoria

class IndicacaoAbstract(ABC):
    """Molde para qualquer Indicação. Sabe QUEM indicou e O QUÊ foi indicado."""
    def __init__(self, id_indicacao: int, membro_id: int, categoria: Categoria, tipo_item_indicado: str):
        self.__id_indicacao = id_indicacao
        self.__membro_id = membro_id
        self.__categoria = categoria
        # O tipo agora é definido corretamente no nascimento do objeto.
        self.__tipo_item_indicado = tipo_item_indicado

    @property
    def id_indicacao(self) -> int:
        return self.__id_indicacao

    @property
    def membro_id(self) -> int:
        return self.__membro_id

    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    @property
    def tipo_indicacao(self) -> str:
        # Lê a informação que foi salva no construtor.
        return self.__tipo_item_indicado

    @property
    @abstractmethod
    def item_indicado_id(self):
        """Propriedade abstrata para o ID do item indicado (filme, ator, etc)."""
        pass

    @abstractmethod
    def obter_detalhes_item_indicado(self) -> str:
        """Método abstrato para retornar uma string com os detalhes do item indicado."""
        pass