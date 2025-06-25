from Entidades.Categoria import Categoria
from Limites.TelaCategoria import TelaCategoria
from DAOs.CategoriaDao import CategoriaDAO

class ControladorCategorias:
    # --- CORREÇÃO APLICADA AQUI ---
    # Removido o parâmetro 'controlador_sistema' que não era utilizado
    def __init__(self):
        self.__dao = CategoriaDAO()
        self.__tela_categoria = TelaCategoria()
    # -----------------------------

    @property
    def entidades(self):
        return self.__dao.get_all()

    def _gerar_proximo_id(self):
        todas_entidades = self.__dao.get_all()
        if not todas_entidades:
            return 1
        return max(cat.id for cat in todas_entidades) + 1

    def buscar_categoria_por_id(self, id_categoria: int):
        return self.__dao.get(id_categoria)

    def _existe_nome_categoria(self, nome: str, id_excluir: int = None):
        for categoria in self.__dao.get_all():
            if id_excluir is not None and categoria.id == id_excluir:
                continue
            if categoria.nome.casefold() == nome.casefold():
                return True
        return False
    
    def abrir_menu(self):
        self.__tela_categoria.init_components_lista(self.entidades)
        while True:
            event, values = self.__tela_categoria.open_lista()

            if event in (None, '-VOLTAR-'):
                break

            if event == '-ADICIONAR-':
                self.cadastrar()
            
            # Garante que uma linha da tabela foi selecionada para Editar/Excluir
            elif values['-TABELA-']:
                # Pega o índice da linha selecionada
                index_selecionado = values['-TABELA-'][0]
                # Pega o objeto Categoria correspondente a esse índice
                categoria_selecionada = self.entidades[index_selecionado]

                if event == '-EDITAR-':
                    self.alterar(categoria_selecionada)
                elif event == '-EXCLUIR-':
                    self.excluir(categoria_selecionada)
            elif event in ('-EDITAR-', '-EXCLUIR-'):
                self.__tela_categoria.show_message("Aviso", "Por favor, selecione uma categoria na tabela primeiro.")

        self.__tela_categoria.close_lista()

    def cadastrar(self):
        dados_categoria = self.__tela_categoria.pega_dados_categoria()

        if dados_categoria:
            if self._existe_nome_categoria(dados_categoria["-NOME-"]):
                self.__tela_categoria.show_message("Erro", f"❌ Categoria '{dados_categoria['-NOME-']}' já existe.")
                return

            novo_id = self._gerar_proximo_id()
            nova_categoria = Categoria(novo_id, dados_categoria["-NOME-"], dados_categoria["-TIPO-"])
            self.__dao.add(novo_id, nova_categoria)
            self.__tela_categoria.show_message("Sucesso", f"✅ Categoria '{nova_categoria.nome}' cadastrada.")
            self.__tela_categoria.refresh_table(self.entidades)

    def alterar(self, categoria_alvo: Categoria):
        dados_atuais = {'nome': categoria_alvo.nome, 'tipo_indicacao': categoria_alvo.tipo_indicacao}
        novos_dados = self.__tela_categoria.pega_dados_categoria(dados_atuais=dados_atuais)

        if novos_dados:
            novo_nome = novos_dados["-NOME-"]
            if (categoria_alvo.nome.casefold() != novo_nome.casefold() and
                    self._existe_nome_categoria(novo_nome, id_excluir=categoria_alvo.id)):
                self.__tela_categoria.show_message("Erro", f"❌ Já existe outra categoria com o nome '{novo_nome}'.")
                return

            categoria_alvo.nome = novo_nome
            self.__dao.add(categoria_alvo.id, categoria_alvo)
            self.__tela_categoria.show_message("Sucesso", "✅ Alteração realizada com sucesso!")
            self.__tela_categoria.refresh_table(self.entidades)

    def excluir(self, categoria_alvo: Categoria):
        confirmado = self.__tela_categoria.show_confirm_message(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a categoria '{categoria_alvo.nome}'?"
        )
        if confirmado == 'Yes':
            self.__dao.remove(categoria_alvo.id)
            self.__tela_categoria.show_message("Sucesso", "🗑️ Categoria removida com sucesso.")
            self.__tela_categoria.refresh_table(self.entidades)