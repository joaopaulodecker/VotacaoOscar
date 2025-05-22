from Limites.TelaSistema import TelaSistema
from Controladores.ControladorFilme import ControladorFilmes
from Controladores.ControladorCadastro import ControladorCadastro
from Controladores.ControladorIndicacao import ControladorIndicacao
from Controladores.ControladorVotacao import ControladorVotacao
from Controladores.ControladorCategoria import ControladorCategorias
from Excecoes.OpcaoInvalida import OpcaoInvalida


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__controlador_membros = ControladorCadastro("membro")
        self.__controlador_atores = ControladorCadastro("ator")
        self.__controlador_diretores = ControladorCadastro("diretor")
        self.__controlador_categorias = ControladorCategorias()
        self.__controlador_filmes = ControladorFilmes(self)
        self.__controlador_indicacao = ControladorIndicacao(self.__controlador_membros, self.__controlador_categorias)
        self.__controlador_votacao = ControladorVotacao(self.__controlador_membros, self.__controlador_categorias)


    def inicializa_sistema(self):
        while True:
            try:
                opcao = self.__tela_sistema.mostra_opcoes()

                if opcao == 1:
                    self.__controlador_membros.abrir_menu()
                elif opcao == 2:
                    self.__controlador_atores.abrir_menu()
                elif opcao == 3:
                    self.__controlador_diretores.abrir_menu()
                elif opcao == 4:
                    self.__controlador_filme.abre_tela()
                elif opcao == 5:
                    self.__controlador_categorias.abrir_menu()
                elif opcao == 6:
                    self.__controlador_indicacao.iniciar_indicacao()
                elif opcao == 7:
                    self.__controlador_votacao.iniciar_votacao()
                elif opcao == 0:
                    print("Saindo do sistema...")
                    break
            except OpcaoInvalida as e:
                print(e)
                input("🔁 Pressione Enter para tentar novamente...")
