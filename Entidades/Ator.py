
from Entidades.PessoaAbstract import PessoaAbstract
from Entidades.Nacionalidade import Nacionalidade


class Ator(PessoaAbstract):

    def __init__(
        self,
        nome: str,
        data_nascimento: int,
        nacionalidade: Nacionalidade, genero_artistico: str
    ):
        super().__init__(nome, data_nascimento, nacionalidade)
        if genero_artistico.capitalize() not in ["Ator", "Atriz"]:
            raise ValueError("Gênero artístico deve ser 'Ator' ou 'Atriz'.")
        self.__genero_artistico = genero_artistico.capitalize()


    @property
    def genero_artistico(self) -> str:
        return self.__genero_artistico

    @genero_artistico.setter
    def genero_artistico(self, genero: str):
        if genero.capitalize() not in ["Ator", "Atriz"]:
            raise ValueError("Gênero artístico deve ser 'Ator' ou 'Atriz'.")
        self.__genero_artistico = genero.capitalize()


    def get_info_str(self) -> str:
        """ Implementação do método abstrato da classe PessoaAbstract. """
        return f"Nome: {self.nome}, Gênero: {self.genero_artistico}"

