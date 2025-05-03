from PessoaAbstract import PessoaAbstract
from Nacionalidade import Nacionalidade
from datetime import date

class Diretor(PessoaAbstract):
    def __init__(self, nome, data_nascimento: date, nacionalidade: Nacionalidade):
        super().__init__(nome, data_nascimento, nacionalidade)