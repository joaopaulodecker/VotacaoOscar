from Entidades.Filme import Filme
from Limites.TelaFilme import TelaFilmes
from Excecoes.OpcaoInvalida import OpcaoInvalida

class ControladorFilmes:
    def __init__(self, controlador_sistema):
        self.__filmes = []
        self.__tela_filmes = TelaFilmes()
        self.__controlador_sistema = controlador_sistema
        self.__proximo_id = 1

    @property
    def filmes(self):
        return self.__filmes

    def _gerar_proximo_id(self):
        id_atual = self.__proximo_id
        self.__proximo_id += 1
        return id_atual

    def buscar_filme_por_id(self, id_filme):
        for filme in self.__filmes:
            if filme.id == id_filme:
                return filme
        return None

    def existe_titulo_filme(self, titulo, id_excluir=None):
        for filme in self.__filmes:
            if filme.id == id_excluir:
                continue
            if filme.titulo.casefold() == titulo.casefold():
                return True
        return False

    def abre_tela(self):
        while True:
            try:
                opcao = self.__tela_filmes.mostra_opcoes()
                if opcao == 1:
                    self.cadastrar()
                elif opcao == 2:
                    self.alterar()
                elif opcao == 3:
                    self.excluir()
                elif opcao == 4:
                    self.listar(mostrar_msg_voltar=True)
                elif opcao == 0:
                    break
            except OpcaoInvalida as e:
                print(f"❌ {e}")
                input("🔁 Pressione Enter para tentar novamente...")
            except Exception as e:
                print(f"❌ Ocorreu um erro inesperado no menu de filmes: {e}")
                input("🔁 Pressione Enter para continuar...")


    def cadastrar(self):
        print("\n--- Cadastro de Novo Filme ---")
        dados = self.__tela_filmes.le_dados_filme()
        if not dados or not dados.get("titulo") or dados.get("ano") is None:
            print("❌ Dados inválidos para cadastro. Título e ano são obrigatórios.")
            input("🔁 Pressione Enter para continuar...")
            return

        if self.existe_titulo_filme(dados["titulo"]):
            print(f"❌ Já existe um filme com o título '{dados['titulo']}'.")
            input("🔁 Pressione Enter para continuar...")
            return
        
        try:
            ano = int(dados["ano"])
            if ano <= 0:
                raise ValueError("Ano deve ser um número positivo.")
        except ValueError as e:
            print(f"❌ Ano inválido: {e}. Deve ser um número inteiro positivo.")
            input("🔁 Pressione Enter para continuar...")
            return

        novo_id = self._gerar_proximo_id()
        filme = Filme(id_filme=novo_id, titulo=dados["titulo"], ano=ano)
        self.__filmes.append(filme)
        print(f"✅ Filme ID {filme.id} - '{filme.titulo}' ({filme.ano}) cadastrado!")
        input("🔁 Pressione Enter para continuar...")

    def listar(self, mostrar_msg_voltar=False, com_indices=False):
        if not self.__filmes:
            print("📭 Nenhum filme cadastrado.")
            return False
        
        print("\n--- Lista de Filmes Cadastrados ---")
        for i, filme in enumerate(self.__filmes):
            prefixo = f"{filme.id}. " if not com_indices else f"{i+1}. (ID: {filme.id}) "
            print(f"{prefixo}🎬 {filme.titulo} ({filme.ano})")
        
        if mostrar_msg_voltar:
            input("\n🔁 Pressione Enter para voltar ao menu...")
        return True

    def alterar(self):
        print("\n--- Alteração de Filme ---")
        if not self.listar():
            input("🔁 Pressione Enter para continuar...")
            return

        try:
            id_alvo_str = self.__tela_filmes.seleciona_filme_por_id(mensagem="Digite o ID do filme que deseja alterar: ")
            if id_alvo_str is None: # Usuário cancelou
                print("ℹ️ Alteração cancelada.")
                input("� Pressione Enter para continuar...")
                return
            id_alvo = int(id_alvo_str)
        except ValueError:
            print("❌ ID inválido. Deve ser um número.")
            input("🔁 Pressione Enter para continuar...")
            return

        filme_alvo = self.buscar_filme_por_id(id_alvo)

        if not filme_alvo:
            print(f"❌ Filme com ID {id_alvo} não encontrado.")
            input("🔁 Pressione Enter para continuar...")
            return

        print(f"\nEditando filme: ID {filme_alvo.id} - '{filme_alvo.titulo}' ({filme_alvo.ano})")
        novos_dados = self.__tela_filmes.le_dados_filme(dados_atuais={"titulo": filme_alvo.titulo, "ano": filme_alvo.ano})

        if not novos_dados or not novos_dados.get("titulo") or novos_dados.get("ano") is None:
            print("❌ Dados inválidos para alteração. Título e ano são obrigatórios.")
            input("🔁 Pressione Enter para continuar...")
            return

        if filme_alvo.titulo.casefold() != novos_dados["titulo"].casefold() and self.existe_titulo_filme(novos_dados["titulo"], id_excluir=filme_alvo.id):
            print(f"❌ Já existe outro filme com o título '{novos_dados['titulo']}'.")
            input("🔁 Pressione Enter para continuar...")
            return
            
        try:
            novo_ano = int(novos_dados["ano"])
            if novo_ano <= 0:
                raise ValueError("Ano deve ser um número positivo.")
        except ValueError as e:
            print(f"❌ Ano inválido: {e}. Deve ser um número inteiro positivo.")
            input("🔁 Pressione Enter para continuar...")
            return

        filme_alvo.titulo = novos_dados["titulo"]
        filme_alvo.ano = novo_ano
        print(f"✅ Filme ID {filme_alvo.id} - '{filme_alvo.titulo}' alterado com sucesso.")
        input("🔁 Pressione Enter para continuar...")

    def excluir(self):
        print("\n--- Exclusão de Filme ---")
        if not self.listar():
            input("🔁 Pressione Enter para continuar...")
            return

        try:
            id_alvo_str = self.__tela_filmes.seleciona_filme_por_id(mensagem="Digite o ID do filme que deseja excluir: ")
            if id_alvo_str is None: # Usuário cancelou
                print("ℹ️ Exclusão cancelada.")
                input("🔁 Pressione Enter para continuar...")
                return
            id_alvo = int(id_alvo_str)
        except ValueError:
            print("❌ ID inválido. Deve ser um número.")
            input("🔁 Pressione Enter para continuar...")
            return

        filme_alvo = self.buscar_filme_por_id(id_alvo)

        if not filme_alvo:
            print(f"❌ Filme com ID {id_alvo} não encontrado.")
            input("🔁 Pressione Enter para continuar...")
            return
        
        self.__filmes.remove(filme_alvo)
        print(f"🗑️ Filme ID {filme_alvo.id} - '{filme_alvo.titulo}' removido com sucesso.")
        input("🔁 Pressione Enter para continuar...")
