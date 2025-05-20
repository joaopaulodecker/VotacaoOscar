from Utils.validadores import le_num_inteiro, le_string_nao_vazia

class TelaCadastro:
    def __init__(self, tipo):
        self.__tipo = tipo

    def mostrar_menu(self):
        print(f"\n===== MENU {self.__tipo.upper()} =====")
        print("1 - Cadastrar")
        print("2 - Alterar")
        print("3 - Excluir")
        print("4 - Listar")
        print("0 - Voltar")
        return le_num_inteiro("Escolha uma opção: ")

    def pegar_dados(self):
        """Coleta dados para cadastro, diferenciando categorias (sem nacionalidade)"""
        print(f"\n--- Cadastro de {self.__tipo.capitalize()} ---")
        print("(Deixe em branco para cancelar)")

        try:
            # Coleta nome (obrigatório para todos)
            nome = input("Nome: ").strip()
            if not nome:
                return None

            # Coleta ID (numérico)
            id = le_num_inteiro("ID: ")

            # Lógica diferenciada para categorias
            if self.__tipo == "categoria":
                return {
                    "id": id,
                    "nome": nome
                }
            else:
                # Para membros/atores/diretores
                nacionalidade = input("Nacionalidade: ").strip()
                if not nacionalidade:
                    return None

                return {
                    "id": id,
                    "nome": nome,
                    "nacionalidade": nacionalidade
                }

        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário")
            return None

    def pegar_id(self):
        return le_num_inteiro("Informe o ID: ")