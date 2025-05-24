from Limites.TelaSistema import TelaSistema
from Controladores.ControladorFilme import ControladorFilmes
from Controladores.ControladorCadastro import ControladorCadastro
from Controladores.ControladorIndicacao import ControladorIndicacao
from Controladores.ControladorVotacao import ControladorVotacao
from Controladores.ControladorCategoria import ControladorCategorias
from Excecoes.OpcaoInvalida import OpcaoInvalida

class ControladorSistema:
    FASE_INDICACOES_ABERTAS = "FASE_INDICACOES_ABERTAS"
    FASE_VOTACAO_ABERTA = "FASE_VOTACAO_ABERTA"
    FASE_PREMIACAO_CONCLUIDA = "FASE_PREMIACAO_CONCLUIDA"

    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__fase_atual_premiacao = ControladorSistema.FASE_INDICACOES_ABERTAS
        
        self.__controlador_membros = ControladorCadastro("membro")
        self.__controlador_categorias = ControladorCategorias()
        self.__controlador_filmes = ControladorFilmes(self)
        self.__controlador_indicacao = ControladorIndicacao(
            self, self.__controlador_membros, self.__controlador_categorias, self.__controlador_filmes
        )
        self.__controlador_votacao = ControladorVotacao(
            self, self.__controlador_membros, self.__controlador_categorias, 
            self.__controlador_filmes, self.__controlador_indicacao
        )

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

    @property
    def fase_atual_premiacao(self) -> str:
        return self.__fase_atual_premiacao

    def encerrar_indicacoes_abrir_votacao(self):
        if self.__fase_atual_premiacao == ControladorSistema.FASE_INDICACOES_ABERTAS:
            self.__fase_atual_premiacao = ControladorSistema.FASE_VOTACAO_ABERTA
            print("\n✅ Período de indicações encerrado. Votação liberada!")
        elif self.__fase_atual_premiacao == ControladorSistema.FASE_VOTACAO_ABERTA:
            print("\nℹ️ A votação já está aberta. As indicações já foram encerradas.")
        else:
            print("\nℹ️ A premiação já foi concluída.")
        input("🔁 Pressione Enter para continuar...")

    def inicializa_sistema(self):
        while True:
            try:
                print(f"\n--- Fase Atual: {self.fase_atual_premiacao.replace('_', ' ').title()} ---")
                opcao = self.__tela_sistema.mostra_opcoes()

                if opcao == 1:
                    self.__controlador_membros.abrir_menu()
                elif opcao == 2:
                    print("\n🎭 Atores Cadastrados:")
                    atores = self.__controlador_membros.buscar_por_funcao("ator")
                    if atores:
                        for ator in atores:
                            print(f"   ID: {ator.get('id', 'N/A')} | Nome: {ator.get('nome', 'N/A')}")
                    else:
                        print("   Nenhum ator cadastrado.")
                    input("🔁 Pressione Enter para voltar...")
                elif opcao == 3:
                    print("\n🎬 Diretores Cadastrados:")
                    diretores = self.__controlador_membros.buscar_por_funcao("diretor")
                    if diretores:
                        for diretor in diretores:
                            print(f"   ID: {diretor.get('id', 'N/A')} | Nome: {diretor.get('nome', 'N/A')}")
                    else:
                        print("   Nenhum diretor cadastrado.")
                    input("🔁 Pressione Enter para voltar...")
                elif opcao == 4:
                    self.__controlador_filmes.abre_tela()
                elif opcao == 5:
                    self.__controlador_categorias.abrir_menu()
                elif opcao == 6:
                    self.__controlador_indicacao.abrir_menu_indicacoes()
                elif opcao == 7:
                    self.__controlador_votacao.abrir_menu_votacao()
                elif opcao == 8:
                    self.__controlador_votacao.mostrar_resultados()
                elif opcao == 9:
                    self.encerrar_indicacoes_abrir_votacao()
                elif opcao == 0:
                    print("Saindo do sistema Oscar...")
                    break
                else:
                    print("❌ Opção não reconhecida pelo sistema. Tente novamente.")

            except OpcaoInvalida as e:
                print(f"❌ {e}")
                input("🔁 Pressione Enter para tentar novamente...")
            except Exception as e:
                print(f"❌ Ocorreu um erro geral no sistema: {e}")
                input("🔁 Pressione Enter para continuar...")