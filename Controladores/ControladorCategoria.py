from Entidades.Categoria import Categoria
from Limites.TelaCategoria import TelaCategoria
from DAOs.CategoriaDao import CategoriaDAO


class ControladorCategorias:
    """Controlador principal para as regras de negócio de Categorias."""

    def __init__(self):
        self.__dao = CategoriaDAO()
        self.__tela_categoria = TelaCategoria()

    def get_categorias(self):
        """Metodo público para fornecer a lista de todas as categorias."""
        return self.__dao.get_all()

    def _preparar_dados_tabela(self):
        """Busca as categorias e as formata para a tabela da interface."""
        categorias = self.__dao.get_all()
        dados_tabela = []
        for categoria in categorias:
            dados_tabela.append([categoria.id, categoria.nome, categoria.tipo_indicacao.capitalize()])
        return dados_tabela

    def buscar_categoria_por_id(self, id_categoria: int):
        """Busca uma categoria pelo seu ID no DAO."""
        return self.__dao.get(id_categoria)

    def _existe_nome_categoria(self, nome: str, id_excluir: int = None):
        """Verifica se um nome de categoria já existe."""
        for categoria in self.__dao.get_all():
            if id_excluir is not None and categoria.id == id_excluir:
                continue
            if categoria.nome.casefold() == nome.casefold():
                return True
        return False

    def abre_tela(self):
        """Abre a tela principal e gerencia o loop de eventos."""
        dados_tabela = self._preparar_dados_tabela()
        self.__tela_categoria.init_components_lista(dados_tabela)

        while True:
            event, values = self.__tela_categoria.open_lista()
            if event in (None, '-VOLTAR-'):
                self.__tela_categoria.close_lista()
                break

            # --- LÓGICA DE EVENTOS ---
            if event == '-ADICIONAR-':
                self.cadastrar()

            elif event in ('-EDITAR-', '-EXCLUIR-'):
                if values.get('-TABELA-'):
                    index_selecionado = values['-TABELA-'][0]
                    id_categoria_selecionada = dados_tabela[index_selecionado][0]
                    categoria_alvo = self.buscar_categoria_por_id(id_categoria_selecionada)

                    if categoria_alvo and event == '-EDITAR-':
                        self.alterar(categoria_alvo)
                    elif categoria_alvo and event == '-EXCLUIR-':
                        self.excluir(categoria_alvo)
                else:
                    self.__tela_categoria.show_message("Aviso",
                                                       "Por favor, selecione uma categoria na tabela primeiro.")

            if event in ('-ADICIONAR-', '-EDITAR-', '-EXCLUIR-'):
                dados_tabela = self._preparar_dados_tabela()
                self.__tela_categoria.refresh_table(dados_tabela)
    def cadastrar(self):
        """Orquestra o processo de cadastro de uma nova categoria."""
        dados_brutos = self.__tela_categoria.pega_dados_categoria({
            'titulo_janela': "Adicionar Categoria"
        })

        if dados_brutos:
            # Controlador faz a validação dos dados brutos recebidos da Tela
            nome_categoria = dados_brutos["-NOME-"].strip().title()
            if not nome_categoria:
                self.__tela_categoria.show_message("Erro de Validação", "O nome da categoria não pode ser vazio.")
                return

            if self._existe_nome_categoria(nome_categoria):
                self.__tela_categoria.show_message("Erro", f"A categoria '{nome_categoria}' já existe.")
                return

            # Controlador cria o objeto e o salva
            novo_id = self.__dao.get_next_id()
            nova_categoria = Categoria(novo_id, nome_categoria, dados_brutos["-TIPO-"])
            self.__dao.add(key=novo_id, categoria=nova_categoria)
            self.__tela_categoria.show_message("Sucesso", f"Categoria '{nova_categoria.nome}' cadastrada.")

    def alterar(self, categoria_alvo: Categoria):
        """Orquestra a alteração de uma categoria existente."""
        dados_iniciais = {
            'titulo_janela': "Editar Categoria",
            'is_edicao': True,
            'nome': categoria_alvo.nome,
            'tipo_indicacao': categoria_alvo.tipo_indicacao
        }
        dados_brutos = self.__tela_categoria.pega_dados_categoria(dados_iniciais)

        if dados_brutos:
            novo_nome = dados_brutos["-NOME-"].strip().title()
            if not novo_nome:
                self.__tela_categoria.show_message("Erro de Validação", "O nome da categoria não pode ser vazio.")
                return

            if (categoria_alvo.nome.casefold() != novo_nome.casefold() and
                    self._existe_nome_categoria(novo_nome, id_excluir=categoria_alvo.id)):
                self.__tela_categoria.show_message("Erro", f"Já existe outra categoria com o nome '{novo_nome}'.")
                return

            categoria_alvo.nome = novo_nome
            self.__dao.add(key=categoria_alvo.id, categoria=categoria_alvo)
            self.__tela_categoria.show_message("Sucesso", "Alteração realizada com sucesso!")

    def excluir(self, categoria_alvo: Categoria):
        """Orquestra a exclusão de uma categoria."""
        confirmado = self.__tela_categoria.show_confirm_message(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a categoria '{categoria_alvo.nome}'?"
        )
        if confirmado == 'Yes':
            self.__dao.remove(categoria_alvo.id)
            self.__tela_categoria.show_message("Sucesso", "Categoria removida com sucesso.")