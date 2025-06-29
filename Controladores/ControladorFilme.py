from Entidades.Filme import Filme
from Entidades.Nacionalidade import Nacionalidade
from Limites.TelaFilme import TelaFilmes
from DAOs.FilmeDao import FilmeDAO


class ControladorFilmes:
    """O cérebro por trás de todas as operações de Filmes."""

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__dao = FilmeDAO()
        self.__tela_filmes = TelaFilmes()

    def _preparar_dados_tabela(self):
        """Busca os filmes e formata os dados para a tabela da interface."""
        filmes = self.__dao.get_all()
        mapa_diretores = {d.id: d.nome for d in self.__controlador_sistema.controlador_membros.membros}

        dados_tabela = []
        for filme in filmes:
            nome_diretor = mapa_diretores.get(filme.diretor_id, "ID não encontrado")
            dados_tabela.append(
                [filme.id_filme, filme.titulo, filme.ano_lancamento, filme.nacionalidade.pais, nome_diretor])
        return dados_tabela

    def buscar_filme_por_id(self, id_filme: int):
        """Pega um filme específico pelo seu ID."""
        return self.__dao.get(id_filme)

    def existe_titulo_filme(self, titulo: str, id_excluir: int = None):
        """Verifica no banco se um filme com o mesmo título já existe."""
        for filme in self.__dao.get_all():
            if id_excluir is not None and filme.id_filme == id_excluir:
                continue
            if filme.titulo.casefold() == titulo.casefold():
                return True
        return False

    def abre_tela(self):
        """Inicia e gerencia a tela principal do módulo de Filmes."""
        dados_tabela = self._preparar_dados_tabela()
        self.__tela_filmes.init_components_lista(dados_tabela)

        while True:
            event, values = self.__tela_filmes.open_lista()
            if event in (None, '-VOLTAR-'):
                break

            if event == '-ADICIONAR-':
                self.cadastrar()
            elif event == '-AGRUPAR-':
                self.listar_filmes_agrupados_por_nacionalidade()
            elif values.get('-TABELA-'):
                index_selecionado = values['-TABELA-'][0]
                id_filme_selecionado = dados_tabela[index_selecionado][0]
                filme_alvo = self.buscar_filme_por_id(id_filme_selecionado)
                if not filme_alvo: continue

                if event == '-EDITAR-':
                    self.alterar(filme_alvo)
                elif event == '-EXCLUIR-':
                    self.excluir(filme_alvo)
            elif event in ('-EDITAR-', '-EXCLUIR-'):
                self.__tela_filmes.show_message("Aviso", "Por favor, selecione um filme na tabela primeiro.")

            # Sempre atualiza a tabela para o usuário ver as mudanças na hora.
            dados_tabela = self._preparar_dados_tabela()
            self.__tela_filmes.refresh_table(dados_tabela)

        self.__tela_filmes.close_lista()

    def cadastrar(self):
        """Orquestra o processo de cadastro de um novo filme."""
        diretores_obj = self.__controlador_sistema.controlador_membros.buscar_por_funcao_e_genero("diretor")
        if not diretores_obj:
            self.__tela_filmes.show_message("Erro", "É necessário cadastrar um diretor antes.")
            return

        diretores_para_combo = [f"ID: {d.id} - {d.nome}" for d in diretores_obj]
        dados_brutos = self.__tela_filmes.pega_dados_filme(diretores_para_combo, {'titulo_janela': "Adicionar Filme"})

        if dados_brutos:
            # Aqui o Controlador valida os dados brutos que vieram da Tela.
            erros = []
            titulo = dados_brutos['-TITULO-']
            ano_str = dados_brutos['-ANO-']
            nacionalidade = dados_brutos['-NACIONALIDADE-']
            diretor_str = dados_brutos['-DIRETOR-']

            if not titulo.strip(): erros.append("O campo 'Título' é obrigatório.")
            if self.existe_titulo_filme(titulo): erros.append(f"Já existe um filme com o título '{titulo}'.")
            if not nacionalidade.strip(): erros.append("O campo 'Nacionalidade' é obrigatório.")
            if not diretor_str: erros.append("A seleção de um 'Diretor' é obrigatória.")

            ano_int = None
            try:
                ano_int = int(ano_str)
                if not (1888 <= ano_int <= 2030): erros.append("O 'Ano' deve ser um valor realista.")
            except (ValueError, TypeError):
                erros.append("O 'Ano' deve ser um número inteiro válido.")

            if erros:
                self.__tela_filmes.show_message("Erros de Validação", "\n".join(erros))
                return

            id_diretor = int(diretor_str.split(' ')[1])
            novo_id = self.__dao.get_next_id()
            novo_filme = Filme(id_filme=novo_id,
                               titulo=titulo.strip(),
                               ano_lancamento=ano_int,
                               diretor_id=id_diretor,
                               nacionalidade=Nacionalidade(nacionalidade.strip()))

            self.__dao.add(key=novo_id, filme=novo_filme)
            self.__tela_filmes.show_message("Sucesso", f"Filme '{novo_filme.titulo}' cadastrado.")

    def alterar(self, filme_alvo: Filme):
        """Orquestra a alteração de um filme que já existe."""
        diretores_obj = self.__controlador_sistema.controlador_membros.buscar_por_funcao_e_genero("diretor")
        diretores_para_combo = [f"ID: {d.id} - {d.nome}" for d in diretores_obj]
        diretor_atual_str = ""
        for s in diretores_para_combo:
            if f"ID: {filme_alvo.diretor_id}" in s:
                diretor_atual_str = s
                break

        dados_iniciais = {
            'titulo_janela': "Editar Filme", 'titulo': filme_alvo.titulo,
            'ano': str(filme_alvo.ano_lancamento), 'nacionalidade_str': filme_alvo.nacionalidade.pais,
            'diretor_str': diretor_atual_str
        }
        dados_brutos = self.__tela_filmes.pega_dados_filme(diretores_para_combo, dados_iniciais)

        if dados_brutos:
            # A validação completa também é feita na alteração, para máxima segurança.
            erros = []
            titulo = dados_brutos['-TITULO-']
            ano_str = dados_brutos['-ANO-']

            if filme_alvo.titulo.casefold() != titulo.casefold() and self.existe_titulo_filme(titulo):
                erros.append(f"Já existe outro filme com o título '{titulo}'.")

            ano_int = None
            try:
                ano_int = int(ano_str)
                if not (1888 <= ano_int <= 2030): erros.append("O 'Ano' deve ser um valor realista.")
            except (ValueError, TypeError):
                erros.append("O 'Ano' deve ser um número inteiro válido.")

            if erros:
                self.__tela_filmes.show_message("Erros de Validação", "\n".join(erros))
                return

            filme_alvo.titulo = titulo.strip()
            filme_alvo.ano_lancamento = ano_int
            filme_alvo.diretor_id = int(dados_brutos["-DIRETOR-"].split(' ')[1])
            filme_alvo.nacionalidade = Nacionalidade(dados_brutos["-NACIONALIDADE-"].strip())

            self.__dao.add(key=filme_alvo.id_filme, filme=filme_alvo)
            self.__tela_filmes.show_message("Sucesso", "Filme alterado com sucesso!")

    def excluir(self, filme_alvo: Filme):
        """Orquestra a exclusão de um filme, com confirmação."""
        confirmado = self.__tela_filmes.show_confirm_message("Confirmar Exclusão",
                                                             f"Tem certeza que deseja excluir '{filme_alvo.titulo}'?")
        if confirmado == 'Yes':
            self.__dao.remove(filme_alvo.id_filme)
            self.__tela_filmes.show_message("Sucesso", "Filme removido com sucesso.")

    def listar_filmes_agrupados_por_nacionalidade(self):
        """Busca, agrupa e formata os filmes por nacionalidade."""
        todos_os_filmes = self.__dao.get_all()
        if not todos_os_filmes:
            self.__tela_filmes.show_message("Aviso", "Nenhum filme cadastrado.")
            return

        mapa_diretores = {d.id: d.nome for d in self.__controlador_sistema.controlador_membros.membros}
        filmes_por_nacionalidade = {}
        for filme in todos_os_filmes:
            pais = filme.nacionalidade.pais
            if pais not in filmes_por_nacionalidade: filmes_por_nacionalidade[pais] = []
            diretor = mapa_diretores.get(filme.diretor_id, "N/A")
            filmes_por_nacionalidade[pais].append(f"  - {filme.titulo} ({filme.ano_lancamento}) (Dir: {diretor})")

        # Aqui o Controlador monta a string final para a tela apenas exibir.
        texto_final = ""
        for pais, lista_filmes in sorted(filmes_por_nacionalidade.items()):
            texto_final += f"🌍 Nacionalidade: {pais}\n" + "-" * 30 + "\n"
            texto_final += "\n".join(lista_filmes) + "\n\n"

        self.__tela_filmes.mostra_filmes_agrupados(texto_final)