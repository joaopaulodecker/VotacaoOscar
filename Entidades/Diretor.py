from Entidades.PessoaAbstract import PessoaAbstract
from Entidades.Nacionalidade import Nacionalidade


class Diretor(PessoaAbstract):

    def __init__(
        self,
        nome: str,
        data_nascimento: int,
        nacionalidade: Nacionalidade
    ):
        super().__init__(nome, data_nascimento, nacionalidade)
