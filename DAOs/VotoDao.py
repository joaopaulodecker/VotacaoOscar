from DAOs.Dao import DAO
from Entidades.Voto import Voto

class VotoDAO(DAO):
    def __init__(self):
        super().__init__('votos.pkl')

    def add(self, key: int, voto: Voto):
        if voto is not None and isinstance(voto, Voto) and hasattr(voto, 'id_voto'):
            super().add(key, voto)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)
        return None

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)