from PessoaAbstract import PessoaAbstract
from Nacionalidade import Nacionalidade
from datetime import date

class MembroAcademia(PessoaAbstract):
    def __init__(self, nome: str, data_nascimento: date, nacionalidade: Nacionalidade, id_membro: int, profissao: str):
        super().__init__(nome, data_nascimento, nacionalidade)
        if isinstance(id_membro, int):
            self.__id_membro = id_membro
        self.__profissao = profissao

    @property
    def id_membro(self):
        return self.__id_membro

    @id_membro.setter
    def id_membro(self, id_membro):
        self.__id_membro = id_membro

    @property
    def profissao(self):
        return self.__profissao

    @profissao.setter
    def profissao(self, profissao):
        self.__profissao = profissao
