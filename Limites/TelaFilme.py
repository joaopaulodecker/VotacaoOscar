from Excecoes.OpcaoInvalida import OpcaoInvalida

class TelaFilmes:
    def mostra_opcoes(self):
        print("\n----- FILMES -----")
        print("1 - Cadastrar Filme")
        print("2 - Alterar Filme")
        print("3 - Excluir Filme")
        print("4 - Listar Filmes")
        print("0 - Voltar")

        while True:
            opcao_str = input("Escolha a opção: ").strip()
            if opcao_str.isdigit():
                valor = int(opcao_str)
                if 0 <= valor <= 4:
                    return valor
            raise OpcaoInvalida("Opção de menu de filmes inválida. Escolha entre 0 e 4.")


    def le_dados_filme(self, dados_atuais=None):
        print("\n--- Dados do Filme ---")
        if dados_atuais:
            print(f"(Deixe em branco para manter o valor atual: '{dados_atuais.get('titulo', '')}')")
            titulo_input = input("Novo Título do filme: ").strip()
            titulo = titulo_input if titulo_input else dados_atuais.get("titulo")

            print(f"(Deixe em branco para manter o valor atual: '{dados_atuais.get('ano', '')}')")
            ano_input = input("Novo Ano de lançamento: ").strip()
            ano_str = ano_input if ano_input else str(dados_atuais.get("ano", ""))
        else:
            titulo = input("Título do filme: ").strip()
            ano_str = input("Ano de lançamento: ").strip()

        if not titulo:
            print("❌ Título não pode ser vazio.")
            return None

        if not ano_str:
             print("❌ Ano não pode ser vazio.")
             return None

        try:
            ano = int(ano_str)
            if ano <= 0:
                print("❌ Ano deve ser um número positivo.")
                return None
            return {"titulo": titulo, "ano": ano}
        except ValueError:
            print("❌ Ano inválido. Deve ser um número inteiro.")
            return None

    def seleciona_filme_por_id(self, mensagem="Digite o ID do filme: "):
        while True:
            id_str = input(mensagem).strip()
            if not id_str:
                return None
            if id_str.isdigit():
                return id_str
            print("❌ ID inválido. Por favor, digite um número.")

    def confirma_exclusao(self, titulo_filme):
        while True:
            confirmacao = input(f"Tem certeza que deseja excluir o filme '{titulo_filme}'? (S/N): ").strip().upper()
            if confirmacao == 'S':
                return True
            elif confirmacao == 'N':
                return False
            print("❌ Opção inválida. Digite S para Sim ou N para Não.")

    def mostra_detalhes_filme(self, filme):
        print(f"  ID: {filme.id}")
        print(f"  Título: {filme.titulo}")
        print(f"  Ano: {filme.ano}")
