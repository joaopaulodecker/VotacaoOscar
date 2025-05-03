from IndicacaoAbstract import Indicacao
from Diretor import Diretor
from Categoria import Categoria
from MembroAcademia import MembroAcademia

class IndDiretor(Indicacao):
    def __init__(self, diretor: Diretor, categoria: Categoria, membro_indicador: MembroAcademia):
        super().__init__(categoria, membro_indicador)
        if isinstance(diretor, Diretor):
            self.__diretor = diretor

    @property
    def diretor(self):
        return self.__filme
    
    @diretor.setter
    def diretor(self, diretor):
        self.__diretor = diretor

    def indicar(self) -> str:
        return f"Diretor '{self.diretor.nome}' indicado por {self.membro_indicador.nome} na categoria '{self.categoria.nome}'."