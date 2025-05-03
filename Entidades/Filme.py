from Diretor import Diretor
from Nacionalidade import Nacionalidade

class Filme:
    def __init__(self, titulo: str, diretor: Diretor, ano: int, nacionalidade: Nacionalidade):
        self.__titulo = titulo
        if isinstance(diretor, Diretor):
            self.__diretor = diretor
        if isinstance(ano, int):
            self.ano = ano

    @property
    def titulo(self):
        return self.__titulo
    
    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = titulo

    @property
    def diretor(self):
        return self.__diretor
    
    @diretor.setter
    def diretor(self, diretor):
        self.__diretor = diretor

    @property
    def ano(self):
        return self.__ano
    
    @ano.setter
    def ano(self, ano):
        self.__ano = ano

    @property
    def nacionalidade(self):
        return self.__nacionalidade
    
    @nacionalidade.setter
    def nacionalidade(self, nacionalidade):
        self.__nacionalidade = nacionalidade

