from datetime import date
from Entidades.Nacionalidade import Nacionalidade
from Entidades.Ator import Ator
from Entidades.Diretor import Diretor
from Entidades.MembroAcademia import MembroAcademia
from Excecoes.EntidadeDuplicadaException import EntidadeDuplicadaException
from Excecoes.AnoInvalidoException import AnoInvalidoException
from Limites.TelaMembros import TelaMembros
from DAOs.MembroDao import MembroDAO


class ControladorMembros:
    """Controlador principal para as regras de negócio de Membros."""

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__dao = MembroDAO()
        self.__tela_membros = TelaMembros()

    def get_membros(self):
        """Metodo público para fornecer a lista de todos os membros."""
        return self.__dao.get_all()

    # --- MÉTODOS DE PREPARAÇÃO E BUSCA ---

    def _preparar_dados_tabela(self):
        """Busca os membros e os formata para a tabela da interface."""
        membros = self.get_membros()
        dados_tabela = []
        for membro in membros:
            genero = "N/A"
            # Define o 'Tipo' e o 'Gênero' baseado na classe do objeto
            if isinstance(membro, Ator):
                tipo = "Ator/Atriz"
                genero = membro.genero_artistico
            elif isinstance(membro, Diretor):
                tipo = "Diretor(a)"
            else:
                tipo = "Membro Academia"

            dados_tabela.append(
                [membro.id, membro.nome, membro.data_nascimento, membro.nacionalidade.pais, tipo, genero])
        return dados_tabela

    def buscar_por_id(self, id_busca: int):
        """Busca um membro pelo seu ID no DAO."""
        return self.__dao.get(id_busca)

    def _existe_nome_membro(self, nome: str, id_excluir: int = None):
        """Verifica se um nome de membro já existe."""
        for membro in self.get_membros():
            if id_excluir is not None and membro.id == id_excluir:
                continue
            if membro.nome.casefold() == nome.casefold():
                return True
        return False

    def buscar_por_funcao_e_genero(self, funcao_busca: str, genero_alvo: str = None):
        """Busca membros por tipo e, opcionalmente, por gênero artístico."""
        membros_aptos = []
        for membro in self.get_membros():
            if isinstance(membro, Diretor) and funcao_busca == 'diretor':
                membros_aptos.append(membro)
            elif isinstance(membro, Ator) and funcao_busca == 'ator':
                if genero_alvo is None or membro.genero_artistico == genero_alvo:
                    membros_aptos.append(membro)
        return membros_aptos

    # --- MÉTODOS DE ORQUESTRAÇÃO DE TELAS (CRUD) ---

    def abre_tela(self):
        """Abre a tela principal e gerencia o loop de eventos."""
        dados_tabela = self._preparar_dados_tabela()
        self.__tela_membros.init_components_lista(dados_tabela)

        while True:
            event, values = self.__tela_membros.open_lista()
            if event in (None, '-VOLTAR-'):
                self.__tela_membros.close_lista()
                break

            # --- LÓGICA DE EVENTOS ---
            if event == '-ADICIONAR-':
                self.cadastrar()

            elif event in ('-EDITAR-', '-EXCLUIR-'):
                if values.get('-TABELA-'):
                    index_selecionado = values['-TABELA-'][0]
                    id_membro_selecionado = dados_tabela[index_selecionado][0]
                    membro_alvo = self.buscar_por_id(id_membro_selecionado)

                    if membro_alvo and event == '-EDITAR-':
                        self.alterar(membro_alvo)
                    elif membro_alvo and event == '-EXCLUIR-':
                        self.excluir(membro_alvo)
                else:
                    self.__tela_membros.show_message("Aviso", "Por favor, selecione uma pessoa na tabela primeiro.")

            if event in ('-ADICIONAR-', '-EDITAR-', '-EXCLUIR-'):
                dados_tabela = self._preparar_dados_tabela()
                self.__tela_membros.refresh_table(dados_tabela)

    def cadastrar(self):
        """Orquestra o processo de cadastro de um novo membro com validação robusta."""
        dados_brutos = self.__tela_membros.pega_dados_membro({
            'titulo_janela': "Adicionar Pessoa", 'is_ator': True
        })

        if dados_brutos:
            try:
                # Tenta executar toda a lógica de validação e criação
                nome = dados_brutos["-NOME-"].strip().title()
                nacionalidade_str = dados_brutos["-NACIONALIDADE-"].strip().title()
                ano_nasc_str = dados_brutos["-NASCIMENTO-"]

                if not nome or not nacionalidade_str:
                    raise ValueError("Os campos 'Nome' e 'Nacionalidade' são obrigatórios.")

                if self._existe_nome_membro(nome):
                    raise EntidadeDuplicadaException(nome)

                if any(c.isdigit() for c in nacionalidade_str):
                    raise ValueError("O campo 'Nacionalidade' não pode conter números.")

                try:
                    ano_nasc = int(ano_nasc_str)
                    if not (1900 <= ano_nasc <= date.today().year):
                        raise AnoInvalidoException(ano_nasc_str)
                except ValueError:
                    raise AnoInvalidoException(ano_nasc_str)

                # Se tudo deu certo, cria o objeto correto
                novo_id = self.__dao.get_next_id()
                nacionalidade_obj = Nacionalidade(nacionalidade_str)
                novo_membro = None

                if dados_brutos["-TIPO_ATOR-"]:
                    genero = "Atriz" if dados_brutos["-GENERO_ATRIZ-"] else "Ator"
                    novo_membro = Ator(id_=novo_id, nome=nome, data_nascimento=ano_nasc,
                                       nacionalidade=nacionalidade_obj, genero_artistico=genero)
                elif dados_brutos["-TIPO_DIRETOR-"]:
                    novo_membro = Diretor(id_=novo_id, nome=nome, data_nascimento=ano_nasc,
                                          nacionalidade=nacionalidade_obj)
                elif dados_brutos["-TIPO_MEMBRO-"]:
                    novo_membro = MembroAcademia(id_=novo_id, nome=nome, data_nascimento=ano_nasc,
                                                 nacionalidade=nacionalidade_obj, funcao="membro")

                if novo_membro:
                    self.__dao.add(key=novo_id, membro=novo_membro)
                    self.__tela_membros.show_message("Sucesso", "Pessoa cadastrada com sucesso.")
                else:
                    raise ValueError("Um tipo de pessoa deve ser selecionado.")

            except (ValueError, AnoInvalidoException, EntidadeDuplicadaException) as e:
                self.__tela_membros.show_message("Erro de Validação", str(e))

    def alterar(self, membro_alvo):
        """Orquestra a alteração de um membro existente com validação robusta."""
        is_ator = isinstance(membro_alvo, Ator)
        dados_iniciais = {
            'titulo_janela': "Editar Pessoa", 'is_edicao': True, 'is_ator': is_ator,
            'nome': membro_alvo.nome, 'data_nascimento': str(membro_alvo.data_nascimento),
            'nacionalidade_str': membro_alvo.nacionalidade.pais
        }
        if is_ator:
            dados_iniciais['genero_artistico'] = membro_alvo.genero_artistico

        dados_brutos = self.__tela_membros.pega_dados_membro(dados_iniciais)
        if dados_brutos:
            try:
                novo_nome = dados_brutos["-NOME-"].strip().title()
                nacionalidade_str = dados_brutos["-NACIONALIDADE-"].strip().title()
                ano_nasc_str = dados_brutos["-NASCIMENTO-"]

                if not novo_nome or not nacionalidade_str:
                    raise ValueError("Os campos 'Nome' e 'Nacionalidade' são obrigatórios.")

                if (membro_alvo.nome.casefold() != novo_nome.casefold() and
                        self._existe_nome_membro(novo_nome, id_excluir=membro_alvo.id)):
                    raise EntidadeDuplicadaException(novo_nome)

                if any(c.isdigit() for c in nacionalidade_str):
                    raise ValueError("O campo 'Nacionalidade' não pode conter números.")

                try:
                    ano_nasc = int(ano_nasc_str)
                    if not (1900 <= ano_nasc <= date.today().year):
                        raise AnoInvalidoException(ano_nasc_str)
                except ValueError:
                    raise AnoInvalidoException(ano_nasc_str)

                # Atualiza o objeto original
                membro_alvo.nome = novo_nome
                membro_alvo.data_nascimento = ano_nasc
                membro_alvo.nacionalidade = Nacionalidade(nacionalidade_str)
                if isinstance(membro_alvo, Ator):
                    membro_alvo.genero_artistico = "Atriz" if dados_brutos["-GENERO_ATRIZ-"] else "Ator"

                self.__dao.add(key=membro_alvo.id, membro=membro_alvo)
                self.__tela_membros.show_message("Sucesso", "Alteração realizada com sucesso!")

            except (ValueError, AnoInvalidoException, EntidadeDuplicadaException) as e:
                self.__tela_membros.show_message("Erro de Validação", str(e))

    def excluir(self, membro_alvo):
        """Orquestra a exclusão de um membro."""
        confirmado = self.__tela_membros.show_confirm_message(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir '{membro_alvo.nome}'?"
        )
        if confirmado == 'Yes':
            self.__dao.remove(membro_alvo.id)
            self.__tela_membros.show_message("Sucesso", "Pessoa removida com sucesso.")