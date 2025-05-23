from abc import ABC, abstractmethod
from datetime import date
from Entidades.Nacionalidade import Nacionalidade

class PessoaAbstract(ABC):
    def __init__(
        self,
        id_pessoa: int,
        nome: str,
        data_nascimento: date,
        nacionalidade: Nacionalidade
    ):
        self.__id_pessoa = id_pessoa
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__nacionalidade = nacionalidade

    @property
    def id_pessoa(self) -> int:
        return self.__id_pessoa

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    # ... outras properties ...
