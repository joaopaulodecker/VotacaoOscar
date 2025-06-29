# Em Entidades/Filme.py
from Entidades.Nacionalidade import Nacionalidade

class Filme:
    """Representa a entidade Filme no sistema."""
    def __init__(self, id_filme: int, titulo: str, ano_lancamento: int, diretor_id: int, nacionalidade: Nacionalidade):
        # --- CORREÇÃO APLICADA AQUI ---
        # O parâmetro 'ano' foi renomeado para 'ano_lancamento' para ser consistente
        # com o resto do sistema.
        self.__id_filme = id_filme
        self.__titulo = titulo
        self.__ano_lancamento = ano_lancamento
        self.__diretor_id = diretor_id
        self.__nacionalidade = nacionalidade

    @property
    def id_filme(self) -> int:
        return self.__id_filme

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo: str):
        self.__titulo = titulo

    @property
    def ano_lancamento(self) -> int:
        return self.__ano_lancamento

    @ano_lancamento.setter
    def ano_lancamento(self, ano_lancamento: int):
        self.__ano_lancamento = ano_lancamento

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
        self.__nacionalidade = nacionalidade