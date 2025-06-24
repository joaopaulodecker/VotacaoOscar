from __future__ import annotations
import Entidades.Categoria

class Voto:
    def __init__(self, id_voto: int, membro_id: int, categoria: Entidades.Categoria.Categoria, item_indicado_id: any, tipo_item_indicado: str):
        self.__id_voto = id_voto
        self.__membro_id = membro_id
        self.__categoria = categoria
        self.__item_indicado_id = item_indicado_id
        self.__tipo_item_indicado = tipo_item_indicado
    @property
    def id_voto(self) -> int:
        return self.__id_voto

    @property
    def membro_id(self) -> int:
        return self.__membro_id

    @membro_id.setter
    def membro_id(self, membro_id: int):
        self.__membro_id = membro_id

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria: Entidades.Categoria.Categoria):
        self.__categoria = categoria

    @property
    def item_indicado_id(self) -> any:
        return self.__item_indicado_id

    @property
    def tipo_item_indicado(self) -> str:
        return self.__tipo_item_indicado