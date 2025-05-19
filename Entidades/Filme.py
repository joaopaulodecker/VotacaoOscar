class Filme:
    def __init__(self, titulo: str, ano: int):
        self.__titulo = titulo
        self.__ano = ano

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = titulo

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, ano):
        self.__ano = ano
