from abc import ABC, abstractmethod
from Entidades.Nacionalidade import Nacionalidade

class PessoaAbstract(ABC):
    """
        Representa o molde base para qualquer pessoa no sistema do Oscar.

        Esta classe é abstrata e não pode ser criada diretamente. Ela serve como
        um contrato, garantindo que todas as pessoas, sejam Atores, Diretores ou
        Membros da Academia, tenham atributos essenciais como ID, nome e
        nacionalidade.
        """

    def __init__(
        self, id_: int,
        nome: str,
        data_nascimento: int,
        nacionalidade: Nacionalidade
    ):
        self.__id = id_
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__nacionalidade = nacionalidade


    @property
    def id(self) -> int:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def data_nascimento(self) -> int:
        return self.__data_nascimento

    @property
    def nacionalidade(self) -> Nacionalidade:
        return self.__nacionalidade
    
    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: int):
        self.__data_nascimento = data_nascimento
    
    @nacionalidade.setter
    def nacionalidade(self, nacionalidade: Nacionalidade):
        self.__nacionalidade = nacionalidade

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @abstractmethod
    def get_info_str(self) -> str:
        """
        Um método de contrato. Força todas as classes filhas (Ator, Diretor)
        a implementarem sua própria maneira de se descrever como uma string.
        """
        pass
