from Entidades.Categoria import Categoria
from Limites.TelaCategoria import TelaCategoria
from Excecoes.OpcaoInvalida import OpcaoInvalida
from Excecoes.EntidadeDuplicadaException import EntidadeDuplicadaException
from DAOs.categoria_dao import CategoriaDAO


class ControladorCategorias:
    def __init__(self):
        self.__dao = CategoriaDAO()
        self.__tela_categoria = TelaCategoria()

    @property
    def entidades(self):
        """Retorna todas as categorias do DAO."""
        return self.__dao.get_all()

    def _gerar_proximo_id(self):
        """Gera um ID único com base nos IDs existentes."""
        todas_categorias = self.entidades
        if not todas_categorias:
            return 1
        ultimo_id = max(categoria.id for categoria in todas_categorias)
        return ultimo_id + 1

    def buscar_categoria_por_id(self, id_categoria: int):
        """Busca uma categoria pelo seu ID usando o DAO."""
        return self.__dao.get(id_categoria)

    def _existe_nome_categoria(self, nome: str, id_excluir: int = None):
        """Verifica se um nome de categoria já existe."""
        for categoria in self.entidades:
            if id_excluir is not None and categoria.id == id_excluir:
                continue
            if categoria.nome.casefold() == nome.casefold():
                return True
        return False

    def abrir_menu(self):
        """Exibe o menu de categorias e processa a escolha do usuário."""
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
        """Processa o cadastro de uma nova categoria."""
        dados_tela = self.__tela_categoria.pega_dados_categoria()
        if dados_tela is None:
            self.__tela_categoria.mostra_mensagem("ℹ️ Cadastro cancelado.")
            self.__tela_categoria.espera_input()
            return

        nome_categoria = dados_tela["nome"]
        if self._existe_nome_categoria(nome_categoria):
            raise EntidadeDuplicadaException(
                f"❌ Categoria '{nome_categoria}' já existe."
            )

        novo_id = self._gerar_proximo_id()
        nova_categoria = Categoria(
            id_categoria=novo_id,
            nome=nome_categoria,
            tipo_indicacao=dados_tela["tipo_indicacao"]
        )
        self.__dao.add(nova_categoria)
        self.__tela_categoria.mostra_mensagem(
            f"✅ Categoria ID {nova_categoria.id} - '{nova_categoria.nome}' "
            "cadastrada com sucesso!"
        )
        self.__tela_categoria.espera_input()

    def listar(self, mostrar_msg_voltar=False):
        """Prepara os dados das categorias e os envia para a tela."""
        categorias_existentes = self.entidades
        dados_para_tela = [
            {"id": cat.id, "nome": cat.nome, "tipo_indicacao": cat.tipo_indicacao}
            for cat in categorias_existentes
        ]
        self.__tela_categoria.mostra_lista_categorias(dados_para_tela)

        if mostrar_msg_voltar:
            self.__tela_categoria.espera_input()
        
        return bool(categorias_existentes)

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
            self.__tela_categoria.mostra_mensagem(
                f"❌ Categoria com ID {id_alvo} não encontrada."
            )
        else:
            dados_atuais = {
                "id": categoria_alvo.id,
                "nome": categoria_alvo.nome,
                "tipo_indicacao": categoria_alvo.tipo_indicacao
            }
            novos_dados = self.__tela_categoria.pega_dados_categoria(
                dados_atuais=dados_atuais
            )

            if not novos_dados or not novos_dados.get("nome"):
                self.__tela_categoria.mostra_mensagem("ℹ️ Nenhuma alteração realizada.")
            else:
                novo_nome = novos_dados["nome"]
                if (categoria_alvo.nome.casefold() != novo_nome.casefold() and
                        self._existe_nome_categoria(novo_nome, id_excluir=categoria_alvo.id)):
                    self.__tela_categoria.mostra_mensagem(
                        f"❌ Já existe outra categoria com o nome '{novo_nome}'."
                    )
                else:
                    categoria_alvo.nome = novo_nome
                    self.__dao.update()
                    self.__tela_categoria.mostra_mensagem(
                        "✅ Alteração realizada com sucesso!"
                    )
        
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
            self.__tela_categoria.mostra_mensagem(
                f"❌ Categoria com ID {id_alvo} não encontrada."
            )
        elif self.__tela_categoria.confirma_exclusao(categoria_alvo.nome):
            self.__dao.remove(id_alvo) 
            self.__tela_categoria.mostra_mensagem("🗑️ Categoria removida com sucesso.")
        else:
            self.__tela_categoria.mostra_mensagem("ℹ️ Exclusão cancelada pelo usuário.")
        
        self.__tela_categoria.espera_input()
