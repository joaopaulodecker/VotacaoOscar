import pickle
from abc import ABC


class DAO(ABC):
    def __init__(self, datasource=''):
        """
        A classe abstrata para todos os Data Access Objects.
        Usa um dicionário como cache para performance e o pickle para persistência.
        """
        self.__datasource = datasource
        self.__cache = {}
        try:
            # Tenta carregar o almoxarifado do arquivo
            self.__cache = self.__load()
        except FileNotFoundError:
            # Se o arquivo não existe, cria um almoxarifado vazio
            self.__dump()

    def __dump(self):
        """Salva o estado ATUAL do cache no arquivo. Simples e direto."""
        with open(self.__datasource, 'wb') as file:
            pickle.dump(self.__cache, file)

    def __load(self):
        """Carrega os dados do arquivo para o cache em memória."""
        with open(self.__datasource, 'rb') as file:
            return pickle.load(file)

    def add(self,key, obj):
        """Adiciona ou ATUALIZA um objeto no cache usando sua chave (ID)."""
        self.__cache[key] = obj
        self.__dump()

    def get(self, key):
        """Pega um objeto do cache pela chave. Retorna None se não encontrar."""
        return self.__cache.get(key)

    def remove(self, key):
        """Remove um objeto do cache pela chave, se ele existir."""
        if key in self.__cache:
            self.__cache.pop(key)
            self.__dump()  # Salva o estado atualizado

    def get_all(self):
        """Retorna uma lista com todos os objetos (valores) do cache."""
        return list(self.__cache.values())
