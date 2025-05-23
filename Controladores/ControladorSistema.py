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
        self.__controlador_categorias = ControladorCategorias()
        self.__controlador_filmes = ControladorFilmes(self)
        self.__controlador_indicacao = ControladorIndicacao(self.__controlador_membros, self.__controlador_categorias, self.__controlador_filmes)
        self.__controlador_votacao = ControladorVotacao(self.__controlador_membros, self.__controlador_categorias, self.__controlador_filmes, self.__controlador_indicacao)

    @property
    def controlador_membros(self):
        return self.__controlador_membros

    @property
    def controlador_categorias(self):
        return self.__controlador_categorias

    @property
    def controlador_filmes(self):
        return self.__controlador_filmes
    
    @property
    def controlador_indicacao(self):
        return self.__controlador_indicacao

    @property
    def controlador_votacao(self):
        return self.__controlador_votacao

    def inicializa_sistema(self):
        while True:
            try:
                opcao = self.__tela_sistema.mostra_opcoes()

                if opcao == 1:
                    self.__controlador_membros.abrir_menu()
                elif opcao == 2:
                    print("\n🎭 Atores Cadastrados:")
                    atores = self.__controlador_membros.buscar_por_funcao("ator")
                    if atores:
                        for ator in atores:
                            print(f"  ID: {ator.get('id', 'N/A')} | Nome: {ator.get('nome', 'N/A')}")
                    else:
                        print("  Nenhum ator cadastrado.")
                    input("🔁 Pressione Enter para voltar...")
                elif opcao == 3:
                    print("\n🎬 Diretores Cadastrados:")
                    diretores = self.__controlador_membros.buscar_por_funcao("diretor")
                    if diretores:
                        for diretor in diretores:
                            print(f"  ID: {diretor.get('id', 'N/A')} | Nome: {diretor.get('nome', 'N/A')}")
                    else:
                        print("  Nenhum diretor cadastrado.")
                    input("🔁 Pressione Enter para voltar...")
                elif opcao == 4:
                    self.__controlador_filmes.abre_tela()
                elif opcao == 5:
                    self.__controlador_categorias.abrir_menu()
                elif opcao == 6:
                    if hasattr(self.__controlador_indicacao, 'abrir_menu_indicacoes'):
                        self.__controlador_indicacao.abrir_menu_indicacoes()
                    else:
                        print("Funcionalidade de menu de indicações ainda não implementada no controlador.")
                        input("🔁 Pressione Enter para voltar...")
                elif opcao == 7:
                    if hasattr(self.__controlador_votacao, 'abrir_menu_votacao'):
                        self.__controlador_votacao.abrir_menu_votacao()
                    else:
                        print("Funcionalidade de menu de votação ainda não implementada no controlador.")
                        input("🔁 Pressione Enter para voltar...")
                elif opcao == 8:
                    self.__controlador_votacao.mostrar_resultados()
                elif opcao == 0:
                    print("Saindo do sistema Oscar...")
                    break
                else:
                    print("❌ Opção não reconhecida pelo sistema. Tente novamente.")

            except OpcaoInvalida as e:
                print(f"❌ {e}")
                input("🔁 Pressione Enter para tentar novamente...")
