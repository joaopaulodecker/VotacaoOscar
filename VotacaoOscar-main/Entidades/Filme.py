from Entidades.Nacionalidade import Nacionalidade

class Filme:
    def __init__(self, id_filme: int, titulo: str, ano: int, diretor_id: int, nacionalidade: Nacionalidade):
        self.__id_filme = id_filme
        self.__titulo = titulo
        self.__ano = ano
        self.__diretor_id = diretor_id
        self.__nacionalidade = nacionalidade

    @property
    def id_filme(self) -> int:
        return self.__id_filme
    
    @id_filme.setter
    def id_filme(self, id_filme: int):
        self.__id_filme = id_filme

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo: str):
        self.__titulo = titulo

    @property
    def ano(self) -> int:
        return self.__ano

    @ano.setter
    def ano(self, ano: int):
        self.__ano = ano

    @property
    def diretor_id(self) -> int:
        return self.__diretor_id

    @diretor_id.setter
    def diretor_id(self, diretor_id: int):
        self.__diretor_id = diretor_id

    @property
    def nacionalidade(self) -> Nacionalidade:
        return self.__nacionalidade

    @nacionalidade.setter
    def nacionalidade(self, nacionalidade: Nacionalidade):
        if not isinstance(nacionalidade, Nacionalidade):
            raise TypeError("A nacionalidade deve ser uma instância da classe Nacionalidade.")
        self.__nacionalidade = nacionalidade