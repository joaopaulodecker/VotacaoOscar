from Entidades.Filme import Filme
from Limites.TelaFilme import TelaFilmes


class ControladorFilmes:
    def __init__(self, controlador_sistema):
        self.__filmes = []
        self.__tela_filmes = TelaFilmes()
        self.__controlador_sistema = controlador_sistema

    def abre_tela(self):
        while True:
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
            else:
                print("❌ Opção inválida!")

    def cadastrar(self):
        dados = self.__tela_filmes.le_dados_filme()
        filme = Filme(dados["titulo"], dados["ano"])
        self.__filmes.append(filme)
        print(f"✅ Filme '{filme.titulo}' ({filme.ano}) cadastrado!")
        print(f"📋 Total de filmes agora: {len(self.__filmes)}")
        input("🔁 Pressione Enter para continuar...")

    def listar(self, mostrar_msg_voltar=False):
        if not self.__filmes:
            print("📭 Nenhum filme cadastrado.")
        else:
            print("\n🎞️ Lista de Filmes:")
            for i, filme in enumerate(self.__filmes, start=1):
                print(f"{i}. 🎬 {filme.titulo} ({filme.ano})")
        if mostrar_msg_voltar:
            input("🔁 Pressione Enter para voltar ao menu...")

    def alterar(self):
        self.listar()
        titulo_antigo = input("🎬 Digite o título do filme a alterar: ").strip()
        if not titulo_antigo:
            print("❌ Título não pode ser vazio.")
            input("🔁 Pressione Enter para voltar ao menu...")
            return

        for filme in self.__filmes:
            if filme.titulo.casefold() == titulo_antigo.casefold():
                dados = self.__tela_filmes.le_dados_filme()
                filme.titulo = dados["titulo"]
                filme.ano = dados["ano"]
                print(f"✅ Filme '{filme.titulo}' alterado com sucesso.")
                input("🔁 Pressione Enter para voltar ao menu...")
                return

        print("❌ Filme não encontrado.")
        input("🔁 Pressione Enter para voltar ao menu...")

    def excluir(self):
        self.listar()
        titulo = input("🎬 Digite o título do filme a excluir: ").strip()
        if not titulo:
            print("❌ Título não pode ser vazio.")
            input("🔁 Pressione Enter para voltar ao menu...")
            return

        for filme in self.__filmes:
            if filme.titulo.casefold() == titulo.casefold():
                self.__filmes.remove(filme)
                print(f"✅ Filme '{titulo}' removido com sucesso.")
                input("🔁 Pressione Enter para voltar ao menu...")
                return

        print("❌ Filme não encontrado.")
        input("🔁 Pressione Enter para voltar ao menu...")



