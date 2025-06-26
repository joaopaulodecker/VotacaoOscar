import PySimpleGUI as sg

class TelaFilmes:
    def __init__(self):
        self.__window = None


    def init_components_lista(self,  dados_prontos_da_tabela: list):
        sg.theme('DarkAmber')
        
        headings = ['ID', 'Título', 'Ano', 'Nacionalidade', 'Diretor']

        layout = [
            [sg.Text('Gerenciador de Filmes', font=('Helvetica', 25))],
            [sg.Table(values=dados_prontos_da_tabela, headings=headings, max_col_width=35,
                      auto_size_columns=True, justification='left', num_rows=10,
                      key='-TABELA-', row_height=25, enable_events=True)],
            [
                sg.Button('Adicionar', key='-ADICIONAR-'),
                sg.Button('Editar', key='-EDITAR-'),
                sg.Button('Excluir', key='-EXCLUIR-'),
                sg.Button('Agrupar por Nacionalidade', key='-AGRUPAR-'),
                sg.Button('Voltar', key='-VOLTAR-')
            ]
        ]

        self.__window = sg.Window('Filmes', layout, finalize=True)

    def pega_dados_filme(self, diretores_lista, dados_atuais: dict = None):
        is_edicao = bool(dados_atuais)
        titulo_janela = "Editar Filme" if is_edicao else "Adicionar Novo Filme"
        
        titulo_default = dados_atuais.get('titulo', '')
        ano_default = dados_atuais.get('ano', '')
        nac_default = dados_atuais.get('nacionalidade_str', '')
        
        diretor_selecionado_default = None
        if is_edicao and dados_atuais.get('diretor_id'):
            for diretor in diretores_lista:
                if diretor.id == dados_atuais['diretor_id']:
                    diretor_selecionado_default = f"ID: {diretor.id} - {diretor.nome}"
                    break
        
        mapa_diretores_display = [f"ID: {d.id} - {d.nome}" for d in diretores_lista]

        layout_form = [
            [sg.Text('Título:', size=(15,1)), sg.Input(default_text=titulo_default, key='-TITULO-')],
            [sg.Text('Ano:', size=(15,1)), sg.Input(default_text=ano_default, key='-ANO-')],
            [sg.Text('Nacionalidade:', size=(15,1)), sg.Input(default_text=nac_default, key='-NACIONALIDADE-')],
            [sg.Text('Diretor:', size=(15,1)), sg.Combo(mapa_diretores_display, default_value=diretor_selecionado_default, readonly=True, key='-DIRETOR-', expand_x=True)],
            [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
        ]

        form_window = sg.Window(titulo_janela, layout_form, finalize=True)
        while True:
            event, values = form_window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                form_window.close()
                return None

            if event == 'Salvar':
                erros = []
                if not values['-TITULO-'].strip():
                    erros.append("O campo 'Título' é obrigatório.")
                if not values['-NACIONALIDADE-'].strip():
                    erros.append("O campo 'Nacionalidade' é obrigatório.")
                if not values['-DIRETOR-']:
                    erros.append("A seleção de um 'Diretor' é obrigatória.")

                try:
                    int(values['-ANO-'])  # Apenas checa se é um número, a validação de range fica no controlador
                except (ValueError, TypeError):
                    erros.append("O 'Ano' deve ser um número inteiro válido.")

                if erros:
                    self.show_message("Erros de Validação", "\n".join(erros))
                    continue

                # Se passou, extrai o ID do diretor e retorna
                id_diretor_str = values['-DIRETOR-'].split(' ')[1]
                values['-DIRETOR_ID-'] = int(id_diretor_str)
                values['-ANO-'] = int(values['-ANO-'])
                form_window.close()
                return values

    def mostra_filmes_agrupados(self, filmes_agrupados: dict):
        texto_final = ""
        for pais, lista_filmes in filmes_agrupados.items():
            texto_final += f"🌍 Nacionalidade: {pais}\n" + "-"*30 + "\n"
            for filme_info in lista_filmes:
                texto_final += f"  ID: {filme_info['id']}. 🎬 {filme_info['titulo']} ({filme_info['ano']}) (Dir: {filme_info['diretor']})\n"
            texto_final += "\n"
        
        self.show_message("Filmes Agrupados por Nacionalidade", texto_final)

    def open_lista(self):
        event, values = self.__window.read()
        return event, values

    def close_lista(self):
        if self.__window:
            self.__window.close()
        self.__window = None

    @staticmethod
    def show_message(titulo: str, mensagem: str):
        sg.Popup(titulo, mensagem, grab_anywhere=True)

    @staticmethod
    def show_confirm_message(titulo: str, mensagem: str):
        return sg.popup_yes_no(mensagem, title=titulo)

    def refresh_table(self, dados_prontos_da_tabela: list):
        self.__window['-TABELA-'].update(values=dados_prontos_da_tabela)