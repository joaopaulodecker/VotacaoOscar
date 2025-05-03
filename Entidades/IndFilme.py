from IndicacaoAbstract import Indicacao
from Filme import Filme
from Categoria import Categoria
from MembroAcademia import MembroAcademia

class IndFilme(Indicacao):
    def __init__(self, filme: Filme, categoria: Categoria, membro_indicador: MembroAcademia):
        super().__init__(categoria, membro_indicador)
        if isinstance(filme, Filme):
            self.__filme = filme

    @property
    def filme(self):
        return self.__filme
    
    @filme.setter
    def filme(self, filme):
        self.__filme = filme

    def indicar(self) -> str:
        return f"Filme '{self.filme.titulo}' indicado por {self.membro_indicador.nome} na categoria '{self.categoria.nome}'."