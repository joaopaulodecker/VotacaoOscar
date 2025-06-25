
class Categoria:
    """Representa uma categoria de premiação no Oscar.

    Cada categoria tem um nome e um tipo de item que pode ser indicado
    (ator, diretor, filme).

    Attributes:
        -id (int): Identificador único da categoria.
        -nome (str): Nome da categoria (e.g., "Melhor Filme").
        -tipo_indicacao (str): Tipo de item que pode ser indicado nesta categoria
                              (definido em TIPOS_VALIDOS).
    """
    TIPOS_VALIDOS = ("ator", "diretor", "filme")

    def __init__(self, id_categoria: int, nome: str, tipo_indicacao: str):
        self.__tipo = tipo_indicacao.lower()
        if self.__tipo not in Categoria.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de indicação inválido: '{tipo_indicacao}'")
        self.__id = id_categoria
        self.__nome = nome


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
    def tipo_indicacao(self) -> str:
        return self.__tipo

