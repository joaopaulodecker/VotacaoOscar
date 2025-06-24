import pickle
from abc import ABC, abstractmethod


class DAO(ABC):
    def __init__(self, datasource=''):
        """
        Inicializa o DAO, definindo o arquivo de dados e carregando o cache.

        Se o arquivo de dados não existir, ele é criado com uma lista vazia.
        """
        self.__datasource = datasource
        self.__cache = []  
        try:
            self.__cache = self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        """Salva a lista do cache em memória para o arquivo de dados."""
        with open(self.__datasource, 'wb') as file:
            pickle.dump(self.__cache, file)

    def __load(self):
        """Carrega os dados do arquivo para o cache em memória."""
        with open(self.__datasource, 'rb') as file:
            return pickle.load(file)

    def add(self, obj):
        self.__cache.append(obj)
        self.__dump()

    @abstractmethod
    def get(self, key):
      
        pass

    @abstractmethod
    def remove(self, key):
        pass

    def get_all(self):
        """Retorna a lista completa de objetos armazenados no cache."""
        return self.__cache