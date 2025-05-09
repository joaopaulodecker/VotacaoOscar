class TelaFilme:
    def tela_opcoes(self):
        print("\n------ FILMES ------")
        print("1 - Cadastrar Filme")
        print("2 - Alterar Filme")
        print("3 - Listar Filmes")
        print("4 - Excluir Filme")
        print("0 - Voltar")

        while True:
            try:
                opcao = int(input("Escolha a opção: "))
                if opcao in [0, 1, 2, 3, 4]:
                    return opcao
                else:
                    print("Opção inválida. Digite um número entre 0 e 4.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def pega_dados_filme(self):
        print("\n------ DADOS DO FILME ------")
        titulo = input("Título: ")
        ano = input("Ano: ")
        diretor = input("Diretor: ")
        nacionalidade = input("Nacionalidade: ")

        return {
            "titulo": titulo,
            "ano": ano,
            "diretor": diretor,
            "nacionalidade": nacionalidade
        }

    def mostra_filme(self, dados_filme):
        print("\nTÍTULO:", dados_filme["titulo"])
        print("ANO:", dados_filme["ano"])
        print("DIRETOR:", dados_filme["diretor"])
        print("NACIONALIDADE:", dados_filme["nacionalidade"])
        print("--------------------------")

    def mostra_mensagem(self, mensagem):
        print(f"\n{mensagem}")

    def seleciona_filme(self):
        titulo = input("\nDigite o título do filme: ")
        return titulo
