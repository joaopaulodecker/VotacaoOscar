from DAOs.Dao import DAO
from Entidades.PessoaAbstract import PessoaAbstract

class MembroDAO(DAO):
    """DAO responsável pela persistência dos Membros da Academia."""
    def __init__(self):
        super().__init__('membros.pkl')

    def add(self,key: int, membro: PessoaAbstract):
        """Adiciona um membro, validando o objeto antes de salvar."""
        if membro is not None and isinstance(membro, PessoaAbstract):
            # Se o membro já existe, removemos a versão antiga para substituí-la
            # Importante para a funcionalidade de "alterar"
            super().add(key, membro)

    def get(self, key: int):
        """Busca um membro pelo seu ID (chave)."""
        return super().get(key)

    def remove(self, key: int):
        """Remove um membro pelo seu ID (chave)."""
        return super().remove(key)