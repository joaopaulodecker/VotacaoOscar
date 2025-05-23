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
        for membro_dict in self.__membros:
            if membro_dict.get("id") == id_busca:
                return True
        return False

    def listar_membros(self, mostrar_msg_voltar=False):
        if not self.__membros:
            print("📭 Nenhum membro cadastrado.")
        else:
            print("\n👥 Lista de Membros:")
            for membro in self.__membros:
                funcao_str = f" | Função: {membro.get('funcao', 'N/A').capitalize()}" if 'funcao' in membro else ""
                print(f"ID: {membro['id']} | Nome: {membro['nome']}{funcao_str}")
        if mostrar_msg_voltar:
            input("🔁 Pressione Enter para voltar ao menu...")

    def get_diretores_info(self) -> list[dict]:
        diretores_info = []
        for membro_dict in self.__membros:
            if membro_dict.get("funcao") == "diretor":
                diretores_info.append({
                    "id": membro_dict.get("id"),
                    "nome": membro_dict.get("nome")
                })
        return diretores_info

    def get_membro_por_id(self, id_membro_busca) -> dict | None:
        for membro_dict in self.__membros:
            if membro_dict.get("id") == id_membro_busca:
                return membro_dict
        return None