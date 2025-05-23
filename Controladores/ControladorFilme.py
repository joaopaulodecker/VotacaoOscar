from Entidades.Filme import Filme
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
                elif opcao == 0:
                    break
            except OpcaoInvalida as e:
                print(f"❌ {e}")
                input("🔁 Pressione Enter para tentar novamente...")
            except Exception as e:
                print(f"❌ Ocorreu um erro inesperado no menu de filmes: {e}")
                input("🔁 Pressione Enter para continuar...")

    def cadastrar(self):
        print("\n--- Cadastro de Novo Filme ---")
        
        lista_diretores = self.__controlador_sistema.controlador_membros.buscar_por_funcao("diretor")
        
        dados = self.__tela_filmes.le_dados_filme(diretores_disponiveis=lista_diretores)
        
        if not dados or not dados.get("titulo") or dados.get("ano") is None or dados.get("diretor_id") is None:
            print("❌ Dados inválidos para cadastro. Título, ano e diretor são obrigatórios.")
            input("🔁 Pressione Enter para continuar...")
            return

        if self.existe_titulo_filme(dados["titulo"]):
            print(f"❌ Já existe um filme com o título '{dados['titulo']}'.")
            input("🔁 Pressione Enter para continuar...")
            return
        
        try:
            ano = int(dados["ano"])
            if ano <= 0:
                raise ValueError("Ano deve ser um número positivo.")
        except ValueError as e:
            print(f"❌ Ano inválido: {e}. Deve ser um número inteiro positivo.")
            input("🔁 Pressione Enter para continuar...")
            return

        novo_id = self._gerar_proximo_id()
        diretor_id_selecionado = dados["diretor_id"]
        
        filme = Filme(id_filme=novo_id, 
                      titulo=dados["titulo"], 
                      ano=ano, 
                      diretor_id=diretor_id_selecionado)
        self.__filmes.append(filme)
        
        nome_diretor = "ID " + str(diretor_id_selecionado)
        if hasattr(self.__controlador_sistema.controlador_membros, 'buscar_membro_por_id'):
            diretor_obj = self.__controlador_sistema.controlador_membros.buscar_membro_por_id(diretor_id_selecionado)
            if diretor_obj and diretor_obj.get('nome'):
                nome_diretor = diretor_obj.get('nome')
        
        print(f"✅ Filme ID {filme.id_filme} - '{filme.titulo}' ({filme.ano}), Dirigido por: {nome_diretor}, cadastrado!")
        input("🔁 Pressione Enter para continuar...")

    def listar(self, mostrar_msg_voltar=False, com_indices=False):
        if not self.__filmes:
            print("📭 Nenhum filme cadastrado.")
            if mostrar_msg_voltar:
                input("\n🔁 Pressione Enter para voltar ao menu...")
            return False
        
        print("\n--- Lista de Filmes Cadastrados ---")
        for i, filme in enumerate(self.__filmes):
            prefixo = f"{filme.id_filme}. " if not com_indices else f"{i+1}. (ID: {filme.id_filme}) "
            
            nome_diretor_str = f"(Diretor ID: {filme.diretor_id})"
            if hasattr(self.__controlador_sistema.controlador_membros, 'buscar_membro_por_id'):
                diretor_obj = self.__controlador_sistema.controlador_membros.buscar_membro_por_id(filme.diretor_id)
                if diretor_obj and diretor_obj.get('nome'):
                    nome_diretor_str = f"(Dir: {diretor_obj.get('nome')})"
            
            print(f"{prefixo}🎬 {filme.titulo} ({filme.ano}) {nome_diretor_str}")
        
        if mostrar_msg_voltar:
            input("\n🔁 Pressione Enter para voltar ao menu...")
        return True

    def alterar(self):
        print("\n--- Alteração de Filme ---")
        if not self.listar(com_indices=False):
            input("🔁 Pressione Enter para continuar...")
            return

        try:
            id_alvo = self.__tela_filmes.seleciona_filme_por_id(mensagem="Digite o ID do filme que deseja alterar: ")
            if id_alvo is None:
                print("ℹ️ Alteração cancelada.")
                input("🔁 Pressione Enter para continuar...")
                return
        except ValueError:
            print("❌ ID inválido. Deve ser um número.")
            input("🔁 Pressione Enter para continuar...")
            return

        filme_alvo = self.buscar_filme_por_id(id_alvo)

        if not filme_alvo:
            print(f"❌ Filme com ID {id_alvo} não encontrado.")
            input("🔁 Pressione Enter para continuar...")
            return

        nome_diretor_atual = "N/A"
        if hasattr(self.__controlador_sistema.controlador_membros, 'buscar_membro_por_id'):
            diretor_atual_obj = self.__controlador_sistema.controlador_membros.buscar_membro_por_id(filme_alvo.diretor_id)
            if diretor_atual_obj and diretor_atual_obj.get('nome'):
                nome_diretor_atual = diretor_atual_obj.get('nome')
        
        print(f"\nEditando filme: ID {filme_alvo.id_filme} - '{filme_alvo.titulo}' ({filme_alvo.ano}), Dir: {nome_diretor_atual}")
        
        lista_diretores = self.__controlador_sistema.controlador_membros.buscar_por_funcao("diretor")
        
        dados_atuais_filme = {
            "id_filme": filme_alvo.id_filme, 
            "titulo": filme_alvo.titulo, 
            "ano": filme_alvo.ano,
            "diretor_id": filme_alvo.diretor_id
        }
        novos_dados = self.__tela_filmes.le_dados_filme(dados_atuais=dados_atuais_filme, diretores_disponiveis=lista_diretores)

        if not novos_dados or not novos_dados.get("titulo") or novos_dados.get("ano") is None or novos_dados.get("diretor_id") is None:
            print("❌ Dados inválidos para alteração. Título, ano e diretor são obrigatórios.")
            input("🔁 Pressione Enter para continuar...")
            return

        if filme_alvo.titulo.casefold() != novos_dados["titulo"].casefold() and \
           self.existe_titulo_filme(novos_dados["titulo"], id_excluir=filme_alvo.id_filme):
            print(f"❌ Já existe outro filme com o título '{novos_dados['titulo']}'.")
            input("🔁 Pressione Enter para continuar...")
            return
            
        try:
            novo_ano = int(novos_dados["ano"])
            if novo_ano <= 0:
                raise ValueError("Ano deve ser um número positivo.")
        except ValueError as e:
            print(f"❌ Ano inválido: {e}. Deve ser um número inteiro positivo.")
            input("🔁 Pressione Enter para continuar...")
            return

        filme_alvo.titulo = novos_dados["titulo"]
        filme_alvo.ano = novo_ano
        filme_alvo.diretor_id = novos_dados["diretor_id"]
        novo_nome_diretor = "ID " + str(novos_dados["diretor_id"])
        if hasattr(self.__controlador_sistema.controlador_membros, 'buscar_membro_por_id'):
            diretor_obj = self.__controlador_sistema.controlador_membros.buscar_membro_por_id(novos_dados["diretor_id"])
            if diretor_obj and diretor_obj.get('nome'):
                novo_nome_diretor = diretor_obj.get('nome')

        print(f"✅ Filme ID {filme_alvo.id_filme} - '{filme_alvo.titulo}', Dir: {novo_nome_diretor} alterado com sucesso.")
        input("🔁 Pressione Enter para continuar...")

    def excluir(self):
        print("\n--- Exclusão de Filme ---")
        if not self.listar(com_indices=False):
            input("🔁 Pressione Enter para continuar...")
            return

        try:
            id_alvo = self.__tela_filmes.seleciona_filme_por_id(mensagem="Digite o ID do filme que deseja excluir: ")
            if id_alvo is None:
                print("ℹ️ Exclusão cancelada.")
                input("🔁 Pressione Enter para continuar...")
                return
        except ValueError:
            print("❌ ID inválido. Deve ser um número.")
            input("🔁 Pressione Enter para continuar...")
            return

        filme_alvo = self.buscar_filme_por_id(id_alvo)

        if not filme_alvo:
            print(f"❌ Filme com ID {id_alvo} não encontrado.")
            input("🔁 Pressione Enter para continuar...")
            return
        
        if self.__tela_filmes.confirma_exclusao(filme_alvo.titulo):
            self.__filmes.remove(filme_alvo)
            print(f"🗑️ Filme ID {filme_alvo.id_filme} - '{filme_alvo.titulo}' removido com sucesso.")
        else:
            print("ℹ️ Exclusão cancelada pelo usuário.")
        input("🔁 Pressione Enter para continuar...")