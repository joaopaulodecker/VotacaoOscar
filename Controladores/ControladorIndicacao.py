from Entidades.Categoria import Categoria
from Entidades.Ator import Ator
from Entidades.Diretor import Diretor
from Entidades.IndAtor import IndAtor
from Entidades.IndDiretor import IndDiretor
from Entidades.IndFilme import IndFilme
from Limites.TelaIndicacao import TelaIndicacao
from DAOs.IndicacaoDao import IndicacaoDAO



class ControladorIndicacao:
    """Controlador principal para as regras de negócio de Indicações."""

    def __init__(self, controlador_sistema, controlador_membros,
                 controlador_categorias, controlador_filmes):
        self.__controlador_sistema = controlador_sistema
        self.__tela_indicacao = TelaIndicacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__controlador_filmes = controlador_filmes
        self.__dao = IndicacaoDAO()

    def _preparar_dados_tabela(self):
        """Busca as indicações e as formata para a tabela da interface."""
        indicacoes = self.__dao.get_all()
        # Mapa para buscar nomes de membros sem passar os objetos para a tela
        mapa_membros = {m.id: m.nome for m in self.__controlador_membros.get_membros()}
        dados_tabela = []
        for indicacao in indicacoes:
            nome_membro = mapa_membros.get(indicacao.membro_id, "ID não encontrado")
            dados_tabela.append([indicacao.id_indicacao, nome_membro, indicacao.categoria.nome,
                                 indicacao.obter_detalhes_item_indicado()])
        return dados_tabela

    def abre_tela(self):
        """Abre a tela principal e gerencia o loop de eventos."""
        dados_tabela = self._preparar_dados_tabela()
        self.__tela_indicacao.init_components(dados_tabela)

        while True:
            event, values = self.__tela_indicacao.open()
            if event in (None, '-VOLTAR-'):
                self.__tela_indicacao.close()
                break

            if event == '-ADICIONAR-':
                self.iniciar_processo_indicacao()

            elif event == '-EXCLUIR-':
                if values.get('-TABELA-'):
                    index_selecionado = values['-TABELA-'][0]
                    id_indicacao = dados_tabela[index_selecionado][0]
                    indicacao_alvo = self.__dao.get(id_indicacao)
                    if not indicacao_alvo: continue
                    self.excluir_indicacao(indicacao_alvo)
                else:
                    self.__tela_indicacao.show_message("Aviso",
                                                       "Por favor, selecione uma indicação na tabela primeiro.")

            if event in ('-ADICIONAR-', '-EXCLUIR-'):
                dados_tabela = self._preparar_dados_tabela()
                self.__tela_indicacao.refresh_table(dados_tabela)

    def iniciar_processo_indicacao(self):
        """Orquestra o fluxo de registrar uma nova indicação."""
        try:
            if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_INDICACOES_ABERTAS:
                raise ValueError("O período de indicações já foi encerrado.")

            # --- PASSO 1: Selecionar Indicante e Categoria ---
            categorias = self.__controlador_categorias.get_categorias()
            membros = self.__controlador_membros.get_membros()
            if not categorias or not membros:
                raise ValueError("É preciso ter Categorias e Membros cadastrados.")

            mapa_categorias = {f"ID {cat.id}: {cat.nome}": cat for cat in categorias}
            mapa_membros = {f"ID {m.id}: {m.nome}": m for m in membros}

            dados_passo1 = self.__tela_indicacao.pega_dados_indicacao_passo1(mapa_categorias, mapa_membros)
            if not dados_passo1 or not dados_passo1.get('-CATEGORIA-') or not dados_passo1.get('-MEMBRO-'):
                return  # Usuário cancelou, não é um erro

            membro_obj = mapa_membros[dados_passo1['-MEMBRO-'][0]]
            categoria_obj = mapa_categorias[dados_passo1['-CATEGORIA-'][0]]

            # --- Validação da Regra de Negócio do Oscar ---
            tipo_categoria = categoria_obj.tipo_indicacao
            if tipo_categoria in ("ator", "atriz") and not isinstance(membro_obj, Ator):
                raise ValueError("Acesso Negado: Apenas Atores/Atrizes podem indicar para esta categoria.")
            if tipo_categoria == "diretor" and not isinstance(membro_obj, Diretor):
                raise ValueError("Acesso Negado: Apenas Diretores podem indicar para esta categoria.")

            # --- PASSO 2: Selecionar o Indicado ---
            lista_indicaveis = self._get_lista_indicaveis(categoria_obj)
            if not lista_indicaveis:
                raise ValueError(f"Não há itens elegíveis para a categoria '{categoria_obj.nome}'.")

            mapa_indicaveis = {item['nome_display']: item for item in lista_indicaveis}
            dados_passo2 = self.__tela_indicacao.pega_dados_indicacao_passo2(mapa_indicaveis, categoria_obj.nome)
            if not dados_passo2 or not dados_passo2.get('-INDICADO-'):
                return  # Usuário cancelou

            item_indicado = mapa_indicaveis[dados_passo2['-INDICADO-'][0]]

            # --- Criação e Persistência ---
            novo_id = self.__dao.get_next_id()
            tipo_indicado = item_indicado['tipo_original_indicado']
            objeto_indicado = item_indicado['objeto_completo']
            nova_indicacao = None

            if tipo_indicado == 'filme':
                nova_indicacao = IndFilme(id_indicacao=novo_id, membro_id=membro_obj.id, categoria=categoria_obj,
                                          filme_indicado=objeto_indicado)
            elif tipo_indicado in ('ator', 'atriz'):
                nova_indicacao = IndAtor(id_indicacao=novo_id, membro_id=membro_obj.id, categoria=categoria_obj,
                                         ator_indicado=objeto_indicado)
            elif tipo_indicado == 'diretor':
                nova_indicacao = IndDiretor(id_indicacao=novo_id, membro_id=membro_obj.id, categoria=categoria_obj,
                                            diretor_indicado=objeto_indicado)

            if nova_indicacao:
                self.__dao.add(key=novo_id, indicacao=nova_indicacao)
                self.__tela_indicacao.show_message("Sucesso", "Indicação registrada com sucesso!")
            else:
                raise ValueError("Falha ao criar o objeto de indicação.")

        except ValueError as e:
            self.__tela_indicacao.show_message("Aviso", str(e))

    def excluir_indicacao(self, indicacao_alvo):
        """Exclui uma indicação que foi selecionada na tabela."""
        if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_INDICACOES_ABERTAS:
            self.__tela_indicacao.show_message("Aviso", "Não é possível excluir indicações após o início da votação.")
            return

        info = indicacao_alvo.obter_detalhes_item_indicado()
        confirmado = self.__tela_indicacao.show_confirm_message(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a indicação para '{info}'?"
        )
        if confirmado == 'Yes':
            self.__dao.remove(indicacao_alvo.id_indicacao)
            self.__tela_indicacao.show_message("Sucesso", "Indicação removida com sucesso!")

    def get_finalistas_por_categoria(self, categoria_id: int):
        """
        Calcula os 'finalistas' de uma categoria baseado no número de indicações.
        Este metodo é crucial para a Votação.
        """
        from collections import Counter

        contagem = Counter()
        indicacoes_da_categoria = [ind for ind in self.__dao.get_all() if ind.categoria.id == categoria_id]

        for indicacao in indicacoes_da_categoria:
            # A chave da contagem é o ID do item indicado (filme, ator, etc.)
            contagem[indicacao.item_indicado_id] += 1

        # Pega os 5 mais indicados (ou menos, se não houver 5)
        top_indicados = contagem.most_common(5)
        finalistas = []

        for id_item, _ in top_indicados:
            # Encontra a primeira indicação daquele item para pegar os detalhes
            for indicacao in indicacoes_da_categoria:
                if indicacao.item_indicado_id == id_item:
                    finalistas.append({
                        "nome_display": indicacao.obter_detalhes_item_indicado(),
                        "id_original_indicado": indicacao.item_indicado_id,
                        "tipo_original_indicado": indicacao.tipo_indicacao
                    })
                    break
        return finalistas

    def _get_lista_indicaveis(self, categoria_obj: Categoria) -> list:
        """Busca a lista de filmes ou membros e formata para a tela de seleção."""
        tipo_item = categoria_obj.tipo_indicacao
        lista_formatada, lista_crua = [], []

        if tipo_item == "filme":
            lista_crua = self.__controlador_filmes.get_filmes()
        elif tipo_item == "ator":
            lista_crua = self.__controlador_membros.buscar_por_funcao_e_genero("ator", genero_alvo="Ator")
        elif tipo_item == "atriz":
            lista_crua = self.__controlador_membros.buscar_por_funcao_e_genero("ator", genero_alvo="Atriz")
        elif tipo_item == "diretor":
            lista_crua = self.__controlador_membros.buscar_por_funcao_e_genero("diretor")

        for item in lista_crua:
            nome = item.titulo if tipo_item == 'filme' else item.nome
            lista_formatada.append({"nome_display": nome, "objeto_completo": item, "tipo_original_indicado": tipo_item})
        return lista_formatada