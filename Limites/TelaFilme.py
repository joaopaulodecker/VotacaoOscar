# Em Limites/TelaFilme.py
import PySimpleGUI as sg

class TelaFilmes:
    """Responsável pela interface gráfica do gerenciamento de Filmes."""
    def __init__(self):
        self.__window = None
        sg.theme('DarkAmber')

    def init_components_lista(self, dados_tabela: list):
        """Prepara a janela principal com a lista de filmes."""
        headings = ['ID', 'Título', 'Ano', 'Nacionalidade', 'Diretor']
        layout = [
            [sg.Text('Gerenciador de Filmes', font=('Helvetica', 25), justification='center', expand_x=True, pad=(0,10))],
            [sg.Table(values=dados_tabela, headings=headings, max_col_width=35,
                      auto_size_columns=True, justification='left', num_rows=10,
                      key='-TABELA-', row_height=25, enable_events=True)],
            [
                sg.Button('Adicionar', key='-ADICIONAR-'),
                sg.Button('Editar', key='-EDITAR-'),
                sg.Button('Excluir', key='-EXCLUIR-'),
                sg.Button('Agrupar por Nacionalidade', key='-AGRUPAR-'),
                sg.Push(),
                sg.Button('Voltar', key='-VOLTAR-')
            ]
        ]
        self.__window = sg.Window('Filmes', layout, finalize=True)

    def pega_dados_filme(self, diretores_para_combobox: list, dados_iniciais: dict):
        """Abre um formulário para Adicionar ou Editar um filme e retorna os dados brutos."""
        titulo_janela = dados_iniciais.get('titulo_janela', "Novo Filme")
        layout_form = [
            [sg.Text('Título:', size=(15,1)), sg.Input(default_text=dados_iniciais.get('titulo', ''), key='-TITULO-', expand_x=True)],
            [sg.Text('Ano:', size=(15,1)), sg.Input(default_text=dados_iniciais.get('ano', ''), key='-ANO-', expand_x=True)],
            [sg.Text('Nacionalidade:', size=(15,1)), sg.Input(default_text=dados_iniciais.get('nacionalidade_str', ''), key='-NACIONALIDADE-', expand_x=True)],
            [sg.Text('Diretor:', size=(15,1)), sg.Combo(diretores_para_combobox, default_value=dados_iniciais.get('diretor_str', ''), readonly=True, key='-DIRETOR-', expand_x=True)],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]
        form_window = sg.Window(titulo_janela, layout_form, finalize=True, modal=True)
        event, values = form_window.read()
        form_window.close()
        if event == 'Salvar':
            return values
        return None

    def mostra_filmes_agrupados(self, texto_formatado: str):
        """Exibe uma janela com o texto dos filmes agrupados."""
        sg.PopupScrolled(texto_formatado, title="Filmes Agrupados por Nacionalidade", size=(80, 20))

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