from Utils.validadores import le_num_inteiro

class TelaIndicacao:

    def mostra_mensagem(self, msg: str):
        print(msg)

    def espera_input(self, msg: str = "🔁 Pressione Enter para continuar..."):
        """Exibe uma mensagem e aguarda o input do usuário para pausar."""
        input(msg)

    def mostra_opcoes_indicacao(self) -> int:
        """Exibe o menu de opções e retorna a escolha do usuário."""
        self.mostra_mensagem("\n----- INDICAÇÕES -----")
        self.mostra_mensagem("1 - Registrar Nova Indicação")
        self.mostra_mensagem("2 - Alterar Indicação")
        self.mostra_mensagem("3 - Excluir Indicação")
        self.mostra_mensagem("4 - Listar Indicações por Categoria")
        self.mostra_mensagem("0 - Voltar ao Menu Principal")

        return le_num_inteiro("Escolha a opção: ", min_val=0, max_val=4)

    def _selecionar_item_da_lista(self, lista_dados: list[dict], titulo_selecao: str) -> dict | None:

        if not lista_dados:
            self.mostra_mensagem(f"Nenhum(a) {titulo_selecao} disponível para seleção.")
            return None
        
        self.mostra_mensagem(f"\n--- Selecionar {titulo_selecao} ---")
        for i, item in enumerate(lista_dados):
            self.mostra_mensagem(f"{i + 1}. {item.get('info', 'Dados indisponíveis')}")
            
        try:
            prompt = (f"Escolha o número do(a) {titulo_selecao.lower()} (1-{len(lista_dados)}) "
                      "ou 0 para cancelar: ")
            escolha_num = le_num_inteiro(prompt, min_val=0, max_val=len(lista_dados))
            
            if escolha_num is None or escolha_num == 0:
                self.mostra_mensagem("Seleção cancelada.")
                return None

            return lista_dados[escolha_num - 1].get('id')
        except (ValueError, IndexError):
            self.mostra_mensagem("Entrada inválida. Por favor, digite um número da lista.")
            return None

    def seleciona_membro(self, membros_dados: list[dict]) -> dict | None:
        return self._selecionar_item_da_lista(membros_dados, "Membro da Academia")

    def seleciona_categoria(self, categorias_dados: list[dict]) -> dict | None:
        return self._selecionar_item_da_lista(categorias_dados, "Categoria")

    def seleciona_filme(self, filmes_dados: list[dict]) -> dict | None:
        return self._selecionar_item_da_lista(filmes_dados, "Filme")

    def seleciona_membro_por_funcao(self, membros_dados: list, funcao_nome: str) -> dict | None:
        return self._selecionar_item_da_lista(membros_dados, funcao_nome)

    def mostra_lista_indicacoes(self, categoria_nome: str, indicacoes_dados: list[str]):
        """Exibe as indicações para uma categoria específica."""

        self.mostra_mensagem(f"\nIndicados para: {categoria_nome}")

        if not indicacoes_dados:
            self.mostra_mensagem("   Nenhuma indicação para esta categoria ainda.")
        else:
            for detalhes_indicacao in indicacoes_dados:
                self.mostra_mensagem(f"   - {detalhes_indicacao}")

    def mostra_lista_geral_indicacoes(self, indicacoes: list[str]):
        """Exibe uma lista formatada de todas as indicações registradas."""
        print("\n--- Lista Geral de Indicações Registradas ---")
        if not indicacoes:
            print("📭 Nenhuma indicação registrada até o momento.")
            return

        for info_str in indicacoes:
            print(info_str)

    def pega_id_indicacao(self, mensagem_prompt: str) -> int | None:
        """Pede ao usuário para digitar o ID de uma indicação e o retorna."""
        print("")
        # Validador para garantir um número ou None se o usuário cancelar
        return le_num_inteiro(mensagem_prompt, min_val=1, permitir_vazio=True)

    def confirma_exclusao(self, info_indicacao: str) -> bool:
        """Mostra os detalhes de uma indicação e pede confirmação para excluir."""
        from Utils.validadores import le_string_nao_vazia
        print(f"\nVocê está prestes a excluir a seguinte indicação:")
        print(f"  -> {info_indicacao}")

        resposta = le_string_nao_vazia("Tem certeza que deseja excluir? (S/N): ")

        # Retorna True se a resposta for 'S' ou 's', False caso contrário
        return resposta is not None and resposta.upper().startswith('S')
