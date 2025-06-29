import PySimpleGUI as sg

class TelaSistema:
    """Responsável pela interface gráfica do menu principal do sistema."""
    def __init__(self):
        self.__window = None
        sg.theme('DarkAmber')

    def init_components(self, fase_premiacao: str):
        """Prepara a janela principal do sistema."""
        # Layout organizado em colunas para melhor alinhamento
        coluna_cadastros = [
            [sg.Button('Gerenciar Pessoas', key='-MEMBROS-', size=(25, 2))],
            [sg.Button('Gerenciar Filmes', key='-FILMES-', size=(25, 2))],
            [sg.Button('Gerenciar Categorias', key='-CATEGORIAS-', size=(25, 2))],
        ]
        coluna_processos = [
            [sg.Button('Registrar Indicações', key='-INDICACOES-', size=(25, 2))],
            [sg.Button('Registrar Votos', key='-VOTACAO-', size=(25, 2))],
            [sg.Button('Ver Resultados Finais', key='-RESULTADOS-', size=(25, 2))],
        ]

        layout = [
            [sg.Text('Sistema de Premiação Oscar', font=('Helvetica', 25), justification='center', expand_x=True, pad=(0,10))],
            [sg.Text(f"Fase Atual: {fase_premiacao}", key='-FASE-', font=('Helvetica', 12), justification='center', expand_x=True, pad=(0,10))],
            [sg.HorizontalSeparator(pad=(0,15))],
            [
                sg.Column(coluna_cadastros, element_justification='c'),
                sg.VSeparator(),
                sg.Column(coluna_processos, element_justification='c')
            ],
            [sg.HorizontalSeparator(pad=(0,15))],
            [
                sg.Button('Avançar Fase (Encerrar Indicações)', key='-AVANCAR_FASE-', pad=(5,15)),
                sg.Push(),
                sg.Button('Sair', key='-SAIR-', pad=(5,15))
            ]
        ]
        self.__window = sg.Window('Sistema Oscar', layout)

    def open(self):
        """Lê um evento da janela principal do sistema."""
        event, values = self.__window.read()
        return event, values

    def close(self):
        """Fecha a janela principal do sistema."""
        self.__window.close()

    def update_fase(self, nova_fase: str):
        """Atualiza o texto da fase na janela."""
        self.__window['-FASE-'].update(f"Fase Atual: {nova_fase}")

    @staticmethod
    def show_message(titulo: str, mensagem: str):
        """Exibe uma mensagem de pop-up simples."""
        sg.Popup(titulo, mensagem)