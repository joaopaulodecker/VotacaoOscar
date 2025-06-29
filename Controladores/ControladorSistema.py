from Limites.TelaSistema import TelaSistema
from Controladores.ControladorFilme import ControladorFilmes
from Controladores.ControladorMembros import ControladorMembros
from Controladores.ControladorIndicacao import ControladorIndicacao
from Controladores.ControladorVotacao import ControladorVotacao
from Controladores.ControladorCategoria import ControladorCategorias


class ControladorSistema:
    """Controlador principal que orquestra todo o sistema."""
    # Constantes para as fases, evitando erros de digitação
    FASE_INDICACOES_ABERTAS = "INDICAÇÕES ABERTAS"
    FASE_VOTACAO_ABERTA = "VOTAÇÃO ABERTA"
    FASE_PREMIACAO_CONCLUIDA = "PREMIAÇÃO CONCLUÍDA"

    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__fase_atual_premiacao = self.FASE_INDICACOES_ABERTAS

        # Inicializa todos os outros controladores
        self.__controlador_membros = ControladorMembros(self)
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
    def fase_atual_premiacao(self) -> str:
        return self.__fase_atual_premiacao

    def encerrar_indicacoes_abrir_votacao(self):
        """Altera a fase da premiação de Indicações para Votação."""
        if self.__fase_atual_premiacao == self.FASE_INDICACOES_ABERTAS:
            self.__fase_atual_premiacao = self.FASE_VOTACAO_ABERTA
            self.__tela_sistema.show_message("Fase Alterada", "✅ Período de indicações encerrado. Votação liberada!")
        elif self.__fase_atual_premiacao == self.FASE_VOTACAO_ABERTA:
            self.__tela_sistema.show_message("Aviso", "ℹ️ A votação já está aberta.")
        else:
            self.__tela_sistema.show_message("Aviso", "ℹ️ A premiação já foi concluída.")

    def inicializa_sistema(self):
        """Metodo principal que abre o menu e gerencia o loop de eventos."""
        self.__tela_sistema.init_components(self.fase_atual_premiacao)

        menu_opcoes = {
            '-MEMBROS-': self.__controlador_membros.abre_tela,
            '-FILMES-': self.__controlador_filmes.abre_tela,
            '-CATEGORIAS-': self.__controlador_categorias.abre_tela,
            '-INDICACOES-': self.__controlador_indicacao.abre_tela,
            '-VOTACAO-': self.__controlador_votacao.abre_tela,
            # --- CORREÇÃO APLICADA AQUI ---
            # O botão de resultados agora chama o metodo correto do controlador de votação.
            '-RESULTADOS-': self.__controlador_votacao.mostrar_resultados_gui,
        }

        while True:
            event, values = self.__tela_sistema.open()

            if event in (None, '-SAIR-'):
                break

            # Chama a função correspondente ao botão clicado
            if event in menu_opcoes:
                metodo_a_chamar = menu_opcoes[event]
                metodo_a_chamar()

            elif event == '-AVANCAR_FASE-':
                self.encerrar_indicacoes_abrir_votacao()
                # Atualiza o texto da fase na tela
                self.__tela_sistema.update_fase(self.fase_atual_premiacao)

        self.__tela_sistema.close()