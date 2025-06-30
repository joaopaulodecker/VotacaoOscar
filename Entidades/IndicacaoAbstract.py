from __future__ import annotations
from abc import ABC, abstractmethod
import Entidades.Categoria

class IndicacaoAbstract(ABC):
    def __init__(self, id_indicacao: int, categoria: Entidades.Categoria.Categoria, item_indicado_id: any, membro_id: int, tipo_item_indicado: str):
        self.__id_indicacao = id_indicacao
        self.__categoria = categoria
        self.__item_indicado_id = item_indicado_id
        self.__tipo_item_indicado = tipo_item_indicado
        self.__membro_id = membro_id

    @property
    def id_indicacao(self) -> int:
        return self.__id_indicacao
    
    @id_indicacao.setter
    def id_indicacao(self, id_indicacao: int):
        self.__id_indicacao = id_indicacao
    
    @property
    def categoria(self) -> Entidades.Categoria.Categoria:
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria: Entidades.Categoria.Categoria):
        self.__categoria = categoria

    @property
    def item_indicado_id(self) -> any:
        return self.__item_indicado_id

    @property
    def membro_id(self) -> int:
        return self.__membro_id

    @property
    def tipo_item_indicado(self) -> str:
        return self.__tipo_item_indicado

    @abstractmethod
    def obter_detalhes_item_indicado(self) -> str:
        pass
