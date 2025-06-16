from Entidades.Filme import Filme
from Entidades.Nacionalidade import Nacionalidade
from Limites.TelaFilme import TelaFilmes 
from Excecoes.OpcaoInvalida import OpcaoInvalida

class ControladorFilmes:
    def __init__(self, controlador_sistema):
        self.__filmes = []
        self.__tela_filmes = TelaFilmes()
        self.__controlador_sistema = controlador_sistema
        self.__proximo_id = 1

    @property
    def filmes(self):
        return self.__filmes

    def _gerar_proximo_id(self):
        id_atual = self.__proximo_id
        self.__proximo_id += 1
        return id_atual

    def buscar_filme_por_id(self, id_filme_param):
        for filme in self.__filmes:
            if filme.id_filme == id_filme_param:
                return filme
        return None

    def existe_titulo_filme(self, titulo, id_excluir=None):
        for filme in self.__filmes:
            if id_excluir is not None and filme.id_filme == id_excluir:
                continue
            if filme.titulo.casefold() == titulo.casefold():
                return True
        return False

    def abre_tela(self):
        while True:
            try:
                opcao = self.__tela_filmes.mostra_opcoes()
                if opcao == 1:
                    self.cadastrar()
                elif opcao == 2:
                    self.alterar()
                elif opcao == 3:
                    self.excluir()
                elif opcao == 4:
                    self.listar(mostrar_msg_voltar=True)
                elif opcao == 5:
                    self.listar_filmes_agrupados_por_nacionalidade(mostrar_msg_voltar=True)
                elif opcao == 0:
                    break
            except OpcaoInvalida as e:
                self.__tela_filmes.mostra_mensagem(f"❌ {e}")
                self.__tela_filmes.espera_input()
            except Exception as e:
                self.__tela_filmes.mostra_mensagem(f"❌ Ocorreu um erro inesperado: {e}")
                self.__tela_filmes.espera_input()

    def cadastrar(self):
        lista_diretores = self.__controlador_sistema.controlador_membros.buscar_por_funcao("diretor")
        dados = self.__tela_filmes.le_dados_filme(diretores_disponiveis=lista_diretores)
        
        if not dados or not all(k in dados for k in ["titulo", "ano", "nacionalidade_str", "diretor_id"]):
            self.__tela_filmes.mostra_mensagem("❌ Cadastro cancelado. Dados incompletos.")
            self.__tela_filmes.espera_input()
            return

        if self.existe_titulo_filme(dados["titulo"]):
            self.__tela_filmes.mostra_mensagem(f"❌ Já existe um filme com o título '{dados['titulo']}'.")
            self.__tela_filmes.espera_input()
            return
        
        novo_id = self._gerar_proximo_id()
        nacionalidade_obj = Nacionalidade(dados["nacionalidade_str"])
        
        filme = Filme(id_filme=novo_id, 
                      titulo=dados["titulo"], 
                      ano=dados["ano"], 
                      diretor_id=dados["diretor_id"],
                      nacionalidade=nacionalidade_obj)
        self.__filmes.append(filme)
        
        self.__tela_filmes.mostra_mensagem(f"✅ Filme '{filme.titulo}' cadastrado com sucesso!")
        self.__tela_filmes.espera_input()

    def _preparar_dados_filme_para_tela(self, filme_obj, indice=None):
        """Helper para criar um dicionário de dados de um filme para a tela."""
        ctrl_membros = self.__controlador_sistema.controlador_membros
        nome_diretor = f"ID {filme_obj.diretor_id}"
        if ctrl_membros and hasattr(ctrl_membros, 'buscar_por_id'):
            diretor_dict = ctrl_membros.buscar_por_id(filme_obj.diretor_id)
            if diretor_dict and diretor_dict.get('nome'):
                nome_diretor = diretor_dict.get('nome')

        pais_nacionalidade = "N/A"
        if filme_obj.nacionalidade and hasattr(filme_obj.nacionalidade, 'pais'):
            pais_nacionalidade = filme_obj.nacionalidade.pais

        dados_para_tela = {
            "id": filme_obj.id_filme,
            "titulo": filme_obj.titulo,
            "ano": filme_obj.ano,
            "nacionalidade": pais_nacionalidade,
            "diretor": nome_diretor,
            "com_indice": indice is not None,
            "indice": indice
        }
        return dados_para_tela

    def listar(self, mostrar_msg_voltar=False, com_indices=False):
        if not self.__filmes:
            self.__tela_filmes.mostra_mensagem("📭 Nenhum filme cadastrado.")
        else:
            lista_para_tela = []
            for i, filme in enumerate(self.__filmes):
                dados_filme = self._preparar_dados_filme_para_tela(filme, indice=i + 1 if com_indices else None)
                lista_para_tela.append(dados_filme)
            self.__tela_filmes.mostra_lista_filmes(lista_para_tela)
        
        if mostrar_msg_voltar:
            self.__tela_filmes.espera_input()

    def listar_filmes_agrupados_por_nacionalidade(self, mostrar_msg_voltar=True):
        if not self.__filmes:
            self.__tela_filmes.mostra_mensagem("📭 Nenhum filme cadastrado.")
            if mostrar_msg_voltar:
                self.__tela_filmes.espera_input()
            return

        filmes_por_nacionalidade = {}
        for filme_obj in self.__filmes:
            pais = "Desconhecida"
            if filme_obj.nacionalidade and hasattr(filme_obj.nacionalidade, 'pais'):
                pais = filme_obj.nacionalidade.pais
            
            if pais not in filmes_por_nacionalidade:
                filmes_por_nacionalidade[pais] = []
            
            dados_filme = self._preparar_dados_filme_para_tela(filme_obj)
            filmes_por_nacionalidade[pais].append(dados_filme)
        
        self.__tela_filmes.mostra_filmes_agrupados(filmes_por_nacionalidade)
        
        if mostrar_msg_voltar:
            self.__tela_filmes.espera_input()

    def alterar(self):
        self.listar(com_indices=False)
        if not self.__filmes:
            return

        id_alvo = self.__tela_filmes.seleciona_filme_por_id()
        if id_alvo is None:
            self.__tela_filmes.mostra_mensagem("ℹ️ Alteração cancelada.")
            self.__tela_filmes.espera_input()
            return

        filme_alvo = self.buscar_filme_por_id(id_alvo)
        if not filme_alvo:
            self.__tela_filmes.mostra_mensagem(f"❌ Filme com ID {id_alvo} não encontrado.")
            self.__tela_filmes.espera_input()
            return
        
        dados_preparados = self._preparar_dados_filme_para_tela(filme_alvo)
        self.__tela_filmes.mostra_mensagem(f"\nEditando filme: ID {dados_preparados['id']} - '{dados_preparados['titulo']}'")

        lista_diretores = self.__controlador_sistema.controlador_membros.buscar_por_funcao("diretor")
        dados_atuais_para_tela = {
            "titulo": filme_alvo.titulo, 
            "ano": filme_alvo.ano,
            "diretor_id": filme_alvo.diretor_id,
            "nacionalidade_str": filme_alvo.nacionalidade.pais if filme_alvo.nacionalidade else ""
        }
        
        novos_dados = self.__tela_filmes.le_dados_filme(dados_atuais=dados_atuais_para_tela, diretores_disponiveis=lista_diretores)

        if not novos_dados:
            self.__tela_filmes.mostra_mensagem("ℹ️ Nenhuma alteração realizada.")
            self.__tela_filmes.espera_input()
            return
        
        filme_alvo.titulo = novos_dados["titulo"]
        filme_alvo.ano = novos_dados["ano"]
        filme_alvo.diretor_id = novos_dados["diretor_id"]
        filme_alvo.nacionalidade = Nacionalidade(novos_dados["nacionalidade_str"])

        self.__tela_filmes.mostra_mensagem("✅ Filme alterado com sucesso!")
        self.__tela_filmes.espera_input()

    def excluir(self):
        self.listar(com_indices=False)
        if not self.__filmes:
            return

        id_alvo = self.__tela_filmes.seleciona_filme_por_id()
        if id_alvo is None:
            self.__tela_filmes.mostra_mensagem("ℹ️ Exclusão cancelada.")
            self.__tela_filmes.espera_input()
            return
            
        filme_alvo = self.buscar_filme_por_id(id_alvo)
        if not filme_alvo:
            self.__tela_filmes.mostra_mensagem(f"❌ Filme com ID {id_alvo} não encontrado.")
            self.__tela_filmes.espera_input()
            return
        
        if self.__tela_filmes.confirma_exclusao(filme_alvo.titulo):
            self.__filmes.remove(filme_alvo)
            self.__tela_filmes.mostra_mensagem("🗑️ Filme removido com sucesso.")
        else:
            self.__tela_filmes.mostra_mensagem("ℹ️ Exclusão cancelada pelo usuário.")
        self.__tela_filmes.espera_input()