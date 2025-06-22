from Entidades.Nacionalidade import Nacionalidade
from Entidades.Ator import Ator
from Entidades.Diretor import Diretor
from Entidades.MembroAcademia import MembroAcademia
from Limites.TelaMembros import TelaMembros
from Excecoes.EntidadeDuplicadaException import EntidadeDuplicadaException
from Excecoes.OpcaoInvalida import OpcaoInvalida


class ControladorMembros:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_membros = TelaMembros()
        self.__membros = []
        self.__proximo_id = 1

    @property
    def membros(self):
        return self.__membros

    def _gerar_proximo_id(self):
        id_atual = self.__proximo_id
        self.__proximo_id += 1
        return id_atual

    def _existe_nome_membro(self, nome: str):
        for membro in self.__membros:
            if membro.nome.casefold() == nome.casefold():
                return True
        return False

    def abrir_menu(self):
        while True:
            try:
                opcao = self.__tela_membros.mostra_menu_membros()
                if opcao == 1:
                    self.cadastrar()
                elif opcao == 2:
                    self.alterar()
                elif opcao == 3:
                    self.excluir()
                elif opcao == 4:
                    self.listar(mostrar_msg_voltar=True)
                elif opcao == 0:
                    break
            except EntidadeDuplicadaException as e:
                self.__tela_membros.mostra_mensagem(str(e))
                self.__tela_membros.espera_input()
            except OpcaoInvalida as e:
                self.__tela_membros.mostra_mensagem(f"❌ {e}")
                self.__tela_membros.espera_input()

    def cadastrar(self):

        # 1. Pede os dados para a Tela. A Tela é responsável pelos inputs.
        dados_membro = self.__tela_membros.pega_dados_membro()
        if dados_membro is None:
            self.__tela_membros.mostra_mensagem("ℹ️Cadastro cancelado")
            self.__tela_membros.espera_input()
            return

        # 2. Valida os dados usando o metodo correto
        if self._existe_nome_membro(dados_membro["nome"]):
            raise EntidadeDuplicadaException(f"❌ Membro já registrado com o nome '{dados_membro['nome']}'.")

        # 3. Cria a entidade OBJETO
        tipo_pessoa = dados_membro.get('tipo_pessoa')
        # Gerar o ID que será usado para qualquer tipo de pessoa.
        novo_id = self._gerar_proximo_id()
        # Criar o objeto de Nacionalidade, que também é comum a todos.
        nacionalidade_obj = Nacionalidade(dados_membro.get('nacionalidade_str'))

        novo_membro_obj = None

        # Usamos if/elif para decidir qual objeto criar.
        if tipo_pessoa == 'ator':
            novo_membro_obj = Ator(id_=novo_id,
                                   nome=dados_membro.get('nome'),
                                   data_nascimento=dados_membro.get('data_nascimento'),
                                   nacionalidade=nacionalidade_obj,
                                   genero_artistico=dados_membro.get('genero_artistico'))
        elif tipo_pessoa == 'diretor':
            novo_membro_obj = Diretor(id_=novo_id,
                                      nome=dados_membro.get('nome'),
                                      data_nascimento=dados_membro.get('data_nascimento'),
                                      nacionalidade=nacionalidade_obj)
        elif tipo_pessoa == 'membro':
            novo_membro_obj = MembroAcademia(id_=novo_id,
                                             nome=dados_membro.get('nome'),
                                             data_nascimento=dados_membro.get('data_nascimento'),
                                             nacionalidade=nacionalidade_obj,
                                             funcao='membro')

        # 4. Adiciona o OBJETO à lista e mostra sucesso
        if novo_membro_obj:
            self.__membros.append(novo_membro_obj)
            self.__tela_membros.mostra_mensagem(
                f"✅ {tipo_pessoa.capitalize()} '{novo_membro_obj.nome}' cadastrado com sucesso!")
        else:
            self.__tela_membros.mostra_mensagem("❌ Tipo de pessoa desconhecido. Cadastro falhou.")
        self.__tela_membros.espera_input()

    def listar(self, mostrar_msg_voltar=False):
        """Prepara e exibe a lista de membros, incluindo o ID."""
        # 1. Prepara os dados
        dados_para_tela = [f"ID: {membro.id} | {membro.get_info_str()}" for membro in self.__membros]

        # 2. Delega todo o trabalho de exibicao para a tela em uma única chamada
        self.__tela_membros.mostra_lista_membros(dados_para_tela)

        # 3. Lógica de pausa (que já estava correta no seu código original)
        if mostrar_msg_voltar:
            self.__tela_membros.espera_input()

        # 4. Retorno (útil para os métodos alterar/excluir)
        return bool(self.__membros)

    def alterar(self):
        # 1: Verificar se a lista não está vazia.
        if not self.membros:
            self.__tela_membros.mostra_mensagem("📭 Nenhuma pessoa cadastrada para alterar.")
            self.__tela_membros.espera_input()
            return

        # 2: Mostra a lista para o usuário saber qual ID escolher
        self.listar()

        # 3. Pede o ID para a tela
        id_alvo = self.__tela_membros.pegar_id(mensagem="Digite o ID do Membro que deseja alterar: ")
        if id_alvo is None:
            self.__tela_membros.mostra_mensagem("ℹ️ Alteração cancelada.")
            self.__tela_membros.espera_input()
            return

        # 3. Busca o OBJETO na lista
        membro_alvo = self.buscar_por_id(id_alvo)
        if not membro_alvo:
            self.__tela_membros.mostra_mensagem(f"❌ Membro com ID {id_alvo} não encontrado.")
            self.__tela_membros.espera_input()
            return

        # 5. Prepara os dados atuais e pede os novos para a tela
        dados_atuais = {
            "nome": membro_alvo.nome,
            "data_nascimento": membro_alvo.data_nascimento
        }
        novos_dados = self.__tela_membros.pega_dados_membro(dados_atuais=dados_atuais)

        # 6. Se recebeu novos dados, valida e atualiza o objeto
        if novos_dados:
            novo_nome = novos_dados.get("nome")
            # Validação para não permitir nomes duplicados
            if membro_alvo.nome.casefold() != novo_nome.casefold() and self._existe_nome_membro(novo_nome):
                self.__tela_membros.mostra_mensagem(f"❌ Já existe outro membro com o nome '{novo_nome}'.")
            else:
                # Atualizando os atributos do objeto diretamente
                membro_alvo.nome = novo_nome
                membro_alvo.data_nascimento = novos_dados.get("data_nascimento")
                self.__tela_membros.mostra_mensagem("✅ Alteração realizada com sucesso!")
        else:
            self.__tela_membros.mostra_mensagem("ℹ️ Nenhuma alteração realizada.")
        self.__tela_membros.espera_input()

    def excluir(self):
        if not self.__membros:
            self.__tela_membros.mostra_mensagem("📭 Nenhuma pessoa cadastrada para excluir.")
            self.__tela_membros.espera_input()
            return

        self.listar()
        id_alvo = self.__tela_membros.pegar_id(mensagem="\nDigite o ID do membro que deseja excluir: ")
        if id_alvo is None:
            self.__tela_membros.mostra_mensagem("ℹ️ Exclusão cancelada.")
            self.__tela_membros.espera_input()
            return

        membro_alvo = self.buscar_por_id(id_alvo)

        if not membro_alvo:
            self.__tela_membros.mostra_mensagem(f"❌ Membro com ID {id_alvo} não encontrado.")
        elif self.__tela_membros.confirma_exclusao(membro_alvo.nome):
            self.__membros.remove(membro_alvo)
            self.__tela_membros.mostra_mensagem("🗑️ Registro excluído com sucesso.")
        else:
            self.__tela_membros.mostra_mensagem("ℹ️ Exclusão cancelada pelo usuário.")

        self.__tela_membros.espera_input()

    def buscar_por_id(self, id_busca):
        for membro in self.__membros:
            if membro.id == id_busca:
                return membro
        return None

    def buscar_por_funcao_e_genero(self, funcao_busca: str, genero_alvo: str = None):
        membros_aptos = []
        for membro in self.__membros:
            if isinstance(membro, Diretor) and funcao_busca == 'diretor':
                membros_aptos.append(membro)
            elif isinstance(membro, Ator) and funcao_busca == 'ator':
                if genero_alvo:
                    if membro.genero_artistico == genero_alvo:
                        membros_aptos.append(membro)
                else:
                    membros_aptos.append(membro)
        return membros_aptos

