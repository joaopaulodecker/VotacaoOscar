from Utils.validadores import le_num_inteiro

class TelaCategoria:

    def mostra_mensagem(self, msg: str):
        """Exibe uma mensagem genérica para o usuário."""
        print(f"\n{msg}")

    def espera_input(self, msg: str = "🔁 Pressione Enter para continuar..."):
        """Exibe uma mensagem e aguarda o input do usuário para pausar."""
        input(msg)

    def mostra_opcoes(self) -> int:
        """Exibe o menu de opções e retorna a escolha validada do usuário."""
        self.mostra_mensagem("----- CATEGORIAS -----")
        self.mostra_mensagem("1 - Cadastrar Categoria")
        self.mostra_mensagem("2 - Alterar Categoria")
        self.mostra_mensagem("3 - Excluir Categoria")
        self.mostra_mensagem("4 - Listar Categorias")
        self.mostra_mensagem("0 - Voltar")

        return le_num_inteiro("Escolha uma opção: ", min_val=0, max_val=4)

    def seleciona_categoria_por_id(self, mensagem="Digite o ID da categoria: ") -> int | None:
        """Pede um ID ao usuário e o retorna como inteiro."""
        return le_num_inteiro(mensagem, permitir_vazio=True)

    def confirma_exclusao(self, nome_categoria: str) -> bool:
        """Pede confirmação do usuário para uma exclusão."""
        confirmacao = input(
            f"Tem certeza que deseja excluir a categoria '{nome_categoria}'? (S/N): "
        ).strip().upper()
        return confirmacao == 'S'

    # Substitua as duas versões de pega_dados_categoria por esta única versão.
    def pega_dados_categoria(self, dados_atuais: dict = None) -> dict | None:
        """
        Coleta dados para CADASTRAR ou ALTERAR uma categoria.
        Se 'dados_atuais' for fornecido, a função entra em modo de alteração.
        """
        from Utils.validadores import le_string_nao_vazia, le_num_inteiro

        # --- Lógica para definir o título e o prompt do nome ---
        if dados_atuais:
            # MODO ALTERAÇÃO: se recebeu dados_atuais
            self.mostra_mensagem(f"\n--- Alteração de Categoria (ID: {dados_atuais.get('id')}) ---")
            self.mostra_mensagem("Dica: Deixe em branco e pressione Enter para manter o valor atual.")
            nome_prompt = f"Novo nome (atual: {dados_atuais.get('nome')}): "
            # Em modo de alteração, permitimos que o input seja vazio
            nome_input = input(nome_prompt)
            # Se o usuário não digitou nada, mantemos o que era antes. Se não, usamos o novo.
            nome_final = nome_input.strip() if nome_input else dados_atuais.get("nome")
        else:
            # MODO CADASTRO: se dados_atuais for None
            self.mostra_mensagem("\n--- Cadastro de Nova Categoria ---")
            nome_prompt = "Nome da categoria: "
            # Em modo de cadastro, o nome não pode ser vazio
            nome_final = le_string_nao_vazia(nome_prompt)

        # Se em algum momento o nome final for nulo (ex: cancelou o cadastro), para.
        if not nome_final:
            return None

        # --- Lógica para definir o tipo (só acontece no cadastro) ---
        if not dados_atuais:
            self.mostra_mensagem("\nTipo de Indicação para a Categoria:")
            mapa_tipos = {1: "filme", 2: "ator", 3: "diretor"}
            self.mostra_mensagem("1 - Filme")
            self.mostra_mensagem("2 - Ator/Atriz")
            self.mostra_mensagem("3 - Diretor")

            escolha = le_num_inteiro("Escolha o número do tipo: ", min_val=1, max_val=3)
            if escolha is None:
                return None  # Usuário cancelou

            tipo_final = mapa_tipos[escolha]
            return {"nome": nome_final.title(), "tipo_indicacao": tipo_final}

        # Se estávamos em modo de alteração, retornamos apenas o nome.
        return {"nome": nome_final.title()}

    def mostra_lista_categorias(self, categorias_dados: list[dict]):
        """Recebe uma lista de dicionários com dados das categorias e os exibe."""
        self.mostra_mensagem("\n--- Lista de Categorias Cadastradas ---")
        if not categorias_dados:
            self.mostra_mensagem("📭 Nenhuma categoria cadastrada.")
            return

        for cat_info in categorias_dados:
            print(f"ID: {cat_info['id']} | Nome: {cat_info['nome']} | Tipo: {cat_info['tipo'].capitalize()}")