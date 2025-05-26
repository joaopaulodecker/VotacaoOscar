import Entidades.Voto

class Categoria:
    """Representa uma categoria de premiação no Oscar.

    Cada categoria tem um nome, um tipo de item que pode ser indicado
    (ator, diretor, filme) e armazena os votos recebidos.

    Attributes:
        id (int): Identificador único da categoria.
        nome (str): Nome da categoria (e.g., "Melhor Filme").
        tipo_indicacao (str): Tipo de item que pode ser indicado nesta categoria
                              (definido em TIPOS_VALIDOS).
        votos (list[Voto]): Lista de objetos Voto registrados para esta categoria.
    """
    TIPOS_VALIDOS = ("ator", "diretor", "filme")

    def __init__(self, id_categoria: int, nome: str, tipo_indicacao: str):
        self.__tipo = tipo_indicacao.lower()
        if self.__tipo not in Categoria.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de indicação inválido: '{tipo_indicacao}'")
        self.__id = id_categoria
        self.__nome = nome
        self.__votos = []

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id_val: int):
        self.__id = id_val

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def votos(self) -> list:
        return self.__votos
    
    @votos.setter
    def votos(self, votos: list):
        self.__votos = votos

    @property
    def tipo_indicacao(self) -> str:
        return self.__tipo

    def adicionar_voto(self, voto):
        """Adiciona um voto à lista de votos desta categoria."""
        if isinstance(voto, Entidades.Voto.Voto): 
            self.__votos.append(voto)

    def total_de_votos(self) -> int:
        return len(self.__votos)
