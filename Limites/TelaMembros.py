import PySimpleGUI as sg
from datetime import date

class TelaMembros:
    def __init__(self):
        self.__window = None

    def init_components_lista(self, membros_lista):
        sg.theme('Reddit')
        
        headings = ['ID', 'Nome', 'Nascimento', 'Nacionalidade', 'Tipo', 'Gênero Art.']
        
        dados_tabela = []
        for membro in membros_lista:
            tipo = "Indefinido"
            genero = "N/A"
            from Entidades.Ator import Ator
            from Entidades.Diretor import Diretor
            
            if isinstance(membro, Ator):
                tipo = "Ator/Atriz"
                genero = membro.genero_artistico
            elif isinstance(membro, Diretor):
                tipo = "Diretor(a)"
            else:
                tipo = "Membro da Academia"

            dados_tabela.append([
                membro.id, membro.nome, membro.data_nascimento, 
                membro.nacionalidade.pais, tipo, genero
            ])

        layout = [
            [sg.Text('Gerenciador de Pessoas', font=('Helvetica', 25))],
            [sg.Table(values=dados_tabela, headings=headings, max_col_width=25,
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
        else:
            nome_default = ''
            nasc_default = ''
            nac_default = ''
            genero_default = 'Ator'
        
        tipo_pessoa = dados_atuais.get('tipo_pessoa', 'ator') if is_edicao else 'ator'
        
        layout_form = [
            [sg.Text('Nome:', size=(15,1)), sg.Input(default_text=nome_default, key='-NOME-')],
            [sg.Text('Ano Nascimento:', size=(15,1)), sg.Input(default_text=nasc_default, key='-NASCIMENTO-')],
            [sg.Text('Nacionalidade:', size=(15,1)), sg.Input(default_text=nac_default, key='-NACIONALIDADE-')],
        ]

        if not is_edicao:
            layout_form.append([sg.Frame('Tipo de Pessoa', [
                [sg.Radio('Ator/Atriz', 'RADIO_TIPO', default=True, key='-TIPO_ATOR-')],
                [sg.Radio('Diretor(a)', 'RADIO_TIPO', key='-TIPO_DIRETOR-')],
                [sg.Radio('Membro Academia', 'RADIO_TIPO', key='-TIPO_MEMBRO-')],
            ])])
        
        layout_form.append([sg.Frame('Dados de Ator/Atriz', [
            [sg.Radio('Ator', 'RADIO_GENERO', default=(genero_default == 'Ator'), key='-GENERO_ATOR-')],
            [sg.Radio('Atriz', 'RADIO_GENERO', default=(genero_default == 'Atriz'), key='-GENERO_ATRIZ-')],
        ], key='-FRAME_ATOR-')])

        layout_form.append([sg.Submit('Salvar'), sg.Cancel('Cancelar')])

        form_window = sg.Window(titulo_janela, layout_form)
        
        while True:
            event, values = form_window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                form_window.close()
                return None
            
            if event == 'Salvar':
                try:
                    if not values['-NOME-'].strip():
                        self.show_message("Erro de Validação", "O campo 'Nome' não pode ser vazio.")
                        continue
                    
                    ano_nasc = int(values['-NASCIMENTO-'])
                    ano_atual = date.today().year
                    if not (1900 <= ano_nasc <= ano_atual):
                         self.show_message("Erro de Validação", f"O ano de nascimento deve estar entre 1900 e {ano_atual}.")
                         continue

                    if not values['-NACIONALIDADE-'].strip():
                        self.show_message("Erro de Validação", "O campo 'Nacionalidade' não pode ser vazio.")
                        continue
                    
                    form_window.close()
                    return values

                except (ValueError, TypeError):
                    self.show_message("Erro de Validação", "Ano de nascimento deve ser um número válido.")

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

    def refresh_table(self, membros_lista):
        dados_tabela = []
        for membro in membros_lista:
            tipo = "Indefinido"
            genero = "N/A"
            from Entidades.Ator import Ator
            from Entidades.Diretor import Diretor
            
            if isinstance(membro, Ator):
                tipo = "Ator/Atriz"
                genero = membro.genero_artistico
            elif isinstance(membro, Diretor):
                tipo = "Diretor(a)"
            else:
                tipo = "Membro da Academia"

            dados_tabela.append([
                membro.id, membro.nome, membro.data_nascimento, 
                membro.nacionalidade.pais, tipo, genero
            ])
        self.__window['-TABELA-'].update(values=dados_tabela)