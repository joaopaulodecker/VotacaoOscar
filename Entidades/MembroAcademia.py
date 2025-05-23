from Entidades.PessoaAbstract import PessoaAbstract
from Entidades.Nacionalidade import Nacionalidade
from datetime import date

class MembroAcademia(PessoaAbstract):
    def __init__(
        self,
        id_membro: int,
        nome: str,
        data_nascimento: date,
        nacionalidade: Nacionalidade,
        funcao: str
    ):
        super().__init__(nome, data_nascimento, nacionalidade)
        self.__id_membro = id_membro
        self.__funcao = funcao

    @property
    def id(self) -> int:
        return self.__id_membro

    @id.setter
    def id(self, id_membro: int):
        if not isinstance(id_membro, int):
            raise TypeError("ID do membro deve ser um inteiro.")
        self.__id_membro = id_membro

    @property
    def funcao(self) -> str:
        return self.__funcao

    @funcao.setter
    def funcao(self, funcao: str):
        self.__funcao = funcao

    def __str__(self) -> str:
        return f"ID Membro: {self.id}, Nome: {self.nome}, Nascimento: {self.data_nascimento}, Nacionalidade: {self.nacionalidade.nome if self.nacionalidade else 'N/A'}, Função: {self.funcao}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, MembroAcademia):
            return NotImplemented
        return self.id == other.id
