from Entidades.IndicacaoAbstract import Indicacao
from Entidades.Ator import Ator
from Entidades.Categoria import Categoria
from Entidades.MembroAcademia import MembroAcademia


class IndAtor(Indicacao):

    def __init__(
        self,
        ator: Ator,
        categoria: Categoria,
        membro_indicador: MembroAcademia
    ):
        super().__init__(categoria, membro_indicador)
        if isinstance(ator, Ator):
            self.__ator = ator

    @property
    def ator(self):
        return self.__ator

    @ator.setter
    def ator(self, ator):
        self.__ator = ator

    def indicar(self) -> str:
        return (
            f"Ator '{self.ator.nome}' indicado por "
            f"{self.membro_indicador.nome} na categoria "
            f"'{self.categoria.nome}'."
        )
