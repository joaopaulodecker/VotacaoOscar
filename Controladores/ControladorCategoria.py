from Entidades.Categoria import Categoria
from Limites.TelaCategoria import TelaCategoria
from Excecoes.OpcaoInvalida import OpcaoInvalida
from Excecoes.EntidadeDuplicadaException import EntidadeDuplicadaException

class ControladorCategorias:
    def __init__(self):
        self.__entidades = []
        self.__tela_categoria = TelaCategoria()
        self.__proximo_id = 1

    @property
    def entidades(self):
        return self.__entidades

    def _gerar_proximo_id(self):
        id_atual = self.__proximo_id
        self.__proximo_id += 1
        return id_atual

    def buscar_categoria_por_id(self, id_categoria: int):
        for categoria in self.__entidades:
            if isinstance(categoria, Categoria) and categoria.id == id_categoria:
                return categoria
        return None

    def _existe_nome_categoria(self, nome: str, id_excluir: int = None):
        for categoria in self.__entidades:
            if id_excluir is not None and categoria.id == id_excluir:
                continue
            if categoria.nome.casefold() == nome.casefold():
                return True
        return False
        
    def abrir_menu(self):
        while True:
            try:
                opcao = self.__tela_categoria.mostra_opcoes()
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
            except EntidadeDuplicadaException as e:
                self.__tela_categoria.mostra_mensagem(str(e))
                self.__tela_categoria.espera_input()
            except OpcaoInvalida as e:
                self.__tela_categoria.mostra_mensagem(f"❌ {e}")
                self.__tela_categoria.espera_input()

    def cadastrar(self):

        # 1. Pede os dados para a Tela. A Tela é responsável pelos inputs.
        dados_categoria = self.__tela_categoria.pega_dados_categoria()
        if dados_categoria is None:
            self.__tela_categoria.mostra_mensagem("ℹ️ Cadastro cancelado.")
            self.__tela_categoria.espera_input()
            return

        # 2. O Controlador valida os dados e lança uma exceção se a regra for violada.
        if self._existe_nome_categoria(dados_categoria["nome"]):
            raise EntidadeDuplicadaException(f"❌ Categoria '{dados_categoria['nome']}' já existe.")

        # 3. O Controlador cria a entidade e manda a Tela mostrar o sucesso.
        novo_id = self._gerar_proximo_id()
        nova_categoria = Categoria(novo_id, dados_categoria["nome"], dados_categoria["tipo_indicacao"])
        self.__entidades.append(nova_categoria)
        self.__tela_categoria.mostra_mensagem(f"✅ Categoria '{nova_categoria.nome}' cadastrada com sucesso!")
        self.__tela_categoria.espera_input()

    def listar(self, mostrar_msg_voltar=False):
        """Prepara os dados das categorias e os envia para a tela para listagem."""

        # 1. O Controlador prepara os dados para a Tela (lista de dicionários)
        dados_para_tela = [
            {"id": cat.id, "nome": cat.nome, "tipo": cat.tipo_indicacao}
            for cat in self.__entidades
        ]

        # 2. O Controlador envia os dados para a Tela exibir.
        self.__tela_categoria.mostra_lista_categorias(dados_para_tela)

        # 3. A pausa (se solicitada) acontece no final, independentemente de a lista estar vazia ou não.
        if mostrar_msg_voltar:
            self.__tela_categoria.espera_input()

        return bool(self.__entidades)

    def alterar(self):
        """Permite alterar o nome de uma categoria existente."""
        if not self.listar():
            return

        id_alvo = self.__tela_categoria.seleciona_categoria_por_id()
        if id_alvo is None:
            self.__tela_categoria.mostra_mensagem("ℹ️ Alteração cancelada.")
            self.__tela_categoria.espera_input()
            return

        categoria_alvo = self.buscar_categoria_por_id(id_alvo)
        if not categoria_alvo:
            self.__tela_categoria.mostra_mensagem(f"❌ Categoria com ID {id_alvo} não encontrada.")
        else:
            dados_atuais_para_tela = {"id": categoria_alvo.id, "nome": categoria_alvo.nome}
            novos_dados = self.__tela_categoria.pega_dados_categoria(dados_atuais=dados_atuais_para_tela)

            if not novos_dados or not novos_dados.get("nome"):
                self.__tela_categoria.mostra_mensagem("ℹ️ Nenhuma alteração realizada.")
            else:
                novo_nome = novos_dados["nome"].title()
                if (categoria_alvo.nome.casefold() != novo_nome.casefold() and
                        self._existe_nome_categoria(novo_nome, id_excluir=categoria_alvo.id)):
                    self.__tela_categoria.mostra_mensagem(f"❌ Já existe outra categoria com o nome '{novo_nome}'.")
                else:
                    categoria_alvo.nome = novo_nome
                    self.__tela_categoria.mostra_mensagem("✅ Alteração realizada com sucesso!")
        
        self.__tela_categoria.espera_input()

    def excluir(self):
        """Permite excluir uma categoria existente."""
        if not self.listar():
            return

        id_alvo = self.__tela_categoria.seleciona_categoria_por_id()
        if id_alvo is None:
            self.__tela_categoria.mostra_mensagem("ℹ️ Exclusão cancelada.")
            self.__tela_categoria.espera_input()
            return

        categoria_alvo = self.buscar_categoria_por_id(id_alvo)
        if not categoria_alvo:
            self.__tela_categoria.mostra_mensagem(f"❌ Categoria com ID {id_alvo} não encontrada.")
        elif self.__tela_categoria.confirma_exclusao(categoria_alvo.nome):
            self.__entidades.remove(categoria_alvo)
            self.__tela_categoria.mostra_mensagem("🗑️ Categoria removida com sucesso.")
        else:
            self.__tela_categoria.mostra_mensagem("ℹ️ Exclusão cancelada pelo usuário.")
        
        self.__tela_categoria.espera_input()