from abc import ABC, abstractmethod
from MembroAcademia import MembroAcademia
from Categoria import Categoria

class Indicacao(ABC):
    def __init__(self, categoria: Categoria, membro_indicador: MembroAcademia):
        if isinstance(categoria, Categoria):
            self.__categoria = categoria
        if isinstance(membro_indicador, MembroAcademia):
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