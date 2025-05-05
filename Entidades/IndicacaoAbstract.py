from __future__ import annotations
from abc import ABC, abstractmethod
from Entidades.MembroAcademia import MembroAcademia
import Entidades.Categoria  # lazy import para evitar import circular

class Indicacao(ABC):
    def __init__(self, categoria: Entidades.Categoria.Categoria, membro_indicador: MembroAcademia):
        self.__categoria = categoria
        self.__membro_indicador = membro_indicador
        self.__categoria.adicionar_indicacao(self)

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria):
        self.__categoria = categoria

    @property
    def membro_indicador(self):
        return self.__membro_indicador

    @membro_indicador.setter
    def membro_indicador(self, membro_indicador):
        self.__membro_indicador = membro_indicador

    @abstractmethod
    def indicar(self):
        pass
