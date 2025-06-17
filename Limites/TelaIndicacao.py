from Excecoes.OpcaoInvalida import OpcaoInvalida
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
        self.mostra_mensagem("2 - Listar Indicações por Categoria")
        self.mostra_mensagem("0 - Voltar ao Menu Principal")

        return le_num_inteiro("Escolha a opção: ", min_val=0, max_val=2)

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
            
            return lista_dados[escolha_num - 1]
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

    def pega_tipo_item_indicado(self, nome_categoria: str) -> str | None:
        self.mostra_mensagem(f"\nPara a categoria '{nome_categoria}', você quer indicar:")
        self.mostra_mensagem("1 - Filme 🎬")
        self.mostra_mensagem("2 - Ator/Atriz 🎭")
        self.mostra_mensagem("3 - Diretor(a) 🎬")
        self.mostra_mensagem("0 - Cancelar Indicação")
        
        opcao = le_num_inteiro("👉 Escolha uma opção (0-3): ", min_val=0, max_val=3)
        if opcao == 1:
            return "filme"
        elif opcao == 2:
            return "ator"
        elif opcao == 3:
            return "diretor"
        return None

    def mostra_lista_indicacoes(self, categoria_nome: str, indicacoes_dados: list[str]):
        """Exibe as indicações para uma categoria específica."""

        self.mostra_mensagem(f"\nIndicados para: {categoria_nome}")

        if not indicacoes_dados:
            self.mostra_mensagem("   Nenhuma indicação para esta categoria ainda.")
        else:
            for detalhes_indicacao in indicacoes_dados:
                self.mostra_mensagem(f"   - {detalhes_indicacao}")