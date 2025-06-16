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
            self.__tela_sistema.mostra_mensagem("\n✅ Período de indicações encerrado. Votação liberada!")
        elif self.__fase_atual_premiacao == ControladorSistema.FASE_VOTACAO_ABERTA:
            self.__tela_sistema.mostra_mensagem("\nℹ️ A votação já está aberta. As indicações já foram encerradas.")
        else:
            self.__tela_sistema.mostra_mensagem("\nℹ️ A premiação já foi concluída.")
        self.__tela_sistema.espera_input()

    def _listar_membros_por_funcao(self, funcao: str, titulo: str):
        membros_encontrados = self.__controlador_membros.buscar_por_funcao(funcao)
        lista_formatada = [
            f"   ID: {membro.get('id', 'N/A')} | Nome: {membro.get('nome', 'N/A')}"
            for membro in membros_encontrados
        ]
        self.__tela_sistema.mostra_lista(titulo, lista_formatada)
        self.__tela_sistema.espera_input()

    def inicializa_sistema(self):
        while True:
            try:
                fase_formatada = self.fase_atual_premiacao.replace('_', ' ').title()
                self.__tela_sistema.mostra_mensagem(f"\n--- Fase Atual: {fase_formatada} ---")
                
                opcao = self.__tela_sistema.mostra_opcoes()

                if opcao == 1:
                    self.__controlador_membros.abrir_menu()
                elif opcao == 2:
                    self._listar_membros_por_funcao("ator", "\n🎭 Atores Cadastrados:")
                elif opcao == 3:
                    self._listar_membros_por_funcao("diretor", "\n🎬 Diretores Cadastrados:")
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
                    self.__tela_sistema.mostra_mensagem("Saindo do sistema Oscar...")
                    break
            
            except OpcaoInvalida as e:
                self.__tela_sistema.mostra_mensagem(f"❌ {e}")
                self.__tela_sistema.espera_input()
            except Exception as e:
                self.__tela_sistema.mostra_mensagem(f"❌ Ocorreu um erro geral no sistema: {e}")
                self.__tela_sistema.espera_input()