from IndicacaoAbstract import Indicacao
from Voto import Voto

class Categoria:
    def __init__(self, nome: str):
        self.nome = nome
        self.__indicacoes = []
        self.__votos = []

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def indicacoes(self):
        return self.__indicacoes

    @property
    def votos(self):
        return self.__votos

    def adicionar_indicacao(self, indicacao):
        if isinstance(indicacao, Indicacao):
            self.__indicacoes.append(indicacao)

    def adicionar_voto(self, voto):
        if isinstance(voto, Voto):
            self.__votos.append(voto)

    def total_de_indicacoes(self):
        return len(self.__indicacoes)

    def total_de_votos(self):
        return len(self.__votos)
