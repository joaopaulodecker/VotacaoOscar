from __future__ import annotations
from datetime import date
from Entidades.MembroAcademia import MembroAcademia
import Entidades.Categoria  # lazy import

class Voto:
    def __init__(self, membro_votante: MembroAcademia, categoria: Entidades.Categoria.Categoria, data_voto: date):
        self.__membro_votante = membro_votante
        self.__categoria = categoria
        self.__data_voto = data_voto
        self.__categoria.adicionar_voto(self)

    @property
    def membro_votante(self):
        return self.__membro_votante

    @membro_votante.setter
    def membro_votante(self, membro_votante):
        self.__membro_votante = membro_votante

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria):
        self.__categoria = categoria

    @property
    def data_voto(self):
        return self.__data_voto

    @data_voto.setter
    def data_voto(self, data_voto):
        self.__data_voto = data_voto
