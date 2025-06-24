from Entidades.PessoaAbstract import PessoaAbstract
from Entidades.Nacionalidade import Nacionalidade


class Diretor(PessoaAbstract):

    def __init__(
        self, id_: int,
        nome: str,
        data_nascimento: int,
        nacionalidade: Nacionalidade
    ):
        super().__init__(id_, nome, data_nascimento, nacionalidade)


    def get_info_str(self) -> str:
        return f"Nome: {self.nome}"
