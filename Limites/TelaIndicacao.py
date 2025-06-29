import PySimpleGUI as sg

class TelaIndicacao:
    """Responsável pela interface gráfica do gerenciamento de Indicações."""
    def __init__(self):
        self.__window = None
        sg.theme('DarkAmber')

    def init_components(self, dados_tabela: list):
        """Prepara a janela principal com a lista de indicações."""
        headings = ['ID', 'Indicado por', 'Categoria', 'Item Indicado']
        layout = [
            [sg.Text('Gerenciador de Indicações', font=('Helvetica', 25), justification='center', expand_x=True, pad=(0,10))],
            [sg.Table(values=dados_tabela, headings=headings, max_col_width=30,
                      auto_size_columns=True, justification='left', num_rows=10,
                      key='-TABELA-', row_height=25, enable_events=True)],
            [
                sg.Button('Adicionar Indicação', key='-ADICIONAR-'),
                sg.Button('Excluir Indicação', key='-EXCLUIR-'),
                sg.Push(),
                sg.Button('Voltar', key='-VOLTAR-')
            ]
        ]
        self.__window = sg.Window('Indicações ao Oscar', layout, finalize=True)

    def pega_dados_indicacao_passo1(self, categorias_map: dict, membros_map: dict):
        """Abre o formulário do Passo 1: selecionar Indicante e Categoria."""
        layout_form = [
            [sg.Text('Passo 1: Selecione o Indicante e a Categoria', font=('Helvetica', 15))],
            [sg.Text('Membro Indicante:')],
            [sg.Listbox(values=list(membros_map.keys()), size=(60, 5), key='-MEMBRO-', expand_x=True)],
            [sg.Text('Categoria:')],
            [sg.Listbox(values=list(categorias_map.keys()), size=(60, 5), key='-CATEGORIA-', expand_x=True)],
            [sg.Submit('Próximo'), sg.Cancel('Cancelar')]
        ]
        form_window = sg.Window("Registrar Nova Indicação - Passo 1", layout_form, modal=True)
        event, values = form_window.read()
        form_window.close()
        if event == 'Próximo':
            return values
        return None

    def pega_dados_indicacao_passo2(self, indicaveis_map: dict, nome_categoria: str):
        """Abre o formulário do Passo 2: selecionar o item a ser indicado."""
        layout_finalistas = [
            [sg.Text(f'Categoria: {nome_categoria}', font=('Helvetica', 12), justification='center', expand_x=True)],
            [sg.Text('Passo 2: Selecione o Indicado', font=('Helvetica', 15))],
            [sg.Listbox(values=list(indicaveis_map.keys()), size=(50, 10), key='-INDICADO-', expand_x=True)],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]
        form_window = sg.Window("Registrar Nova Indicação - Passo 2", layout_finalistas, modal=True)
        event, values = form_window.read()
        form_window.close()
        if event == 'Salvar':
            return values
        return None

    def open(self):
        """Lê um evento da janela principal de listagem."""
        event, values = self.__window.read()
        return event, values

    def close(self):
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