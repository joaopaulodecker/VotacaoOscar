from Utils.validadores import le_num_inteiro, le_string_nao_vazia
from Excecoes.OpcaoInvalida import OpcaoInvalida

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

        opcao = le_num_inteiro("Escolha uma opção: ")
        if opcao not in range(0, 5):
            raise OpcaoInvalida()
        return opcao

    def pegar_dados(self):
        print(f"\n--- Cadastro de {self.__tipo.capitalize()} ---")
        print("(Deixe em branco para cancelar)")

        try:
            nome = input("Nome: ").strip()
            if not nome:
                return None

            id = le_num_inteiro("ID: ")

            if self.__tipo == "categoria":
                return {
                    "id": id,
                    "nome": nome
                }
            else:
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
