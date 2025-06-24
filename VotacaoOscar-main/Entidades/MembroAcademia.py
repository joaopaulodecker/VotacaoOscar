from Entidades.PessoaAbstract import PessoaAbstract
from Entidades.Nacionalidade import Nacionalidade

class MembroAcademia(PessoaAbstract):
    def __init__(
        self,
        id_: int,
        nome: str,
        data_nascimento: int,
        nacionalidade: Nacionalidade,
        funcao: str
    ):
        super().__init__(id_, nome, data_nascimento, nacionalidade)
        self.__funcao = funcao


    @property
    def funcao(self) -> str:
        return self.__funcao

    @funcao.setter
    def funcao(self, funcao: str):
        self.__funcao = funcao


    def get_info_str(self) -> str:
        return f"Nome: {self.nome}, Função: {self.funcao.capitalize()}"

