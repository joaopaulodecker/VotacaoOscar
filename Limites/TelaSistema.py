import PySimpleGUI as sg

class TelaSistema:
    def __init__(self):
        self.__window = None

    def init_components(self, fase_atual_str: str):
        sg.theme('Reddit')

        layout = [
            [sg.Text('Sistema de Premiação Oscar', font=('Helvetica', 25), justification='center', expand_x=True)],
            [sg.Text(f"Fase Atual: {fase_atual_str}", key='-FASE-', font=('Helvetica', 12), justification='center', expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Button('Gerenciar Pessoas', key='1', size=(25,2)), sg.Button('Listar Atores', key='2', size=(25,2))],
            [sg.Button('Gerenciar Filmes', key='4', size=(25,2)), sg.Button('Listar Diretores', key='3', size=(25,2))],
            [sg.Button('Gerenciar Categorias', key='5', size=(25,2)), sg.Button('Gerenciar Indicações', key='6', size=(25,2))],
            [sg.Button('Gerenciar Votação', key='7', size=(25,2)), sg.Button('Ver Resultados', key='8', size=(25,2))],
            [sg.HorizontalSeparator()],
            [sg.Button('Encerrar Indicações / Abrir Votação', key='9', expand_x=True, button_color=('white', 'green'))],
            [sg.Button('Sair do Sistema', key='0', expand_x=True, button_color=('white', 'red'))]
        ]
        
        self.__window = sg.Window(
            'Menu Principal - Oscar',
            layout,
            finalize=True,
            element_justification='center'
        )

    def open(self):
        event, values = self.__window.read()
        if event == sg.WIN_CLOSED:
            return '0', values
        return event, values

    def close(self):
        if self.__window:
            self.__window.close()
        self.__window = None
    
    def update_fase(self, nova_fase_str: str):
        if self.__window:
            self.__window['-FASE-'].update(f"Fase Atual: {nova_fase_str}")

    def show_message(self, titulo: str, mensagem: str):
        sg.Popup(titulo, mensagem)