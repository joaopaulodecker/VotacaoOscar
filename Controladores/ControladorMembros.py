class ControladorMembros:
    def __init__(self):
        self.__membros = []  # Exemplo: [{"id": 1, "nome": "João"}]

    def adicionar_membro(self, membro):
        self.__membros.append(membro)

    def existe_id(self, id_busca):
        for membro in self.__membros:
            if membro["id"] == id_busca:
                return True
        return False
