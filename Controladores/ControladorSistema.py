from Limites.TelaSistema import TelaSistema
from Controladores.ControladorFilme import ControladorFilmes
from Controladores.ControladorMembros import ControladorMembros
from Controladores.ControladorIndicacao import ControladorIndicacao
from Controladores.ControladorVotacao import ControladorVotacao
from Controladores.ControladorCategoria import ControladorCategorias

class ControladorSistema:
    FASE_INDICACOES_ABERTAS = "FASE_INDICACOES_ABERTAS"
    FASE_VOTACAO_ABERTA = "FASE_VOTACAO_ABERTA"
    FASE_PREMIACAO_CONCLUIDA = "FASE_PREMIACAO_CONCLUIDA"

    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__fase_atual_premiacao = ControladorSistema.FASE_INDICACOES_ABERTAS

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
            self.__tela_sistema.show_message("Fase Alterada", "✅ Período de indicações encerrado. Votação liberada!")
        elif self.__fase_atual_premiacao == ControladorSistema.FASE_VOTACAO_ABERTA:
            self.__tela_sistema.show_message("Aviso", "ℹ️ A votação já está aberta.")
        else:
            self.__tela_sistema.show_message("Aviso", "ℹ️ A premiação já foi concluída.")

    def _listar_membros_por_funcao(self, funcao: str, titulo: str):
        membros_encontrados = self.__controlador_membros.buscar_por_funcao_e_genero(funcao)
        lista_formatada = [f"ID: {m.id} | Nome: {m.nome}" for m in membros_encontrados]
        
        texto_lista = "\n".join(lista_formatada) if lista_formatada else "(Nenhum item encontrado)"
        
        self.__tela_sistema.show_message(titulo, texto_lista)

    def inicializa_sistema(self):
        fase_formatada = self.fase_atual_premiacao.replace('_', ' ').title()
        self.__tela_sistema.init_components(fase_formatada)

        while True:
            event, values = self.__tela_sistema.open()
            
            if event is None or event == '0':
                break

            if event == '1':
                self.__controlador_membros.abrir_menu()
            elif event == '2':
                self._listar_membros_por_funcao("ator", "🎭 Atores Cadastrados:")
            elif event == '3':
                self._listar_membros_por_funcao("diretor", "🎬 Diretores Cadastrados:")
            elif event == '4':
                self.__controlador_filmes.abre_tela()
            elif event == '5':
                self.__controlador_categorias.abrir_menu()
            elif event == '6':
                self.__controlador_indicacao.abrir_menu_indicacoes()
            elif event == '7':
                self.__controlador_votacao.abrir_menu_votacao()
            elif event == '8':
                self.__controlador_votacao.mostrar_resultados()
            elif event == '9':
                self.encerrar_indicacoes_abrir_votacao()
                nova_fase_formatada = self.fase_atual_premiacao.replace('_', ' ').title()
                self.__tela_sistema.update_fase(nova_fase_formatada)

        self.__tela_sistema.close()