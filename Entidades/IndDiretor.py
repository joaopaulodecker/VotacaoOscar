from Entidades.IndicacaoAbstract import Indicacao
from Entidades.Diretor import Diretor
from Entidades.Categoria import Categoria
from Entidades.MembroAcademia import MembroAcademia


class IndDiretor(Indicacao):

    def __init__(
        self,
        diretor: Diretor,
        categoria: Categoria,
        membro_indicador: MembroAcademia
    ):
        super().__init__(categoria, membro_indicador)
        if isinstance(diretor, Diretor):
            self.__diretor = diretor

    @property
    def diretor(self):
        return self.__diretor

    @diretor.setter
    def diretor(self, diretor):
        self.__diretor = diretor

    def indicar(self) -> str:
        return (
            f"Diretor '{self.diretor.nome}' indicado por "
            f"{self.membro_indicador.nome} na categoria "
            f"'{self.categoria.nome}'."
        )
