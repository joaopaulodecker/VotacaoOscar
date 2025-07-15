import PySimpleGUI as sg

class TelaVotacao:
    """Responsável pela interface gráfica do gerenciamento de Votação."""
    def __init__(self):
        self.__window = None
        sg.theme('DarkAmber')

    def init_components(self):
        """Prepara a janela principal com as opções de votação."""
        layout = [
            [sg.Text('Menu de Votação', font=('Helvetica', 25), justification='center', expand_x=True, pad=(0,10))],
            [sg.Button('Registrar Novo Voto', key='-REGISTRAR-', size=(30,2), pad=(0,10))],
            [sg.Button('Ver Resultados da Votação', key='-RESULTADOS-', size=(30,2))],
            [sg.Push(), sg.Button('Voltar', key='-VOLTAR-'), sg.Push()]
        ]
        self.__window = sg.Window('Votação', layout, element_justification='center')

    def pega_dados_votacao_passo1(self, membros_map: dict, categorias_map: dict):
        """Abre o formulário do Passo 1: selecionar Votante e Categoria."""
        layout_form = [
            [sg.Text('Passo 1: Selecione o Votante e a Categoria', font=('Helvetica', 15))],
            [sg.Text('Membro Votante:')],
            [sg.Listbox(values=list(membros_map.keys()), size=(60, 5), key='-MEMBRO-', expand_x=True)],
            [sg.Text('Categoria:')],
            [sg.Listbox(values=list(categorias_map.keys()), size=(60, 5), key='-CATEGORIA-', expand_x=True)],
            [sg.Submit('Próximo'), sg.Cancel('Cancelar')]
        ]
        form_window = sg.Window("Registrar Novo Voto - Passo 1", layout_form, modal=True)
        event, values = form_window.read()
        form_window.close()
        if event == 'Próximo':
            return values
        return None

    def pega_dados_votacao_passo2(self, finalistas_map: dict, nome_categoria: str):
        """Abre o formulário do Passo 2: selecionar o finalista."""
        layout_finalistas = [
            [sg.Text(f'Categoria: {nome_categoria}', font=('Helvetica', 12), justification='center', expand_x=True)],
            [sg.Text('Passo 2: Selecione seu Voto', font=('Helvetica', 15))],
            [sg.Listbox(values=list(finalistas_map.keys()), size=(50, 10), key='-FINALISTA-', expand_x=True)],
            [sg.Submit('Salvar Voto'), sg.Cancel('Cancelar')]
        ]
        form_window = sg.Window("Registrar Novo Voto - Passo 2", layout_finalistas, modal=True)
        event, values = form_window.read()
        form_window.close()
        if event == 'Salvar Voto':
            return values
        return None

    def mostra_resultados(self, resultados_finais: list):
        """
        Cria uma janela personalizada e emocionante para anunciar os vencedores
        """
        if not resultados_finais:
            self.show_message("Resultados", "Nenhum voto registrado para exibir.")
            return

        layout_resultados = [
            [sg.Text('E o Oscar vai para...', font=('Helvetica', 25), justification='center', expand_x=True, pad=(0,10))],
            [sg.HorizontalSeparator(pad=(0,10))]
        ]

        # Para cada vencedor que o controlador enviou, criamos uma seção no layout
        for resultado in resultados_finais:
            layout_resultados.extend([
                [sg.Text(f"🏆 {resultado['categoria']}", font=('Helvetica', 14, 'bold'))],
                [sg.Text(f"Vencedor(a): {resultado['vencedor']}", font=('Helvetica', 12), pad=(15,0))],
                [sg.Text(f"Com {resultado['votos']} voto(s)", font=('Helvetica', 10, 'italic'), pad=(15, 5))],
                [sg.HorizontalSeparator(pad=(0,10))]
            ])

        layout_resultados.append([sg.Push(), sg.Button('Ok', size=(10,1)), sg.Push()])
        sg.Window("Resultados Finais do Oscar", layout_resultados, element_justification='c').read(close=True)

    def open(self):
        """Lê um evento da janela principal de votação."""
        event, values = self.__window.read()
        return event, values

    def close(self):
        """Fecha a janela principal de votação."""
        if self.__window:
            self.__window.close()
        self.__window = None

    @staticmethod
    def show_message(titulo: str, mensagem: str):
        """Exibe uma mensagem de pop-up simples."""
        sg.Popup(titulo, mensagem)