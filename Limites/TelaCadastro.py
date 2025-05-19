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
        print(f"\nPreencha os dados do {self.__tipo}:")
        nome = le_string_nao_vazia("Nome: ")
        id = le_num_inteiro("ID: ")
        nacionalidade = le_string_nao_vazia("Nacionalidade: ")
        return {"id": id, "nome": nome, "nacionalidade": nacionalidade}

    def pegar_id(self):
        return le_num_inteiro("Informe o ID: ")