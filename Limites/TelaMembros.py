import PySimpleGUI as sg
from datetime import date

class TelaMembros:
    def __init__(self):
        self.__window = None


    def init_components_lista(self, dados_prontos_da_tabela: list):
        """A tela recebe os dados já formatados do controlador."""
        sg.theme('DarkAmber')

        headings = ['ID', 'Nome', 'Nascimento', 'Nacionalidade', 'Tipo', 'Gênero Art.']
        layout = [
            [sg.Text('Gerenciador de Pessoas', font=('Helvetica', 25))],
            [sg.Table(values=dados_prontos_da_tabela, headings=headings, max_col_width=25,
                      auto_size_columns=True, justification='left', num_rows=10,
                      key='-TABELA-', row_height=25, enable_events=True)],
            [
                sg.Button('Adicionar', key='-ADICIONAR-'),
                sg.Button('Editar', key='-EDITAR-'),
                sg.Button('Excluir', key='-EXCLUIR-'),
                sg.Button('Voltar', key='-VOLTAR-')
            ]
        ]

        self.__window = sg.Window('Membros da Academia', layout, finalize=True)

    def pega_dados_membro(self, dados_atuais: dict = None):
        is_edicao = bool(dados_atuais)
        titulo_janela = "Editar Pessoa" if is_edicao else "Adicionar Nova Pessoa"

        if is_edicao:
            nome_default = dados_atuais.get('nome', '')
            nasc_default = dados_atuais.get('data_nascimento', '')
            nac_default = dados_atuais.get('nacionalidade_str', '')
            genero_default = dados_atuais.get('genero_artistico', 'Ator')
            is_ator_atriz_edicao = dados_atuais.get('tipo_pessoa') == 'ator'
        else:
            nome_default, nasc_default, nac_default  = '', '', ''
            genero_default = 'Ator'
            is_ator_atriz_edicao = True

        # --- Layout do Formulário ---
        layout_form = [
            [sg.Text('Nome:', size=(15, 1)), sg.Input(default_text=nome_default, key='-NOME-')],
            [sg.Text('Ano Nascimento:', size=(15, 1)), sg.Input(default_text=nasc_default, key='-NASCIMENTO-')],
            [sg.Text('Nacionalidade:', size=(15, 1)), sg.Input(default_text=nac_default, key='-NACIONALIDADE-')],
            # Frame do Tipo de Pessoa (só aparece na adição)
            [sg.Frame('Tipo de Pessoa', [
                [sg.Radio('Ator/Atriz', 'RADIO_TIPO', default=not is_edicao, key='-TIPO_ATOR-', enable_events=True)],
                [sg.Radio('Diretor(a)', 'RADIO_TIPO', key='-TIPO_DIRETOR-', enable_events=True)],
                [sg.Radio('Membro Academia', 'RADIO_TIPO', key='-TIPO_MEMBRO-', enable_events=True)],
            ], visible=not is_edicao)],
            # Frame do Gênero Artístico (dinâmico)
            [sg.Frame('Gênero Artístico', [
                [sg.Radio('Ator', 'RADIO_GENERO', default=(genero_default == 'Ator'), key='-GENERO_ATOR-')],
                [sg.Radio('Atriz', 'RADIO_GENERO', default=(genero_default == 'Atriz'), key='-GENERO_ATRIZ-')],
            ], key='-FRAME_ATOR-', visible=is_ator_atriz_edicao)],
            # Botões de ação
            [sg.Submit('Salvar'), sg.Button('Limpar', key='-RESET-'), sg.Cancel('Cancelar')]
        ]
        form_window = sg.Window(titulo_janela, layout_form, finalize=True)

        # --- Loop de Eventos da Janela ---
        while True:
            event, values = form_window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                form_window.close()
                return None  # Sai sem salvar nada

            # Se o usuário clicar no rádio de Ator/Atriz, mostramos o quadro de gênero.
            if event == '-TIPO_ATOR-':
                form_window['-FRAME_ATOR-'].update(visible=True)
                # Se clicar em qualquer outro tipo, escondemos o quadro.
            elif event in ('-TIPO_DIRETOR-', '-TIPO_MEMBRO-'):
                form_window['-FRAME_ATOR-'].update(visible=False)

            #--- BOTÃO DE RESET ---
            if event == '-RESET-':
                form_window['-NOME-'].update('')
                form_window['-NASCIMENTO-'].update('')
                form_window['-NACIONALIDADE-'].update('')
                if not is_edicao:  # Só reseta os rádios se for adição
                    form_window['-TIPO_ATOR-'].update(True)
                    form_window['-FRAME_ATOR-'].update(visible=True)
                form_window['-GENERO_ATOR-'].update(True)

            if event == 'Salvar':
                # --- Bloco de Validação ---
                erros = []
                nome = values['-NOME-'].strip()
                if not nome:
                    erros.append("O campo 'Nome' é obrigatório.")

                nacionalidade = values['-NACIONALIDADE-'].strip()
                if not nacionalidade:
                    erros.append("O campo 'Nacionalidade' é obrigatório.")

                try:
                    ano_nasc = int(values['-NASCIMENTO-'])
                    ano_atual = date.today().year
                    if not (1900 <= ano_nasc <= ano_atual):
                        erros.append(f"O ano de nascimento deve ser um número entre 1900 e {ano_atual}.")
                except (ValueError, TypeError):
                    erros.append("Ano de nascimento deve ser um número válido.")

                # Se encontramos algum erro, mostramos todos de uma vez e voltamos ao form.
                if erros:
                    self.show_message("Erros de Validação", "\n".join(erros))
                    continue  # Continua no loop, não fecha a janela

                # Se tudo estiver OK, fechamos a janela e retornamos os dados!
                form_window.close()
                return values

    def open_lista(self):
        event, values = self.__window.read()
        return event, values

    def close_lista(self):
        if self.__window:
            self.__window.close()
        self.__window = None

    @staticmethod
    def show_message(titulo: str, mensagem: str):
        sg.Popup(titulo, mensagem)

    @staticmethod
    def show_confirm_message(titulo: str, mensagem: str):
        return sg.popup_yes_no(mensagem, title=titulo)

    def refresh_table(self, dados_prontos_da_tabela: list):
        self.__window['-TABELA-'].update(values=dados_prontos_da_tabela)