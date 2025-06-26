import PySimpleGUI as sg


class TelaIndicacao:
    def __init__(self):
        self.__window = None


    @staticmethod
    def _preparar_dados_tabela(indicacoes_lista: list):
        """Formata a lista de objetos de Indicação para a tabela da tela."""
        dados_tabela = []
        for indicacao in indicacoes_lista:
            dados_tabela.append([
                indicacao.id_indicacao,
                indicacao.categoria.nome,
                indicacao.obter_detalhes_item_indicado()
            ])
        return dados_tabela

    def init_components(self, indicacoes_lista: list):
        """Cria a janela principal que lista todas as indicações."""
        sg.theme('DarkAmber')

        headings = ['ID', 'Categoria', 'Indicado']

        dados_tabela = TelaIndicacao._preparar_dados_tabela(indicacoes_lista)

        layout = [
            [sg.Text('Gerenciador de Indicações', font=('Helvetica', 25))],
            [sg.Table(values=dados_tabela, headings=headings, max_col_width=35,
                      auto_size_columns=True, justification='left', num_rows=10,
                      key='-TABELA-', row_height=25, enable_events=True)],
            [
                sg.Button('Adicionar Indicação', key='-ADICIONAR-'),
                sg.Button('Excluir Indicação', key='-EXCLUIR-'),
                sg.Button('Voltar', key='-VOLTAR-')
            ]
        ]
        self.__window = sg.Window('Indicações ao Oscar', layout, finalize=True)

    def pega_dados_indicacao(self, categorias_lista: list) -> dict | None:
        """
           Abre um formulário para o usuário selecionar a categoria.
           Retorna um dicionário com a ação 'BUSCAR_FINALISTAS' e o objeto da categoria.
           """
        if not categorias_lista:
            self.show_message("Aviso", "Nenhuma categoria cadastrada para criar uma indicação.")
            return None

        # Formata os dados para a lista de seleção
        mapa_categorias = {cat.nome: cat for cat in categorias_lista}

        layout_form = [
            [sg.Text('Passo 1: Selecione a Categoria', font=('Helvetica', 15))],
            [sg.Listbox(values=list(mapa_categorias.keys()), size=(50, 8), key='-CATEGORIA-')],
            [sg.Submit('Próximo'), sg.Cancel('Cancelar')]
        ]

        form_window = sg.Window("Registrar Nova Indicação - Passo 1", layout_form, finalize=True)

        event, values = form_window.read()

        if event in (sg.WIN_CLOSED, 'Cancelar'):
            form_window.close()
            return None

        if event == 'Próximo':
            # Validação: Garante que o usuário selecionou uma categoria
            if not values['-CATEGORIA-']:
                self.show_message("Erro", "Você precisa selecionar uma categoria para continuar.")
                # Fechamos e retornamos None para o controlador saber que falhou.
                form_window.close()
                return None

            # Pega o nome e o objeto da categoria selecionada
            nome_cat_selecionada = values['-CATEGORIA-'][0]
            cat_obj_selecionada = mapa_categorias[nome_cat_selecionada]

            form_window.close()

            return {"acao": "BUSCAR_FINALISTAS", "categoria_obj": cat_obj_selecionada}

        form_window.close()
        return None
    def preenche_lista_finalistas(self, finalistas: list, categoria_obj):
        """
        Abre uma segunda janela (ou atualiza a existente) para mostrar os finalistas.
        Este é um metodo chamado pelo controlador DEPOIS de buscar os finalistas.
        """
        mapa_finalistas = {f.get('nome_display'): f for f in finalistas}

        layout_finalistas = [
            [sg.Text(f'Categoria: {categoria_obj.nome}', font=('Helvetica', 12), justification='center')],
            [sg.Text('Passo 2: Selecione o Indicado', font=('Helvetica', 15))],
            [sg.Listbox(values=list(mapa_finalistas.keys()), size=(40, 10), key='-INDICADO-')],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]

        form_window = sg.Window("Registrar Nova Indicação - Passo 2", layout_finalistas, finalize=True)

        event, values = form_window.read()

        if event in (sg.WIN_CLOSED, 'Cancelar'):
            form_window.close()
            return None

        if event == 'Salvar':
            if not values['-INDICADO-']:
                self.show_message("Erro", "Você precisa selecionar um indicado.")
                return self.preenche_lista_finalistas(finalistas, categoria_obj)

            nome_indicado = values['-INDICADO-'][0]
            indicado_obj_completo = mapa_finalistas[nome_indicado]

            form_window.close()
            return {"acao": "SALVAR_INDICACAO", "categoria_obj": categoria_obj, "indicado_obj": indicado_obj_completo}

        return None

    @staticmethod
    def show_message(titulo: str, mensagem: str):
        sg.Popup(titulo, mensagem)

    @staticmethod
    def show_confirm_message(titulo: str, mensagem: str):
        return sg.popup_yes_no(mensagem, title=titulo)

    def open(self):
        if self.__window:
            event, values = self.__window.read()
            return event, values
        return None, None

    def close(self):
        if self.__window:
            self.__window.close()
        self.__window = None

    def refresh_table(self, indicacoes_lista: list):
        if self.__window:
            dados_tabela = TelaIndicacao._preparar_dados_tabela(indicacoes_lista)
            self.__window['-TABELA-'].update(values=dados_tabela)