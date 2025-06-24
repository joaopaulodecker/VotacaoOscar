import PySimpleGUI as sg

class TelaCategoria:
    def __init__(self):
        self.__window = None

    def init_components_lista(self, categorias_lista):
        sg.theme('Reddit')
        
        headings = ['ID', 'Nome', 'Tipo de Indicação']
        
        dados_tabela = []
        for categoria in categorias_lista:
            dados_tabela.append([categoria.id, categoria.nome, categoria.tipo_indicacao.capitalize()])

        layout = [
            [sg.Text('Gerenciador de Categorias', font=('Helvetica', 25))],
            [sg.Table(values=dados_tabela, headings=headings, max_col_width=35,
                      auto_size_columns=True, justification='left', num_rows=10,
                      key='-TABELA-', row_height=25, enable_events=True)],
            [
                sg.Button('Adicionar', key='-ADICIONAR-'),
                sg.Button('Editar', key='-EDITAR-'),
                sg.Button('Excluir', key='-EXCLUIR-'),
                sg.Button('Voltar', key='-VOLTAR-')
            ]
        ]

        self.__window = sg.Window('Categorias', layout, finalize=True)

    def pega_dados_categoria(self, dados_atuais: dict = None):
        is_edicao = bool(dados_atuais)
        titulo_janela = "Editar Categoria" if is_edicao else "Adicionar Nova Categoria"
        
        nome_default = dados_atuais['nome'] if is_edicao else ''
        tipo_default = dados_atuais['tipo_indicacao'] if is_edicao else 'filme'

        tipos_disponiveis = ['filme', 'ator', 'diretor']

        layout_form = [
            [sg.Text('Nome da Categoria:'), sg.Input(default_text=nome_default, key='-NOME-')],
            [sg.Text('Tipo de Indicação:'), sg.Combo(tipos_disponiveis, default_value=tipo_default, readonly=True, key='-TIPO-', disabled=is_edicao)],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]

        form_window = sg.Window(titulo_janela, layout_form)
        event, values = form_window.read()
        form_window.close()

        if event == 'Salvar':
            values['-NOME-'] = values['-NOME-'].strip().title()
            if values['-NOME-']:
                return values
        return None

    def open_lista(self):
        event, values = self.__window.read()
        return event, values

    def close_lista(self):
        if self.__window:
            self.__window.close()
        self.__window = None

    def show_message(self, titulo: str, mensagem: str):
        sg.Popup(titulo, mensagem)

    def show_confirm_message(self, titulo: str, mensagem: str):
        return sg.popup_yes_no(mensagem, title=titulo)

    def refresh_table(self, categorias_lista):
        dados_tabela = []
        for categoria in categorias_lista:
            dados_tabela.append([categoria.id, categoria.nome, categoria.tipo_indicacao.capitalize()])
        self.__window['-TABELA-'].update(values=dados_tabela)