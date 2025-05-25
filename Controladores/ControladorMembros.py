from Limites.TelaMembroAcademia import TelaMembroAcademia

class ControladorMembros:
    """
    Gerencia as operações relacionadas aos membros da academia.

    Esta classe é responsável por adicionar, listar e buscar membros.
    Ela interage com TelaMembroAcademia para a interface com o usuário,
    embora os métodos de menu e CRUD completos não estejam implementados
    diretamente nesta versão da classe (comparado ao ControladorCadastro).
    Os membros são armazenados como dicionários em uma lista interna.

    Atributos:
        __membros (list): Lista de dicionários, onde cada dicionário representa um membro.
        __tela (TelaMembroAcademia): Instância da tela para interação com o usuário
                                     relacionada a membros.
        """
    def __init__(self):
        self.__membros = []
        self.__tela = TelaMembroAcademia()

    def adicionar_membro(self, membro):
        """
        Adiciona um novo membro à lista de membros, se o ID ainda não existir.
        :param:
            membro (dict): Um dicionário contendo os dados do membro a ser adicionado.
                           Espera-se que o dicionário contenha ao menos as chaves 'id' e 'nome'.

        :return:
            bool: True se o membro foi adicionado com sucesso, False caso contrário
                  (por exemplo, se o ID do membro já existir).
        """
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
        """
        Verifica se um membro com o ID especificado já existe na lista.
         :return: True se um membro com o ID fornecido for encontrado, False caso contrário.
        """
        for membro_dict in self.__membros:
            if membro_dict.get("id") == id_busca:
                return True
        return False

    def listar_membros(self, mostrar_msg_voltar=False):
        """
        Exibe uma lista de todos os membros cadastrados.
        Para cada membro, mostra o ID, nome e, se disponível, a função.
        """
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
        """
        Retorna uma lista de dicionários contendo ID e nome de todos os membros
        que têm a função de "diretor".
        Esta função é útil para, por exemplo, listar diretores disponíveis ao
        cadastrar um filme.
        :return:        list[dict]: Lista de dicionários, cada um com as chaves 'id' e 'nome'
                        dos membros que são diretores. Retorna lista vazia se
                        nenhum diretor for encontrado.
        """
        diretores_info = []
        for membro_dict in self.__membros:
            if membro_dict.get("funcao") == "diretor":
                diretores_info.append({
                    "id": membro_dict.get("id"),
                    "nome": membro_dict.get("nome")
                })
        return diretores_info

    def get_membro_por_id(self, id_membro_busca) -> dict | None:
        """
        Busca e retorna um membro da lista pelo seu ID.
        :param id_membro_busca: O ID do membro a ser procurado.
        :return:  dict | None: O dicionário contendo os dados do membro, se encontrado.
                         Retorna None se nenhum membro com o ID especificado for encontrado.
        """
        for membro_dict in self.__membros:
            if membro_dict.get("id") == id_membro_busca:
                return membro_dict
        return None