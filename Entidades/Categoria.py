import Entidades.Voto
from Entidades.IndicacaoAbstract import IndicacaoAbstract

class Categoria:
    TIPOS_VALIDOS = ("ator", "diretor", "filme")

    def __init__(self, id_categoria: int, nome: str, tipo_indicacao: str):
        self.__tipo = tipo_indicacao.lower()
        if self.__tipo not in Categoria.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de indicação inválido: '{tipo_indicacao}'")
        self.__id = id_categoria
        self.__nome = nome
        self.__indicacoes = []
        self.__votos = []

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def indicacoes(self) -> list:
        return self.__indicacoes

    @property
    def votos(self) -> list:
        return self.__votos

    @property
    def tipo_indicacao(self) -> str:
        return self.__tipo

    def adicionar_indicacao(self, indicacao):
        if isinstance(indicacao, IndicacaoAbstract):
            self.__indicacoes.append(indicacao)

    def adicionar_voto(self, voto):
        if isinstance(voto, Entidades.Voto.Voto):
            self.__votos.append(voto)

    def total_de_indicacoes(self) -> int:
        return len(self.__indicacoes)

    def total_de_votos(self) -> int:
        return len(self.__votos)
