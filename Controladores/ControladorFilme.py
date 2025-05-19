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
                self.listar()
            elif opcao == 0:
                break
            else:
                print("Opção inválida!")

    def cadastrar(self):
        dados = self.__tela_filmes.le_dados_filme()
        filme = Filme(dados["titulo"], dados["ano"])
        self.__filmes.append(filme)

    def listar(self):
        for filme in self.__filmes:
            print(f"Título: {filme.titulo} | Ano: {filme.ano}")

    def alterar(self):
        self.listar()
        titulo_antigo = input("Digite o título do filme a alterar: ")
        for filme in self.__filmes:
            if filme.titulo == titulo_antigo:
                dados = self.__tela_filmes.le_dados_filme()
                filme.titulo = dados["titulo"]
                filme.ano = dados["ano"]
                print("Filme alterado com sucesso.")
                return
        print("Filme não encontrado.")

    def excluir(self):
        self.listar()
        titulo = input("Digite o título do filme a excluir: ")
        for filme in self.__filmes:
            if filme.titulo == titulo:
                self.__filmes.remove(filme)
                print("Filme removido com sucesso.")
                return
        print("Filme não encontrado.")
