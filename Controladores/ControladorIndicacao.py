from collections import Counter

from Entidades.Categoria import Categoria
from Entidades.Filme import Filme
from Entidades.IndAtor import IndAtor
from Entidades.IndDiretor import IndDiretor
from Entidades.IndFilme import IndFilme
from Excecoes.OpcaoInvalida import OpcaoInvalida
from Limites.TelaIndicacao import TelaIndicacao


class ControladorIndicacao:

    def __init__(self, controlador_sistema, controlador_membros,
                 controlador_categorias, controlador_filmes):
        self.__controlador_sistema = controlador_sistema
        self.__tela_indicacao = TelaIndicacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__controlador_filmes = controlador_filmes
        self.__indicacoes = []
        self.__proximo_id_indicacao = 1

    def _gerar_proximo_id_indicacao(self):
        id_atual = self.__proximo_id_indicacao
        self.__proximo_id_indicacao += 1
        return id_atual

    def _preparar_dados_para_selecao(self, lista_entidades: list) -> list[dict]:
        """
        Converte listas de entidades ou dicionários em um formato simples
        para a tela exibir.
        """
        dados_para_tela = []
        for item in lista_entidades:
            if isinstance(item, Categoria):
                info = f"ID: {item.id} - Nome: {item.nome}"
                dados_para_tela.append({"id": item.id, "info": info})
            elif isinstance(item, Filme):
                info = (f"ID: {item.id_filme} - Título: {item.titulo} "
                        f"({item.ano})")
                dados_para_tela.append({"id": item.id_filme, "info": info})
            elif isinstance(item, dict): 
                info = f"ID: {item.get('id')} - Nome: {item.get('nome')}"
                dados_para_tela.append({"id": item.get('id'), "info": info})
        return dados_para_tela

    def abrir_menu_indicacoes(self):
        while True:
            try:
                opcao = self.__tela_indicacao.mostra_opcoes_indicacao()
                if opcao == 1:
                    self.iniciar_indicacao()
                elif opcao == 2:
                    self.listar_indicacoes_por_categoria()
                elif opcao == 0:
                    break
            except OpcaoInvalida as e:
                self.__tela_indicacao.mostra_mensagem(f"❌ {e}")
                self.__tela_indicacao.espera_input()
            except Exception as e:
                self.__tela_indicacao.mostra_mensagem(f"❌ Erro inesperado: {e}")
                self.__tela_indicacao.espera_input()

    def iniciar_indicacao(self):
        if self.__controlador_sistema.fase_atual_premiacao != \
           self.__controlador_sistema.FASE_INDICACOES_ABERTAS:
            self.__tela_indicacao.mostra_mensagem(
                "\n❌ O período de indicações já foi encerrado."
            )
            self.__tela_indicacao.espera_input()
            return

        self.__tela_indicacao.mostra_mensagem("\n--- Nova Indicação ---")

        membros = self.__controlador_membros.entidades
        if not membros:
            self.__tela_indicacao.mostra_mensagem(
                "❌ Nenhum membro cadastrado para fazer indicações."
            )
            self.__tela_indicacao.espera_input()
            return

        membros_dados = self._preparar_dados_para_selecao(membros)
        membro_escolhido = self.__tela_indicacao.seleciona_membro(membros_dados)
        if not membro_escolhido:
            self.__tela_indicacao.espera_input()
            return
        membro_id = membro_escolhido.get("id")

        categorias = self.__controlador_categorias.entidades
        if not categorias:
            self.__tela_indicacao.mostra_mensagem(
                "❌ Nenhuma categoria cadastrada para indicação."
            )
            self.__tela_indicacao.espera_input()
            return

        categorias_dados = self._preparar_dados_para_selecao(categorias)
        categoria_escolhida_dados = self.__tela_indicacao.seleciona_categoria(
            categorias_dados
        )
        if not categoria_escolhida_dados:
            self.__tela_indicacao.espera_input()
            return
        categoria_obj = self.__controlador_categorias.buscar_categoria_por_id(
            categoria_escolhida_dados.get('id')
        )

        tipo_item = categoria_obj.tipo_indicacao.lower()
        self.__tela_indicacao.mostra_mensagem(
            f"ℹ️ A categoria '{categoria_obj.nome}' aceita indicações do tipo: "
            f"{tipo_item.capitalize()}"
        )
        
        item_indicado_obj = self._selecionar_item_para_indicacao(tipo_item)
        if not item_indicado_obj:
            self.__tela_indicacao.mostra_mensagem(
                "ℹ️ Seleção do item a ser indicado cancelada ou inválida."
            )
            self.__tela_indicacao.espera_input()
            return

        id_item = (item_indicado_obj.id_filme if isinstance(item_indicado_obj, Filme)
                   else item_indicado_obj.get("id"))
        nome_item = (item_indicado_obj.titulo if isinstance(item_indicado_obj, Filme)
                     else item_indicado_obj.get("nome"))

        if self._indicacao_ja_existe(membro_id, categoria_obj.id, id_item, tipo_item):
            self.__tela_indicacao.mostra_mensagem(
                f"⚠️ O membro ID {membro_id} já indicou '{nome_item}' para "
                f"a categoria '{categoria_obj.nome}'."
            )
            self.__tela_indicacao.espera_input()
            return

        id_nova_indicacao = self._gerar_proximo_id_indicacao()
        nova_indicacao = self._criar_objeto_indicacao(
            id_nova_indicacao, membro_id, categoria_obj,
            tipo_item, item_indicado_obj
        )

        if nova_indicacao:
            self.__indicacoes.append(nova_indicacao)
            self.__tela_indicacao.mostra_mensagem(
                f"✅ Indicação de '{nome_item}' para '{categoria_obj.nome}' "
                "registrada com sucesso!"
            )
        else:
            self.__tela_indicacao.mostra_mensagem(
                "❌ Falha ao criar o objeto de indicação. Verifique os tipos."
            )
        self.__tela_indicacao.espera_input()

    def _selecionar_item_para_indicacao(self, tipo_item: str):
        """Busca a lista apropriada e chama a tela para seleção do item."""
        if tipo_item == "filme":
            filmes = self.__controlador_filmes.filmes
            if not filmes:
                self.__tela_indicacao.mostra_mensagem("❌ Nenhum filme cadastrado.")
                return None
            dados_tela = self._preparar_dados_para_selecao(filmes)
            escolha_dados = self.__tela_indicacao.seleciona_filme(dados_tela)
            return self.buscar_filme_por_id(escolha_dados.get('id')) if escolha_dados else None

        elif tipo_item in ["ator", "diretor"]:
            membros_aptos = self.__controlador_membros.buscar_por_funcao(tipo_item)
            if not membros_aptos:
                self.__tela_indicacao.mostra_mensagem(
                    f"❌ Nenhum(a) {tipo_item.capitalize()} cadastrado."
                )
                return None
            dados_tela = self._preparar_dados_para_selecao(membros_aptos)
            return self.__tela_indicacao.seleciona_membro_por_funcao(
                dados_tela, tipo_item.capitalize()
            )
        return None

    def _indicacao_ja_existe(self, membro_id, categoria_id, item_id, tipo_item):
        """Verifica se uma indicação idêntica já foi feita pelo mesmo membro."""
        for ind in self.__indicacoes:
            if (ind.membro_id == membro_id and
                    ind.categoria.id == categoria_id and
                    ind.item_indicado_id == item_id and
                    ind.tipo_item_indicado == tipo_item):
                return True
        return False
        
    def _criar_objeto_indicacao(self, id_ind, membro_id, cat_obj, tipo, item_obj):
        """Cria a instância correta da classe de indicação."""
        if tipo == "filme":
            return IndFilme(id_ind, membro_id, cat_obj, item_obj)
        elif tipo == "ator":
            return IndAtor(id_ind, membro_id, cat_obj, item_obj)
        elif tipo == "diretor":
            return IndDiretor(id_ind, membro_id, cat_obj, item_obj)
        return None

    def listar_indicacoes_por_categoria(self):
        """Permite ao usuário selecionar uma categoria e lista as indicações."""
        self.__tela_indicacao.mostra_mensagem("\n--- Indicações por Categoria ---")

        categorias = self.__controlador_categorias.entidades
        if not categorias:
            self.__tela_indicacao.mostra_mensagem("❌ Nenhuma categoria cadastrada.")
            self.__tela_indicacao.espera_input()
            return

        # 1. Controlador pede para a tela selecionar a categoria e recebe o ID
        categorias_dados = self._preparar_dados_para_selecao(categorias)
        cat_escolhida_dados = self.__tela_indicacao.seleciona_categoria(categorias_dados)
        if not cat_escolhida_dados:
            self.__tela_indicacao.espera_input()
            return

        # 2. Controlador busca a categoria completa usando o ID
        id_cat_escolhida = cat_escolhida_dados.get('id')

        # 3. Controlador prepara os dados para a TELA
        indicacoes_filtradas = [
            ind for ind in self.__indicacoes
            if ind.categoria.id == id_cat_escolhida
        ]

        dados_para_tela = [
            ind.obter_detalhes_item_indicado() for ind in indicacoes_filtradas
        ]

        nome_categoria = cat_escolhida_dados.get('info', 'Categoria')

        self.__tela_indicacao.mostra_lista_indicacoes(
            nome_categoria,
            dados_para_tela
        )
        self.__tela_indicacao.espera_input()

    def get_finalistas_por_categoria(self, categoria_id: int, limite: int = 5):
        """Calcula e retorna os finalistas para uma categoria."""
        indicacoes_da_categoria = [
            ind for ind in self.__indicacoes 
            if ind.categoria.id == categoria_id
        ]
        if not indicacoes_da_categoria:
            return []

        contagem = Counter(
            (ind.item_indicado_id, ind.tipo_item_indicado) 
            for ind in indicacoes_da_categoria
        )
        if not contagem:
            return []
            
        mapa_info = {
            (ind.item_indicado_id, ind.tipo_item_indicado): 
            ind.obter_detalhes_item_indicado() 
            for ind in indicacoes_da_categoria
        }

        ordenados = contagem.most_common()
        if len(ordenados) <= limite:
            chaves_finalistas = [item[0] for item in ordenados]
        else:
            contagem_corte = ordenados[limite - 1][1]
            chaves_finalistas = [
                item[0] for item in ordenados if item[1] >= contagem_corte
            ]
            
        return [
            {
                "id_original_indicado": chave[0],
                "nome_display": mapa_info.get(chave, "Nome Indisponível"),
                "tipo_original_indicado": chave[1]
            } for chave in chaves_finalistas
        ]