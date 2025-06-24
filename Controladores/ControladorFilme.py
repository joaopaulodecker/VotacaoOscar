from Entidades.Filme import Filme
from Entidades.Nacionalidade import Nacionalidade
from Limites.TelaFilme import TelaFilmes
from Excecoes.EntidadeDuplicadaException import EntidadeDuplicadaException
from DAOs.filme_dao import FilmeDAO

class ControladorFilmes:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__dao = FilmeDAO()
        self.__tela_filmes = TelaFilmes()

    @property
    def filmes(self):
        return self.__dao.get_all()

    def _gerar_proximo_id(self):
        todos_os_filmes = self.__dao.get_all()
        if not todos_os_filmes:
            return 1
        return max(filme.id_filme for filme in todos_os_filmes) + 1

    def buscar_filme_por_id(self, id_filme_param: int):
        return self.__dao.get(id_filme_param)

    def existe_titulo_filme(self, titulo, id_excluir=None):
        for filme in self.__dao.get_all():
            if id_excluir is not None and filme.id_filme == id_excluir:
                continue
            if filme.titulo.casefold() == titulo.casefold():
                return True
        return False

    def abre_tela(self):
        diretores = self.__controlador_sistema.controlador_membros.buscar_por_funcao_e_genero("diretor")
        mapa_diretores = {d.id: d.nome for d in diretores}

        self.__tela_filmes.init_components_lista(self.filmes, mapa_diretores)
        
        while True:
            event, values = self.__tela_filmes.open_lista()

            if event in (None, '-VOLTAR-'):
                break

            if event == '-ADICIONAR-':
                self.cadastrar()
            elif event == '-AGRUPAR-':
                self.listar_filmes_agrupados_por_nacionalidade()
            elif values['-TABELA-']:
                index_selecionado = values['-TABELA-'][0]
                filme_selecionado = self.filmes[index_selecionado]

                if event == '-EDITAR-':
                    self.alterar(filme_selecionado)
                elif event == '-EXCLUIR-':
                    self.excluir(filme_selecionado)
            elif event in ('-EDITAR-', '-EXCLUIR-'):
                self.__tela_filmes.show_message("Aviso", "Por favor, selecione um filme na tabela primeiro.")
        
        self.__tela_filmes.close_lista()

    def cadastrar(self):
        diretores_disponiveis = self.__controlador_sistema.controlador_membros.buscar_por_funcao_e_genero("diretor")
        if not diretores_disponiveis:
            self.__tela_filmes.show_message("Erro", "É necessário cadastrar um diretor antes de poder cadastrar um filme.")
            return

        dados_filme = self.__tela_filmes.pega_dados_filme(diretores_disponiveis)
        if dados_filme:
            if self.existe_titulo_filme(dados_filme["-TITULO-"]):
                self.__tela_filmes.show_message("Erro", f"❌ Já existe um filme com o título '{dados_filme['-TITULO-']}'.")
                return

            novo_id = self._gerar_proximo_id()
            novo_filme = Filme(id_filme=novo_id,
                               titulo=dados_filme["-TITULO-"],
                               ano=dados_filme["-ANO-"],
                               diretor_id=dados_filme["-DIRETOR_ID-"],
                               nacionalidade=Nacionalidade(dados_filme["-NACIONALIDADE-"]))
            
            self.__dao.add(novo_filme)
            self.__tela_filmes.show_message("Sucesso", f"✅ Filme '{novo_filme.titulo}' cadastrado.")
            
            mapa_diretores = {d.id: d.nome for d in diretores_disponiveis}
            self.__tela_filmes.refresh_table(self.filmes, mapa_diretores)

    def alterar(self, filme_alvo: Filme):
        diretores_disponiveis = self.__controlador_sistema.controlador_membros.buscar_por_funcao_e_genero("diretor")
        dados_atuais = {
            'titulo': filme_alvo.titulo, 'ano': filme_alvo.ano, 
            'nacionalidade_str': filme_alvo.nacionalidade.pais, 'diretor_id': filme_alvo.diretor_id
        }

        novos_dados = self.__tela_filmes.pega_dados_filme(diretores_disponiveis, dados_atuais=dados_atuais)
        if novos_dados:
            if (filme_alvo.titulo.casefold() != novos_dados["-TITULO-"].casefold() and
                    self.existe_titulo_filme(novos_dados["-TITULO-"], id_excluir=filme_alvo.id_filme)):
                self.__tela_filmes.show_message("Erro", f"❌ Já existe outro filme com o título '{novos_dados['-TITULO-']}'.")
                return
            
            filme_alvo.titulo = novos_dados["-TITULO-"]
            filme_alvo.ano = novos_dados["-ANO-"]
            filme_alvo.diretor_id = novos_dados["-DIRETOR_ID-"]
            filme_alvo.nacionalidade = Nacionalidade(novos_dados["-NACIONALIDADE-"])
            
            self.__dao.add(filme_alvo)
            self.__tela_filmes.show_message("Sucesso", "✅ Filme alterado com sucesso!")
            
            mapa_diretores = {d.id: d.nome for d in diretores_disponiveis}
            self.__tela_filmes.refresh_table(self.filmes, mapa_diretores)

    def excluir(self, filme_alvo: Filme):
        confirmado = self.__tela_filmes.show_confirm_message(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o filme '{filme_alvo.titulo}'?"
        )
        if confirmado == 'Yes':
            self.__dao.remove(filme_alvo.id_filme)
            self.__tela_filmes.show_message("Sucesso", "🗑️ Filme removido com sucesso.")
            
            diretores = self.__controlador_sistema.controlador_membros.buscar_por_funcao_e_genero("diretor")
            mapa_diretores = {d.id: d.nome for d in diretores}
            self.__tela_filmes.refresh_table(self.filmes, mapa_diretores)

    def listar_filmes_agrupados_por_nacionalidade(self):
        todos_os_filmes = self.filmes
        if not todos_os_filmes:
            self.__tela_filmes.show_message("Aviso", "📭 Nenhum filme cadastrado.")
            return

        diretores = self.__controlador_sistema.controlador_membros.buscar_por_funcao_e_genero("diretor")
        mapa_diretores = {d.id: d.nome for d in diretores}
        
        filmes_por_nacionalidade = {}
        for filme_obj in todos_os_filmes:
            pais = filme_obj.nacionalidade.pais if filme_obj.nacionalidade else "Desconhecida"
            if pais not in filmes_por_nacionalidade:
                filmes_por_nacionalidade[pais] = []
            
            dados_filme = {
                "id": filme_obj.id_filme, "titulo": filme_obj.titulo, "ano": filme_obj.ano,
                "diretor": mapa_diretores.get(filme_obj.diretor_id, "N/A")
            }
            filmes_por_nacionalidade[pais].append(dados_filme)
        
        self.__tela_filmes.mostra_filmes_agrupados(filmes_por_nacionalidade)