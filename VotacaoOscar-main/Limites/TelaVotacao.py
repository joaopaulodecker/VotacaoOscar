from Utils.validadores import le_num_inteiro

class TelaVotacao:

    def mostra_mensagem(self, msg: str):
        print(msg)

    def espera_input(self, msg: str = "🔁 Pressione Enter para continuar..."):
        """Exibe uma mensagem e aguarda o input do usuário para pausar."""
        input(msg)

    def mostra_opcoes_votacao(self) -> int:
        self.mostra_mensagem("\n----- VOTAÇÃO -----")
        self.mostra_mensagem("1 - Registrar Novo Voto")
        self.mostra_mensagem("2 - Ver Resultados da Votação")
        self.mostra_mensagem("0 - Voltar ao Menu Principal")
        return le_num_inteiro("Escolha a opção: ", min_val=0, max_val=2)

    def _selecionar_item_da_lista(self, lista_dados: list[dict], titulo_selecao: str) -> dict | None:
        if not lista_dados:
            self.mostra_mensagem(f"Nenhum(a) {titulo_selecao} disponível para seleção.")
            return None
        
        self.mostra_mensagem(f"\n--- Selecionar {titulo_selecao} ---")
        for i, item in enumerate(lista_dados):
            self.mostra_mensagem(f"{i + 1}. {item.get('info', 'Dados indisponíveis')}")
            
        prompt = (f"Escolha o número do(a) {titulo_selecao.lower()} (1-{len(lista_dados)}) "
                  "ou 0 para cancelar: ")
        escolha_num = le_num_inteiro(prompt, min_val=0, max_val=len(lista_dados))
        
        if escolha_num is None or escolha_num == 0:
            self.mostra_mensagem("Seleção cancelada.")
            return None
        
        return lista_dados[escolha_num - 1]

    def seleciona_membro_votante(self, membros_dados: list[dict]) -> dict | None:
        return self._selecionar_item_da_lista(membros_dados, "Membro Votante")

    def seleciona_categoria_para_voto(self, categorias_dados: list[dict]) -> dict | None:
        return self._selecionar_item_da_lista(categorias_dados, "Categoria para Votar")

    def seleciona_indicado_para_voto(self, indicados_dados: list, nome_categoria: str) -> dict | None:
        if not indicados_dados:
            self.mostra_mensagem(f"Nenhum indicado disponível na categoria '{nome_categoria}'.")
            return None

        self.mostra_mensagem(f"\n--- Votar em Finalistas para '{nome_categoria}' ---")
        for i, indicado in enumerate(indicados_dados):
            self.mostra_mensagem(f"{i + 1}. {indicado.get('nome_display', 'Item Desconhecido')}")
        
        prompt = (f"Escolha o número do seu voto (1-{len(indicados_dados)}) "
                  "ou 0 para cancelar: ")
        escolha = le_num_inteiro(prompt, min_val=0, max_val=len(indicados_dados))
        
        if escolha is None or escolha == 0:
            self.mostra_mensagem("Votação cancelada.")
            return None
            
        return indicados_dados[escolha - 1]

    def mostra_resultados(self, resultados_formatados: dict):
        self.mostra_mensagem("\n--- Resultados da Votação ---")
        if not resultados_formatados:
            self.mostra_mensagem("Nenhuma contagem de votos para exibir.")
            return

        for nome_categoria, votos_ordenados in resultados_formatados.items():
            self.mostra_mensagem(f"\n🏆 Categoria: {nome_categoria}")
            if not votos_ordenados:
                self.mostra_mensagem("   Nenhum voto nesta categoria.")
                continue
            
            for item_nome, contagem in votos_ordenados:
                self.mostra_mensagem(f"   - {item_nome}: {contagem} voto(s)")
