from DAOs.dao import DAO

class MembroDAO(DAO):
    def __init__(self):
        super().__init__('membros.pkl')

    def add(self, membro: dict):
        if isinstance(membro, dict) and 'id' in membro:
            super().add(membro)

    def get(self, key: int):
        if isinstance(key, int):
            for membro in self.get_all():
                if membro.get('id') == key:
                    return membro
        return None

    def remove(self, key: int):
        if isinstance(key, int):
            lista_completa = self.get_all()
            nova_lista = [membro for membro in lista_completa if membro.get('id') != key]
            self._DAO__dump(nova_lista)