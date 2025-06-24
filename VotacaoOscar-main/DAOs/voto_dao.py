from DAOs.dao import DAO
from Entidades.Voto import Voto

class VotoDAO(DAO):
    def __init__(self):
        super().__init__('votos.pkl')

    def add(self, voto: Voto):
        if isinstance(voto, Voto) and (voto.id_voto is not None):
            super().add(voto.id_voto, voto)

    def get(self, key: int):
        return super().get(key)

    def remove(self, key: int):
        return super().remove(key)