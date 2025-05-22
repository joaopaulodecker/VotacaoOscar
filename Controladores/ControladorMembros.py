from Limites.TelaMembroAcademia import TelaMembroAcademia

class ControladorMembros:
    def __init__(self):
        self.__membros = []
        self.__tela = TelaMembroAcademia()

    def adicionar_membro(self, membro):
        if self.existe_id(membro["id"]):
            print(f"❌ Membro com ID {membro['id']} já registrado!")
            input("🔁 Pressione Enter para continuar...")
            return False
        else:
            self.__membros.append(membro)
            print(f"✅ Membro {membro['nome']} cadastrado com sucesso!")
            input("🔁 Pressione Enter para continuar...")
            return True

    def existe_id(self, id_busca):
        return any(membro["id"] == id_busca for membro in self.__membros)

    def listar_membros(self, mostrar_msg_voltar=False):
        if not self.__membros:
            print("📭 Nenhum membro cadastrado.")
        else:
            print("\n👥 Lista de Membros:")
            for membro in self.__membros:
                print(f"ID: {membro['id']} | Nome: {membro['nome']}")
        if mostrar_msg_voltar:
            input("🔁 Pressione Enter para voltar ao menu...")
