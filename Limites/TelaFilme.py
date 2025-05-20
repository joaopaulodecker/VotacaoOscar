class TelaFilmes:
    def mostra_opcoes(self):
        print("\n----- FILMES -----")
        print("1 - Cadastrar Filme")
        print("2 - Alterar Filme")
        print("3 - Excluir Filme")
        print("4 - Listar Filmes")
        print("0 - Voltar")

        opcao = input("Escolha a opção: ")
        if opcao.isdigit():
            return int(opcao)
        return -1

    def le_dados_filme(self):
        titulo = input("Título do filme: ")
        ano = int(input("Ano de lançamento: "))
        return {"titulo": titulo, "ano": ano}
