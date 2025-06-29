from DAOs.Dao import DAO
from Entidades.PessoaAbstract import PessoaAbstract

class MembroDAO(DAO):
    """DAO específico para a persistência dos Membros (Atores, Diretores, etc.)."""
    def __init__(self):
        # Garante que os dados sejam salvos no arquivo 'membros.pkl'
        super().__init__('membros.pkl')

    def add(self, key: int, membro: PessoaAbstract):
        """Adiciona um membro ao cache, validando o tipo do objeto."""
        # Valida que o objeto é uma subclasse de PessoaAbstract (nosso modelo base para membros)
        if membro is not None and isinstance(membro, PessoaAbstract):
            super().add(key, membro)

    def get(self, key: int):
        """Busca um membro pelo seu ID (chave)."""
        return super().get(key)

    def remove(self, key: int):
        """Remove um membro pelo seu ID (chave)."""
        return super().remove(key)