from Utils.validadores import le_num_inteiro

class TelaSistema:

    def mostra_mensagem(self, msg: str):
        print(msg)

    def espera_input(self, msg: str = "🔁 Pressione Enter para continuar..."):
        """Exibe uma mensagem e aguarda o input do usuário para pausar."""
        input(msg)

    def mostra_lista(self, titulo: str, lista_itens: list[str]):
        self.mostra_mensagem(titulo)
        if not lista_itens:
            self.mostra_mensagem("   (Nenhum item encontrado)")
        else:
            for item in lista_itens:
                self.mostra_mensagem(item)

    def mostra_opcoes(self) -> int:
        self.mostra_mensagem("\n⭐ ----- MENU PRINCIPAL OSCAR ----- ⭐")
        self.mostra_mensagem("1 - Gerenciar Membros da Academia")
        self.mostra_mensagem("2 - Listar Atores")
        self.mostra_mensagem("3 - Listar Diretores")
        self.mostra_mensagem("4 - Gerenciar Filmes")
        self.mostra_mensagem("5 - Gerenciar Categorias")
        self.mostra_mensagem("6 - Gerenciar Indicações")
        self.mostra_mensagem("7 - Gerenciar Votação")
        self.mostra_mensagem("8 - Ver Resultados da Votação")
        self.mostra_mensagem("9 - Encerrar Indicações / Abrir Votação")
        self.mostra_mensagem("0 - Sair do Sistema")
        
        return le_num_inteiro("Escolha uma opção: ", min_val=0, max_val=9)