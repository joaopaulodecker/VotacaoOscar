import PySimpleGUI as sg

class TelaCategoria:
    """Responsável pela interface gráfica do gerenciamento de Categorias."""
    def __init__(self):
        self.__window = None
        sg.theme('DarkAmber')

    def init_components_lista(self, dados_tabela: list):
        """Prepara a janela principal com a lista de categorias."""
        headings = ['ID', 'Nome', 'Tipo de Indicação']
        layout = [
            [sg.Text('Gerenciador de Categorias', font=('Helvetica', 25), justification='center', expand_x=True, pad=(0,10))],
            [sg.Table(values=dados_tabela, headings=headings, max_col_width=35,
                      auto_size_columns=True, justification='left', num_rows=10,
                      key='-TABELA-', row_height=25, enable_events=True)],
            [
                sg.Button('Adicionar', key='-ADICIONAR-'),
                sg.Button('Editar', key='-EDITAR-'),
                sg.Button('Excluir', key='-EXCLUIR-'),
                sg.Push(),
                sg.Button('Voltar', key='-VOLTAR-')
            ]
        ]
        self.__window = sg.Window('Categorias', layout, finalize=True)

    def pega_dados_categoria(self, dados_iniciais: dict):
        """Abre um formulário para Adicionar ou Editar uma categoria e retorna os dados brutos."""
        titulo_janela = dados_iniciais.get('titulo_janela', "Nova Categoria")
        is_edicao = dados_iniciais.get('is_edicao', False)

        tipos_disponiveis = ['filme', 'ator', 'diretor']

        layout_form = [
            [sg.Text('Nome da Categoria:', size=(15,1)), sg.Input(default_text=dados_iniciais.get('nome', ''), key='-NOME-', expand_x=True)],
            [sg.Text('Tipo de Indicação:', size=(15,1)), sg.Combo(tipos_disponiveis, default_value=dados_iniciais.get('tipo_indicacao', 'filme'), readonly=True, key='-TIPO-', disabled=is_edicao, expand_x=True)],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]

        form_window = sg.Window(titulo_janela, layout_form, finalize=True, modal=True)
        event, values = form_window.read()
        form_window.close()

        if event == 'Salvar':
            return values
        return None

    def open_lista(self):
        """Lê um evento da janela principal de listagem."""
        event, values = self.__window.read()
        return event, values

    def close_lista(self):
        """Fecha a janela principal de listagem."""
        if self.__window:
            self.__window.close()
        self.__window = None

    def refresh_table(self, dados_tabela: list):
        """Atualiza os dados da tabela na janela principal."""
        self.__window['-TABELA-'].update(values=dados_tabela)

    @staticmethod
    def show_message(titulo: str, mensagem: str):
        """Exibe uma mensagem de pop-up simples."""
        sg.Popup(titulo, mensagem)

    @staticmethod
    def show_confirm_message(titulo: str, mensagem: str):
        """Exibe um pop-up de confirmação (Sim/Não) e retorna a escolha."""
        return sg.popup_yes_no(mensagem, title=titulo)