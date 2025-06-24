from Entidades.Filme import Filme
from Entidades.Nacionalidade import Nacionalidade
from Limites.TelaFilme import TelaFilmes 
from Excecoes.OpcaoInvalida import OpcaoInvalida
from Excecoes.EntidadeDuplicadaException import EntidadeDuplicadaException
from DAOs.filme_dao import FilmeDAO

class ControladorFilmes:
    def __init__(self, controlador_sistema):
        self.__dao = FilmeDAO()
        self.__tela_filmes = TelaFilmes()
        self.__controlador_sistema = controlador_sistema

    @property
    def filmes(self):
        return self.__dao.get_all()

    def _gerar_proximo_id(self):
        todos_os_filmes = self.__dao.get_all()
        if not todos_os_filmes:
            return 1
        
        maior_id = max(filme.id_filme for filme in todos_os_filmes)
        return maior_id + 1

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
            except EntidadeDuplicadaException as e:
                self.__tela_filmes.mostra_mensagem(str(e))
                self.__tela_filmes.espera_input()
            except OpcaoInvalida as e:
                self.__tela_filmes.mostra_mensagem(f"❌ Ocorreu um erro: {e}")
                self.__tela_filmes.espera_input()
            except Exception as e:
                self.__tela_filmes.mostra_mensagem(f"❌ Ocorreu um erro inesperado: {e}")
                self.__tela_filmes.espera_input()

    def cadastrar(self):
        lista_diretores = self.__controlador_sistema.controlador_membros.buscar_por_funcao_e_genero("diretor")

        dados_filmes = self.__tela_filmes.pega_dados_filme(diretores_disponiveis=lista_diretores)
        
        if dados_filmes is None:
            self.__tela_filmes.mostra_mensagem("ℹ️ Cadastro cancelado.")
            self.__tela_filmes.espera_input()
            return
        
        if self.existe_titulo_filme(dados_filmes["titulo"]):
            raise EntidadeDuplicadaException(f"❌ Já existe um filme com o título '{dados_filmes['titulo']}'.")

        novo_id = self._gerar_proximo_id()
        nacionalidade_obj = Nacionalidade(dados_filmes["nacionalidade_str"])
        novo_filme = Filme(id_filme=novo_id,
                               titulo=dados_filmes["titulo"],
                               ano=dados_filmes["ano"],
                               diretor_id=dados_filmes["diretor_id"],
                               nacionalidade=nacionalidade_obj)

        self.__dao.add(novo_filme)
        self.__tela_filmes.mostra_mensagem(f"✅ Filme '{novo_filme.titulo}' cadastrado com sucesso!")
        self.__tela_filmes.espera_input()

    def _preparar_dados_filme_para_tela(self, filme_obj, indice=None):
        ctrl_membros = self.__controlador_sistema.controlador_membros
        diretor_obj = ctrl_membros.buscar_por_id(filme_obj.diretor_id)
        nome_diretor = diretor_obj.nome if diretor_obj else f"ID {filme_obj.diretor_id} não encontrado"
        
        pais_nacionalidade = filme_obj.nacionalidade.pais if filme_obj.nacionalidade else "N/A"

        return {
            "id": filme_obj.id_filme, "titulo": filme_obj.titulo, "ano": filme_obj.ano,
            "nacionalidade": pais_nacionalidade, "diretor": nome_diretor,
            "com_indice": indice is not None, "indice": indice
        }

    def listar(self, mostrar_msg_voltar=False):
        todos_os_filmes = self.__dao.get_all()
        dados_para_tela = []

        for filme in todos_os_filmes:
            diretor_obj = self.__controlador_sistema.controlador_membros.buscar_por_id(filme.diretor_id)
            diretor_nome = diretor_obj.nome if diretor_obj else "Nao encontrado"
            nacionalidade_nome = filme.nacionalidade.pais

            dados_para_tela.append({
                "id": filme.id_filme, "titulo": filme.titulo, "ano": filme.ano, 
                "diretor_nome": diretor_nome, "nacionalidade": nacionalidade_nome
            })

        self.__tela_filmes.mostra_lista_filmes(dados_para_tela)
        if mostrar_msg_voltar:
            self.__tela_filmes.espera_input()

        return bool(todos_os_filmes)

    def listar_filmes_agrupados_por_nacionalidade(self, mostrar_msg_voltar=True):
        todos_os_filmes = self.__dao.get_all()
        if not todos_os_filmes:
            self.__tela_filmes.mostra_mensagem("📭 Nenhum filme cadastrado.")
            if mostrar_msg_voltar:
                self.__tela_filmes.espera_input()
            return

        filmes_por_nacionalidade = {}
        for filme_obj in todos_os_filmes:
            pais = filme_obj.nacionalidade.pais if filme_obj.nacionalidade else "Desconhecida"
            
            if pais not in filmes_por_nacionalidade:
                filmes_por_nacionalidade[pais] = []
            
            dados_filme = self._preparar_dados_filme_para_tela(filme_obj)
            filmes_por_nacionalidade[pais].append(dados_filme)
        
        self.__tela_filmes.mostra_filmes_agrupados(filmes_por_nacionalidade)
        if mostrar_msg_voltar:
            self.__tela_filmes.espera_input()

    def alterar(self):
        if not self.listar():
                 self.__tela_filmes.mostra_mensagem("📭 Nenhum filme cadastrado para alterar.")
                 self.__tela_filmes.espera_input()
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

        lista_diretores = self.__controlador_sistema.controlador_membros.buscar_por_funcao_e_genero("diretor")
        dados_atuais_para_tela = {
            "titulo": filme_alvo.titulo, 
            "ano": filme_alvo.ano,
            "diretor_id": filme_alvo.diretor_id,
            "nacionalidade_str": filme_alvo.nacionalidade.pais if filme_alvo.nacionalidade else ""
        }
        
        novos_dados = self.__tela_filmes.pega_dados_filme(dados_atuais=dados_atuais_para_tela, diretores_disponiveis=lista_diretores)

        if not novos_dados:
            self.__tela_filmes.mostra_mensagem("ℹ️ Nenhuma alteração realizada.")
            self.__tela_filmes.espera_input()
            return
        
        if self.existe_titulo_filme(novos_dados["titulo"], id_excluir=filme_alvo.id_filme):
            self.__tela_filmes.mostra_mensagem(f"❌ Já existe outro filme com o título '{novos_dados['titulo']}'.")
            self.__tela_filmes.espera_input()
            return

        filme_alvo.titulo = novos_dados["titulo"]
        filme_alvo.ano = novos_dados["ano"]
        filme_alvo.diretor_id = novos_dados["diretor_id"]
        filme_alvo.nacionalidade = Nacionalidade(novos_dados["nacionalidade_str"])
        
        self.__dao.add(filme_alvo)
        
        self.__tela_filmes.mostra_mensagem("✅ Filme alterado com sucesso!")
        self.__tela_filmes.espera_input()

    def excluir(self):
        if not self.listar():
                 self.__tela_filmes.mostra_mensagem("📭 Nenhum filme cadastrado para excluir.")
                 self.__tela_filmes.espera_input()
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
            self.__dao.remove(filme_alvo.id_filme)
            self.__tela_filmes.mostra_mensagem("🗑️ Filme removido com sucesso.")
        else:
            self.__tela_filmes.mostra_mensagem("ℹ️ Exclusão cancelada pelo usuário.")
        self.__tela_filmes.espera_input()