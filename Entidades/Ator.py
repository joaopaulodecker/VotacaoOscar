from pandas.core.window.online import generate_online_numba_ewma_func

from Entidades.PessoaAbstract import PessoaAbstract
from Entidades.Nacionalidade import Nacionalidade


class Ator(PessoaAbstract):

    def __init__(
        self,
        nome: str,
        data_nascimento: int,
        nacionalidade: Nacionalidade, genero: str
    ):
        super().__init__(nome, data_nascimento, nacionalidade)
        self.__genero = genero

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, genero: str):
        self.__genero = genero
