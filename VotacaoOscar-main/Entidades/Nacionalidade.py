class Nacionalidade:

    def __init__(self, pais: str):
        self.__pais = pais

    @property
    def pais(self):
        return self.__pais

    @pais.setter
    def pais(self, pais):
        self.__pais = pais
