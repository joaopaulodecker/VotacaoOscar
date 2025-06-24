from collections import Counter
from Entidades.Ator import Ator
from Entidades.Diretor import Diretor
from Entidades.Categoria import Categoria
from Entidades.Filme import Filme
from Entidades.IndAtor import IndAtor
from Entidades.IndDiretor import IndDiretor
from Entidades.IndFilme import IndFilme
from Excecoes.OpcaoInvalida import OpcaoInvalida
from Limites.TelaIndicacao import TelaIndicacao
from DAOs.indicacao_dao import IndicacaoDAO

class ControladorIndicacao:

    def __init__(self, controlador_sistema, controlador_membros,
                 controlador_categorias, controlador_filmes):
        self.__controlador_sistema = controlador_sistema
        self.__tela_indicacao = TelaIndicacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__controlador_filmes = controlador_filmes
        self.__dao = IndicacaoDAO()

    def _gerar_proximo_id_indicacao(self):
        todas_indicacoes = self.__dao.get_all()
        if not todas_indicacoes:
            return 1
        
        maior_id = max(indicacao.id_indicacao for indicacao in todas_indicacoes)
        return maior_id + 1

    def _preparar_dados_para_selecao(self, lista_entidades: list) -> list[dict]:
        dados_para_tela = []
        for item in lista_entidades:
            if isinstance(item, Categoria):
                info = f"ID: {item.id} - Nome: {item.nome}"
                dados_para_tela.append({"id": item.id, "info": info})
            elif isinstance(item, Filme):
                info = (f"ID: {item.id_filme} - Título: {item.titulo} "
                        f"({item.ano})")
                dados_para_tela.append({"id": item.id_filme, "info": info})
            elif isinstance(item, (Ator, Diretor)):
                info = item.get_info_str()
                dados_para_tela.append({"id": item.id, "info": info})
        return dados_para_tela

    def abrir_menu_indicacoes(self):
        while True:
            try:
                opcao = self.__tela_indicacao.mostra_opcoes_indicacao()
                if opcao == 1:
                    self.iniciar_indicacao()
                elif opcao == 2:
                    self.alterar_indicacao()
                elif opcao == 3:
                    self.excluir_indicacao()
                elif opcao == 4:
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
        if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_INDICACOES_ABERTAS:
            self.__tela_indicacao.mostra_mensagem("\n❌ O período de indicações já foi encerrado.")
            self.__tela_indicacao.espera_input()
            return

        self.__tela_indicacao.mostra_mensagem("\n--- Nova Indicação ---")

        categorias = self.__controlador_categorias.entidades 
        if not categorias:
            self.__tela_indicacao.mostra_mensagem("❌ Nenhuma categoria cadastrada para indicação.")
            self.__tela_indicacao.espera_input()
            return
        categorias_dados = self._preparar_dados_para_selecao(categorias)
        categoria_escolhida_dados = self.__tela_indicacao.seleciona_categoria(categorias_dados)
        if not categoria_escolhida_dados:
            self.__tela_indicacao.espera_input()
            return
        categoria_obj = self.__controlador_categorias.buscar_categoria_por_id(categoria_escolhida_dados.get('id'))

        tipo_item = categoria_obj.tipo_indicacao
        item_indicado_obj = self._selecionar_item_para_indicacao(tipo_item, categoria_obj.nome)
        if not item_indicado_obj:
            self.__tela_indicacao.espera_input()
            return

        id_nova_indicacao = self._gerar_proximo_id_indicacao()
        nova_indicacao = self._criar_objeto_indicacao(id_nova_indicacao, categoria_obj, item_indicado_obj)

        if nova_indicacao:
            self.__dao.add(nova_indicacao)
            nome_item = item_indicado_obj.titulo if isinstance(item_indicado_obj, Filme) else item_indicado_obj.nome
            self.__tela_indicacao.mostra_mensagem(
                f"\n✅ Indicação de '{nome_item}' para '{categoria_obj.nome}' registrada com sucesso!"
            )
        else:
            self.__tela_indicacao.mostra_mensagem("❌ Falha ao criar o objeto de indicação.")
        self.__tela_indicacao.espera_input()

    def _selecionar_item_para_indicacao(self, tipo_item: str, nome_categoria: str = ""):
        if tipo_item == "filme":
            filmes = self.__controlador_filmes.filmes
            if not filmes:
                self.__tela_indicacao.mostra_mensagem("❌ Nenhum filme cadastrado.")
                return None
            dados_tela = self._preparar_dados_para_selecao(filmes)
            id_escolhido = self.__tela_indicacao.seleciona_filme(dados_tela)
            return self.__controlador_filmes.buscar_filme_por_id(id_escolhido) if id_escolhido else None

        elif tipo_item == "ator":
            genero_alvo = "Atriz" if "atriz" in nome_categoria.lower() else "Ator"
            membros_aptos = self.__controlador_membros.buscar_por_funcao_e_genero("ator", genero_alvo)
            if not membros_aptos:
                self.__tela_indicacao.mostra_mensagem(f"❌ Nenhum(a) {genero_alvo} cadastrado(a).")
                return None
            dados_tela = self._preparar_dados_para_selecao(membros_aptos)
            id_membro = self.__tela_indicacao.seleciona_membro_por_funcao(dados_tela, genero_alvo)
            return self.__controlador_membros.buscar_por_id(id_membro)

        elif tipo_item == "diretor":
            membros_aptos = self.__controlador_membros.buscar_por_funcao_e_genero("diretor")
            if not membros_aptos:
                self.__tela_indicacao.mostra_mensagem(f"❌ Nenhum(a) {tipo_item.capitalize()} cadastrado.")
                return None
            dados_tela = self._preparar_dados_para_selecao(membros_aptos)
            id_membro = self.__tela_indicacao.seleciona_membro_por_funcao(dados_tela, "Diretor")
            return self.__controlador_membros.buscar_por_id(id_membro)

        return None

    def _criar_objeto_indicacao(self, id_ind, cat_obj, item_obj):
        if isinstance(item_obj, Filme):
            return IndFilme(id_indicacao=id_ind, categoria=cat_obj, filme_indicado=item_obj)
        elif isinstance(item_obj, Ator):
            return IndAtor(id_indicacao=id_ind, categoria=cat_obj, ator_indicado=item_obj)
        elif isinstance(item_obj, Diretor):
            return IndDiretor(id_indicacao=id_ind, categoria=cat_obj, diretor_indicado=item_obj)
        return None

    def excluir_indicacao(self, alterando: bool = False):
        if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_INDICACOES_ABERTAS:
            self.__tela_indicacao.mostra_mensagem("\n❌ Não é possível excluir indicações após o início da votação.")
            self.__tela_indicacao.espera_input()
            return

        self.listar_todas_indicacoes()
        if not self.__dao.get_all():
            return

        prompt = "Digite o ID da indicação a excluir: " if not alterando else "Digite o ID da indicação a substituir: "
        id_alvo = self.__tela_indicacao.pega_id_indicacao(prompt)

        if id_alvo is None:
            self.__tela_indicacao.mostra_mensagem("ℹ️ Operação cancelada.")
            self.__tela_indicacao.espera_input()
            return

        indicacao_alvo = self.buscar_indicacao_por_id(id_alvo)

        if indicacao_alvo:
            info = indicacao_alvo.obter_detalhes_item_indicado()
            if self.__tela_indicacao.confirma_exclusao(info):
                self.__dao.remove(indicacao_alvo.id_indicacao)
                self.__tela_indicacao.mostra_mensagem("🗑️ Indicação removida com sucesso!")
            else:
                self.__tela_indicacao.mostra_mensagem("ℹ️ Operação cancelada.")
        else:
            self.__tela_indicacao.mostra_mensagem(f"❌ Indicação com ID {id_alvo} não encontrada.")
        self.__tela_indicacao.espera_input()

    def alterar_indicacao(self):
        self.__tela_indicacao.mostra_mensagem("\n--- Alterar Indicação ---")
        self.excluir_indicacao(alterando=True)
        self.__tela_indicacao.mostra_mensagem("\nAgora, cadastre a nova indicação:")
        self.iniciar_indicacao()

    def buscar_indicacao_por_id(self, id_busca: int):
        return self.__dao.get(id_busca)

    def listar_todas_indicacoes(self):
        todas_indicacoes = self.__dao.get_all()
        if not todas_indicacoes:
            self.__tela_indicacao.mostra_mensagem("\n📭 Nenhuma indicação registrada.")
            return

        dados_para_tela = []
        for ind in todas_indicacoes:
            detalhes = ind.obter_detalhes_item_indicado()
            info = (f"ID: {ind.id_indicacao} | Categoria: {ind.categoria.nome} | "
                    f"Indicado: {detalhes}")
            dados_para_tela.append(info)

        self.__tela_indicacao.mostra_lista_geral_indicacoes(dados_para_tela)

    def listar_indicacoes_por_categoria(self):
        self.__tela_indicacao.mostra_mensagem("\n--- Indicações por Categoria ---")
        categorias = self.__controlador_categorias.entidades
        if not categorias:
            self.__tela_indicacao.mostra_mensagem("❌ Nenhuma categoria cadastrada.")
            self.__tela_indicacao.espera_input()
            return

        categorias_dados = self._preparar_dados_para_selecao(categorias)
        cat_escolhida_dados = self.__tela_indicacao.seleciona_categoria(categorias_dados)
        if not cat_escolhida_dados:
            self.__tela_indicacao.espera_input()
            return

        id_cat_escolhida = cat_escolhida_dados.get('id')
        
        indicacoes_filtradas = [
            ind for ind in self.__dao.get_all()
            if ind.categoria.id == id_cat_escolhida
        ]

        dados_para_tela = [
            ind.obter_detalhes_item_indicado() for ind in indicacoes_filtradas
        ]
        nome_categoria = next((cat['info'] for cat in categorias_dados if cat['id'] == id_cat_escolhida), 'Categoria')

        self.__tela_indicacao.mostra_lista_indicacoes(nome_categoria, dados_para_tela)
        self.__tela_indicacao.espera_input()

    def get_finalistas_por_categoria(self, categoria_id: int, limite: int = 5):
        indicacoes_da_categoria = [
            ind for ind in self.__dao.get_all()
            if ind.categoria.id == categoria_id
        ]
        if not indicacoes_da_categoria:
            return []

        contagem = Counter((ind.item_indicado_id, ind.tipo_item_indicado) for ind in indicacoes_da_categoria)
        if not contagem:
            return []

        mapa_info = {(ind.item_indicado_id, ind.tipo_item_indicado): ind.obter_detalhes_item_indicado() for ind in indicacoes_da_categoria}
        ordenados = contagem.most_common()

        if len(ordenados) <= limite:
            chaves_finalistas = [item[0] for item in ordenados]
        else:
            contagem_corte = ordenados[limite - 1][1]
            chaves_finalistas = [item[0] for item in ordenados if item[1] >= contagem_corte]

        return [{"id_original_indicado": chave[0], "nome_display": mapa_info.get(chave, "Nome Indisponível"), "tipo_original_indicado": chave[1]} for chave in chaves_finalistas]