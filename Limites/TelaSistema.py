from Utils.validadores import le_num_inteiro

class TelaSistema:
    def mostra_opcoes(self):
        print("\n----- MENU PRINCIPAL -----")
        print("1 - Membro Academia")
        print("2 - Atores")
        print("3 - Diretores")
        print("4 - Filmes")
        print("5 - Categorias")
        print("6 - Indicar")
        print("7 - Votar")
        print("0 - Sair")
        
        return le_num_inteiro("Escolha a opção: ")

