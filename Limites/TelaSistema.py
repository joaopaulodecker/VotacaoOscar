from Utils.validadores import le_num_inteiro
from Excecoes.OpcaoInvalida import OpcaoInvalida

class TelaSistema:
    def __init__(self):
        pass

    def mostra_opcoes(self) -> int:
        print("\n⭐ ----- MENU PRINCIPAL OSCAR ----- ⭐")
        print("1 - Gerenciar Membros da Academia")
        print("2 - Listar Atores")
        print("3 - Listar Diretores")
        print("4 - Gerenciar Filmes")
        print("5 - Gerenciar Categorias")
        print("6 - Gerenciar Indicações")
        print("7 - Gerenciar Votação")
        print("8 - Ver Resultados da Votação")
        print("0 - Sair do Sistema")
        
        while True:
            opcao_str = input("Escolha uma opção: ").strip()
            if opcao_str.isdigit():
                opcao = int(opcao_str)
                if 0 <= opcao <= 8:
                    return opcao
            raise OpcaoInvalida("Opção de menu principal inválida. Escolha entre 0 e 8.")

    def mostra_mensagem(self, msg: str):
        print(f"\n{msg}")
