from abc import ABC
from datetime import date
from Nacionalidade import Nacionalidade

class PessoaAbstract(ABC):
    def __init__(self, nome: str, data_nascimento: date, nacionalidade: Nacionalidade):
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        if isinstance(nacionalidade, Nacionalidade):
            self.__nacionalidade = nacionalidade

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def data_nascimento(self):
        return self.__data_nascimento
    
    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self.__data_nascimento = data_nascimento

    @property
    def nacionalidade(self):
        return self.__nacionalidade
    
    @nacionalidade.setter
    def nacionalidade(self, nacionalidade):
        self.__nacionalidade = nacionalidade
