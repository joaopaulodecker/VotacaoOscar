from Limites.TelaMembroAcademia import TelaMembroAcademia
from datetime import date


class ControladorMembros:

    def __init__(self):
        self.__membros = []
        self.__tela = TelaMembroAcademia()

    @property
    def entidades(self):
        return self.__membros

    def adicionar_membro(self, membro):
        """Adiciona um novo membro à lista, se o ID ainda não existir."""
        if self.existe_id(membro["id"]):
            self.__tela.mostra_mensagem(f"❌ Membro com ID {membro['id']} já registrado!")
            self.__tela.espera_input()
            return False
        else:
            self.__membros.append(membro)
            self.__tela.mostra_mensagem(f"✅ Membro {membro['nome']} cadastrado com sucesso!")
            self.__tela.espera_input()
            return True

    def existe_id(self, id_busca):
        for membro_dict in self.__membros:
            if membro_dict.get("id") == id_busca:
                return True
        return False

    def _preparar_dados_para_tela(self, membro_dict: dict) -> dict:
        info_str = f"ID: {membro_dict.get('id')} | Nome: {membro_dict.get('nome')}"
        if membro_dict.get('funcao'):
            info_str += f" | Função: {membro_dict.get('funcao').capitalize()}"
        return {"info_str": info_str}

    def listar_membros(self, mostrar_msg_voltar=False):
        if not self.__membros:
            self.__tela.mostra_mensagem("📭 Nenhum membro cadastrado.")
        else:
            lista_para_tela = [
                self._preparar_dados_para_tela(membro) for membro in self.__membros
            ]
            self.__tela.mostra_lista_membros(lista_para_tela)

        if mostrar_msg_voltar:
            self.__tela.espera_input()

    def get_diretores_info(self) -> list[dict]:
        return [
            {"id": membro.get("id"), "nome": membro.get("nome")}
            for membro in self.__membros
            if membro.get("funcao") == "diretor"
        ]

    def get_membro_por_id(self, id_membro_busca) -> dict | None:
        for membro_dict in self.__membros:
            if membro_dict.get("id") == id_membro_busca:
                return membro_dict
        return None
