from Limites.TelaSistema import TelaSistema
from Controladores.ControladorFilme import ControladorFilmes
from Controladores.ControladorCadastro import ControladorCadastro
from Controladores.ControladorIndicacao import ControladorIndicacao
from Controladores.ControladorVotacao import ControladorVotacao
from Controladores.ControladorCategoria import ControladorCategorias


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema()
        # Controladores genéricos para entidades simples
        self.__controlador_membros = ControladorCadastro("membro")
        self.__controlador_atores = ControladorCadastro("ator")
        self.__controlador_diretores = ControladorCadastro("diretor")
        self.__controlador_categorias = ControladorCategorias()

        # Controladores específicos para entidades com regras próprias
        # Criar controlador filmes, passando self caso precise (ajuste se necessário)
        self.__controlador_filmes = ControladorFilmes(self)

        # Criar controlador indicacao e votacao, passando membros e categorias (essenciais)
        self.__controlador_indicacao = ControladorIndicacao(self.__controlador_membros, self.__controlador_categorias)
        self.__controlador_votacao = ControladorVotacao(self.__controlador_membros, self.__controlador_categorias)


    def inicializa_sistema(self):
        while True:
            opcao = self.__tela_sistema.mostra_opcoes()

            if opcao == 1:
                self.__controlador_membros.abrir_menu()
            elif opcao == 2:
                self.__controlador_atores.abrir_menu()
            elif opcao == 3:
                self.__controlador_diretores.abrir_menu()
            elif opcao == 4:
                self.__controlador_filmes.abre_tela()
            elif opcao == 5:
                self.__controlador_categorias.abrir_menu()
            elif opcao == 6:
                self.__controlador_indicacao.iniciar_indicacao()
            elif opcao == 7:
                self.__controlador_votacao.iniciar_votacao()
            elif opcao == 0:
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida.")
