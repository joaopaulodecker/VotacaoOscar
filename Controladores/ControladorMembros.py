from Entidades.Nacionalidade import Nacionalidade
from Entidades.Ator import Ator
from Entidades.Diretor import Diretor
from Entidades.MembroAcademia import MembroAcademia
from Limites.TelaMembros import TelaMembros
from DAOs.MembroDao import MembroDAO

class ControladorMembros:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__dao = MembroDAO()
        self.__tela_membros = TelaMembros()

    @property
    def membros(self):
        return self.__dao.get_all()

    def _gerar_proximo_id(self):
        todos_membros = self.__dao.get_all()
        if not todos_membros:
            return 1
        return max(membro.id for membro in todos_membros) + 1

    def _existe_nome_membro(self, nome: str, id_excluir: int = None):
        for membro in self.__dao.get_all():
            if id_excluir is not None and membro.id == id_excluir:
                continue
            if membro.nome.casefold() == nome.casefold():
                return True
        return False

    def abrir_menu(self):
        self.__tela_membros.init_components_lista(self.membros)
        while True:
            event, values = self.__tela_membros.open_lista()

            if event in (None, '-VOLTAR-'):
                break

            if event == '-ADICIONAR-':
                self.cadastrar()
            
            elif values['-TABELA-']:
                index_selecionado = values['-TABELA-'][0]
                membro_selecionado = self.membros[index_selecionado]

                if event == '-EDITAR-':
                    self.alterar(membro_selecionado)
                elif event == '-EXCLUIR-':
                    self.excluir(membro_selecionado)
            elif event in ('-EDITAR-', '-EXCLUIR-'):
                self.__tela_membros.show_message("Aviso", "Por favor, selecione uma pessoa na tabela primeiro.")

        self.__tela_membros.close_lista()

    def cadastrar(self):
        dados_membro = self.__tela_membros.pega_dados_membro()
        if dados_membro:
            nome = dados_membro["-NOME-"]
            if self._existe_nome_membro(nome):
                self.__tela_membros.show_message("Erro", f"❌ Já existe uma pessoa com o nome '{nome}'.")
                return
            
            novo_id = self._gerar_proximo_id()
            nacionalidade_obj = Nacionalidade(dados_membro["-NACIONALIDADE-"])
            data_nasc = int(dados_membro["-NASCIMENTO-"])
            novo_membro_obj = None

            if dados_membro["-TIPO_ATOR-"]:
                genero = "Ator" if dados_membro["-GENERO_ATOR-"] else "Atriz"
                novo_membro_obj = Ator(novo_id, nome, data_nasc, nacionalidade_obj, genero)
            elif dados_membro["-TIPO_DIRETOR-"]:
                novo_membro_obj = Diretor(novo_id, nome, data_nasc, nacionalidade_obj)
            elif dados_membro["-TIPO_MEMBRO-"]:
                novo_membro_obj = MembroAcademia(novo_id, nome, data_nasc, nacionalidade_obj, "membro")
            
            if novo_membro_obj:
                self.__dao.add(novo_id, novo_membro_obj)
                self.__tela_membros.show_message("Sucesso", "✅ Pessoa cadastrada com sucesso.")
                self.__tela_membros.refresh_table(self.membros)

    def alterar(self, membro_alvo):
        from Entidades.Ator import Ator

        dados_atuais = {
            'nome': membro_alvo.nome,
            'data_nascimento': membro_alvo.data_nascimento,
            'nacionalidade_str': membro_alvo.nacionalidade.pais,
            'tipo_pessoa': 'ator' if isinstance(membro_alvo, Ator) else 'outro'
        }
        if isinstance(membro_alvo, Ator):
            dados_atuais['genero_artistico'] = membro_alvo.genero_artistico
            
        novos_dados = self.__tela_membros.pega_dados_membro(dados_atuais=dados_atuais)

        if novos_dados:
            novo_nome = novos_dados["-NOME-"]
            if (membro_alvo.nome.casefold() != novo_nome.casefold() and 
                    self._existe_nome_membro(novo_nome, id_excluir=membro_alvo.id)):
                self.__tela_membros.show_message("Erro", f"❌ Já existe outra pessoa com o nome '{novo_nome}'.")
                return

            membro_alvo.nome = novo_nome
            membro_alvo.data_nascimento = int(novos_dados["-NASCIMENTO-"])
            membro_alvo.nacionalidade = Nacionalidade(novos_dados["-NACIONALIDADE-"])
            if isinstance(membro_alvo, Ator):
                membro_alvo.genero_artistico = "Ator" if novos_dados["-GENERO_ATOR-"] else "Atriz"
            
            self.__dao.add(membro_alvo.id, membro_alvo)
            self.__tela_membros.show_message("Sucesso", "✅ Alteração realizada com sucesso!")
            self.__tela_membros.refresh_table(self.membros)

    def excluir(self, membro_alvo):
        confirmado = self.__tela_membros.show_confirm_message(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir '{membro_alvo.nome}'?"
        )
        if confirmado == 'Yes':
            self.__dao.remove(membro_alvo.id)
            self.__tela_membros.show_message("Sucesso", "🗑️ Pessoa removida com sucesso.")
            self.__tela_membros.refresh_table(self.membros)

    def buscar_por_id(self, id_busca):
        return self.__dao.get(id_busca)

    def buscar_por_funcao_e_genero(self, funcao_busca: str, genero_alvo: str = None):
        from Entidades.Diretor import Diretor
        from Entidades.Ator import Ator
        
        membros_aptos = []
        for membro in self.__dao.get_all():
            if isinstance(membro, Diretor) and funcao_busca == 'diretor':
                membros_aptos.append(membro)
            elif isinstance(membro, Ator) and funcao_busca == 'ator':
                if genero_alvo:
                    if membro.genero_artistico == genero_alvo:
                        membros_aptos.append(membro)
                else:
                    membros_aptos.append(membro)
        return membros_aptos