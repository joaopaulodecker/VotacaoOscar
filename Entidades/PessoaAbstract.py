from abc import ABC
from Entidades.Nacionalidade import Nacionalidade

class PessoaAbstract(ABC):
    def __init__(
        self,
        nome: str,
        data_nascimento: int,
        nacionalidade: Nacionalidade
    ):
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__nacionalidade = nacionalidade

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def data_nascimento(self) -> int:
        return self.__data_nascimento
    
    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: int):
        self.__data_nascimento = data_nascimento

    @property
    def nacionalidade(self) -> Nacionalidade:
        return self.__nacionalidade
    
    @nacionalidade.setter
    def nacionalidade(self, nacionalidade: Nacionalidade):
        self.__nacionalidade = nacionalidade
