from collections import Counter
from Entidades.Categoria import Categoria
from Entidades.Voto import Voto
from Excecoes.OpcaoInvalida import OpcaoInvalida
from Limites.TelaVotacao import TelaVotacao

class ControladorVotacao:
    def __init__(self, controlador_sistema, controlador_membros, controlador_categorias,
                 controlador_filmes, controlador_indicacao):
        self.__controlador_sistema = controlador_sistema
        self.__tela_votacao = TelaVotacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__controlador_filmes = controlador_filmes
        self.__controlador_indicacao = controlador_indicacao
        self.__votos_registrados = []
        self.__proximo_id_voto = 1

    def _gerar_proximo_id_voto(self):
        id_atual = self.__proximo_id_voto
        self.__proximo_id_voto += 1
        return id_atual

    def _preparar_dados_para_selecao(self, lista_entidades: list) -> list[dict]:
        """Converte listas de entidades ou dicionários em um formato para a tela."""
        dados_para_tela = []
        for item in lista_entidades:
            if isinstance(item, Categoria):
                dados_para_tela.append({"id": item.id, "info": f"ID: {item.id} - Nome: {item.nome}"})
            elif isinstance(item, dict):
                dados_para_tela.append({"id": item.get('id'), "info": f"ID: {item.get('id')} - Nome: {item.get('nome')}"})
        return dados_para_tela

    def abrir_menu_votacao(self):
        """Exibe o menu de votação e processa a escolha do usuário."""
        while True:
            try:
                opcao = self.__tela_votacao.mostra_opcoes_votacao()
                if opcao == 1:
                    self.iniciar_votacao()
                elif opcao == 2:
                    self.mostrar_resultados()
                elif opcao == 0:
                    break
            except OpcaoInvalida as e:
                self.__tela_votacao.mostra_mensagem(f"❌ {e}")
                self.__tela_votacao.espera_input()
            except Exception as e:
                self.__tela_votacao.mostra_mensagem(f"❌ Erro inesperado: {e}")
                self.__tela_votacao.espera_input()

    def iniciar_votacao(self):
        """Conduz o processo de registro de um novo voto."""
        if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_VOTACAO_ABERTA:
            msg = ("\n❌ A votação não está disponível nesta fase da premiação."
                   if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_INDICACOES_ABERTAS
                   else "\n❌ A votação ainda não pode começar. O período de indicações precisa ser encerrado primeiro.")
            self.__tela_votacao.mostra_mensagem(msg)
            self.__tela_votacao.espera_input()
            return
        
        self.__tela_votacao.mostra_mensagem("\n--- Iniciar Votação ---")

        membros = self.__controlador_membros.entidades
        if not membros:
            self.__tela_votacao.mostra_mensagem("❌ Nenhum membro da academia cadastrado para votar.")
            self.__tela_votacao.espera_input()
            return

        membros_dados = self._preparar_dados_para_selecao(membros)
        membro_votante_dict = self.__tela_votacao.seleciona_membro_votante(membros_dados)
        if not membro_votante_dict:
            self.__tela_votacao.espera_input()
            return
        membro_id_votante = membro_votante_dict.get("id")
        
        funcao_votante = self.__controlador_membros.buscar_por_id(membro_id_votante).get('funcao', '').lower()

        categorias = self.__controlador_categorias.entidades
        if not categorias:
            self.__tela_votacao.mostra_mensagem("❌ Nenhuma categoria cadastrada para votação.")
            self.__tela_votacao.espera_input()
            return

        categorias_dados = self._preparar_dados_para_selecao(categorias)
        categoria_escolhida_dados = self.__tela_votacao.seleciona_categoria_para_voto(categorias_dados)
        if not categoria_escolhida_dados:
            self.__tela_votacao.espera_input()
            return
        categoria_obj = self.__controlador_categorias.buscar_categoria_por_id(categoria_escolhida_dados.get('id'))

        if categoria_obj.tipo_indicacao == "diretor" and funcao_votante != "diretor":
            self.__tela_votacao.mostra_mensagem(
                f"❌ Apenas membros 'Diretores' podem votar na categoria '{categoria_obj.nome}'."
            )
            self.__tela_votacao.espera_input()
            return

        for voto in self.__votos_registrados:
            if voto.membro_id == membro_id_votante and voto.categoria.id == categoria_obj.id:
                self.__tela_votacao.mostra_mensagem(
                    f"⚠️ O membro ID {membro_id_votante} já votou na categoria '{categoria_obj.nome}'."
                )
                self.__tela_votacao.espera_input()
                return
        
        finalistas = self.__controlador_indicacao.get_finalistas_por_categoria(categoria_obj.id, limite=5)
        if not finalistas:
            self.__tela_votacao.mostra_mensagem(
                f"❌ Não há finalistas para a categoria '{categoria_obj.nome}'."
            )
            self.__tela_votacao.espera_input()
            return

        indicado_escolhido = self.__tela_votacao.seleciona_indicado_para_voto(finalistas, categoria_obj.nome)
        if not indicado_escolhido:
            self.__tela_votacao.espera_input()
            return
            
        id_item_votado = indicado_escolhido.get("id_original_indicado")
        tipo_item_votado = indicado_escolhido.get("tipo_original_indicado")

        novo_voto = Voto(id_voto=self._gerar_proximo_id_voto(),
                          membro_id=membro_id_votante,
                          categoria=categoria_obj,
                          item_indicado_id=id_item_votado,
                          tipo_item_indicado=tipo_item_votado)
        self.__votos_registrados.append(novo_voto)
        if hasattr(categoria_obj, 'adicionar_voto'):
            categoria_obj.adicionar_voto(novo_voto)

        self.__tela_votacao.mostra_mensagem(
            f"✅ Voto para '{indicado_escolhido.get('nome_display')}' registrado com sucesso!"
        )
        self.__tela_votacao.espera_input()

    def mostrar_resultados(self):
        """Calcula e delega a exibição dos resultados da votação para a tela."""
        if not self.__votos_registrados:
            self.__tela_votacao.mostra_mensagem("📭 Nenhum voto registrado ainda.")
            self.__tela_votacao.espera_input()
            return

        resultados = {}
        for voto in self.__votos_registrados:
            cat_id = voto.categoria.id
            if cat_id not in resultados:
                resultados[cat_id] = {
                    "nome_categoria": voto.categoria.nome,
                    "contagem_votos": Counter()
                }
            
            nome_item = "Item Desconhecido"
            if voto.tipo_item_indicado == "filme":
                filme = self.__controlador_filmes.buscar_filme_por_id(voto.item_indicado_id)
                if filme: nome_item = filme.titulo
            elif voto.tipo_item_indicado in ["ator", "diretor"]:
                membro = self.__controlador_membros.buscar_por_id(voto.item_indicado_id)
                if membro: nome_item = membro.get("nome")
            
            resultados[cat_id]["contagem_votos"][f"{nome_item} (ID: {voto.item_indicado_id})"] += 1

        resultados_formatados = {
            dados["nome_categoria"]: sorted(dados["contagem_votos"].items(),
                                            key=lambda item: item[1],
                                            reverse=True)
            for _, dados in resultados.items()
        }
        
        self.__tela_votacao.mostra_resultados(resultados_formatados)
        self.__tela_votacao.espera_input()
        