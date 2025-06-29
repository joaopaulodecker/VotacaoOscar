import PySimpleGUI as sg


class TelaMembros:
    """Responsável pela interface gráfica do gerenciamento de Membros."""

    def __init__(self):
        self.__window = None
        sg.theme('DarkAmber')

    def init_components_lista(self, dados_tabela: list):
        """Prepara a janela principal com a lista de membros."""
        headings = ['ID', 'Nome', 'Nascimento', 'Nacionalidade', 'Tipo', 'Gênero Art.']
        layout = [
            [sg.Text('Gerenciador de Pessoas', font=('Helvetica', 25), justification='center', expand_x=True,
                     pad=(0, 10))],
            [sg.Table(values=dados_tabela, headings=headings, max_col_width=25,
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
        self.__window = sg.Window('Membros da Academia', layout, finalize=True)

    def pega_dados_membro(self, dados_iniciais: dict):
        """Abre um formulário para Adicionar ou Editar um membro e retorna os dados brutos."""
        titulo_janela = dados_iniciais.get('titulo_janela', "Nova Pessoa")
        is_edicao = dados_iniciais.get('is_edicao', False)

        # Frame do Tipo de Pessoa (só pode ser alterado na adição)
        frame_tipo_pessoa = [
            [sg.Radio('Ator/Atriz', 'RADIO_TIPO', default=True, key='-TIPO_ATOR-', enable_events=True)],
            [sg.Radio('Diretor(a)', 'RADIO_TIPO', key='-TIPO_DIRETOR-', enable_events=True)],
            [sg.Radio('Membro Academia', 'RADIO_TIPO', key='-TIPO_MEMBRO-', enable_events=True)],
        ]

        # Frame do Gênero Artístico (só visível para Ator/Atriz)
        frame_genero_ator = [
            [sg.Radio('Ator', 'RADIO_GENERO', default=(dados_iniciais.get('genero_artistico') != 'Atriz'),
                      key='-GENERO_ATOR-')],
            [sg.Radio('Atriz', 'RADIO_GENERO', default=(dados_iniciais.get('genero_artistico') == 'Atriz'),
                      key='-GENERO_ATRIZ-')],
        ]

        layout_form = [
            [sg.Text('Nome:', size=(15, 1)),
             sg.Input(default_text=dados_iniciais.get('nome', ''), key='-NOME-', expand_x=True)],
            [sg.Text('Ano Nascimento:', size=(15, 1)),
             sg.Input(default_text=dados_iniciais.get('data_nascimento', ''), key='-NASCIMENTO-', expand_x=True)],
            [sg.Text('Nacionalidade:', size=(15, 1)),
             sg.Input(default_text=dados_iniciais.get('nacionalidade_str', ''), key='-NACIONALIDADE-', expand_x=True)],
            # A visibilidade do frame de tipo é controlada pelo modo de edição
            [sg.Frame('Tipo de Pessoa', frame_tipo_pessoa, key='-FRAME_TIPO-', visible=not is_edicao)],
            # A visibilidade do frame de gênero é controlada pelo tipo de pessoa
            [sg.Frame('Gênero Artístico', frame_genero_ator, key='-FRAME_ATOR-',
                      visible=dados_iniciais.get('is_ator', True))],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]
        form_window = sg.Window(titulo_janela, layout_form, finalize=True, modal=True)

        # Loop de eventos interno apenas para a lógica da UI (mostrar/esconder frame)
        while True:
            event, values = form_window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                form_window.close()
                return None

            if event == '-TIPO_ATOR-':
                form_window['-FRAME_ATOR-'].update(visible=True)
            elif event in ('-TIPO_DIRETOR-', '-TIPO_MEMBRO-'):
                form_window['-FRAME_ATOR-'].update(visible=False)

            if event == 'Salvar':
                form_window.close()
                return values

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