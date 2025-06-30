from collections import Counter
from Entidades.Voto import Voto
from Limites.TelaVotacao import TelaVotacao
from DAOs.VotoDao import VotoDAO


class ControladorVotacao:
    """Controlador principal para as regras de negócio de Votação."""

    def __init__(self, controlador_sistema, controlador_membros, controlador_categorias,
                 controlador_filmes, controlador_indicacao):
        self.__controlador_sistema = controlador_sistema
        self.__tela_votacao = TelaVotacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__controlador_filmes = controlador_filmes
        self.__controlador_indicacao = controlador_indicacao
        self.__dao = VotoDAO()

    def abre_tela(self):
        """Abre a tela principal e gerencia o loop de eventos."""
        self.__tela_votacao.init_components()
        while True:
            event, values = self.__tela_votacao.open()
            if event in (None, '-VOLTAR-'):
                break
            if event == '-REGISTRAR-':
                self.iniciar_votacao_gui()
            elif event == '-RESULTADOS-':
                self.mostrar_resultados_gui()
        self.__tela_votacao.close()

    def iniciar_votacao_gui(self):
        """Orquestra o fluxo completo de registro de um novo voto."""
        if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_VOTACAO_ABERTA:
            self.__tela_votacao.show_message("Aviso", "A votação não está disponível nesta fase da premiação.")
            return

        # --- PASSO 1: Selecionar Votante e Categoria ---
        membros = self.__controlador_membros.membros
        categorias = self.__controlador_categorias.categorias
        if not membros or not categorias:
            self.__tela_votacao.show_message("Aviso", "É preciso ter Membros e Categorias cadastrados.")
            return

        mapa_membros = {f"ID {m.id}: {m.nome}": m for m in membros}
        mapa_categorias = {f"ID {cat.id}: {cat.nome}": cat for cat in categorias}

        dados_passo1 = self.__tela_votacao.pega_dados_votacao_passo1(mapa_membros, mapa_categorias)
        if not dados_passo1 or not dados_passo1.get('-MEMBRO-') or not dados_passo1.get('-CATEGORIA-'):
            return

        # O Controlador processa os dados brutos da tela
        membro_obj = mapa_membros[dados_passo1['-MEMBRO-'][0]]
        categoria_obj = mapa_categorias[dados_passo1['-CATEGORIA-'][0]]

        # O Controlador faz a validação da regra de negócio
        for voto in self.__dao.get_all():
            if voto.membro_id == membro_obj.id and voto.categoria.id == categoria_obj.id:
                msg = f"O membro '{membro_obj.nome}' já votou na categoria '{categoria_obj.nome}'."
                self.__tela_votacao.show_message("Erro de Votação", msg)
                return

        # --- PASSO 2: Selecionar o Finalista ---
        finalistas = self.__controlador_indicacao.get_finalistas_por_categoria(categoria_obj.id)
        if not finalistas:
            self.__tela_votacao.show_message("Aviso", f"Não há finalistas para a categoria '{categoria_obj.nome}'.")
            return

        mapa_finalistas = {f['nome_display']: f for f in finalistas}
        dados_passo2 = self.__tela_votacao.pega_dados_votacao_passo2(mapa_finalistas, categoria_obj.nome)
        if not dados_passo2 or not dados_passo2.get('-FINALISTA-'):
            return

        # Controlador processa a seleção final e salva o objeto
        finalista_selecionado = mapa_finalistas[dados_passo2['-FINALISTA-'][0]]

        novo_id = self.__dao.get_next_id()
        novo_voto = Voto(id_voto=novo_id,
                         membro_id=membro_obj.id,
                         categoria=categoria_obj,
                         item_indicado_id=finalista_selecionado.get("id_original_indicado"),
                         tipo_item_indicado=finalista_selecionado.get("tipo_original_indicado"))

        self.__dao.add(key=novo_id, voto=novo_voto)
        self.__tela_votacao.show_message("Sucesso",
                                         f"Voto para '{finalista_selecionado.get('nome_display')}' registrado!")

    def mostrar_resultados_gui(self):
        """Busca os votos, calcula os resultados e pede para a tela exibir."""
        todos_os_votos = self.__dao.get_all()
        if not todos_os_votos:
            self.__tela_votacao.mostra_resultados(None)
            return

        # O Controlador faz toda a lógica de contagem e formatação
        resultados = {}
        for voto in todos_os_votos:
            cat_id = voto.categoria.id
            if cat_id not in resultados:
                resultados[cat_id] = {"nome_categoria": voto.categoria.nome, "contagem_votos": Counter()}

            nome_item = "Item Desconhecido"
            if voto.tipo_item_indicado == "filme":
                filme = self.__controlador_filmes.buscar_filme_por_id(voto.item_indicado_id)
                if filme: nome_item = filme.titulo
            elif voto.tipo_item_indicado in ["ator", "diretor"]:
                membro = self.__controlador_membros.buscar_por_id(voto.item_indicado_id)
                if membro: nome_item = membro.nome

            resultados[cat_id]["contagem_votos"][nome_item] += 1

        # Formata o texto final para a tela "burra" apenas exibir
        texto_final = ""
        for dados in resultados.values():
            texto_final += f"🏆 Categoria: {dados['nome_categoria']}\n" + "-" * 40 + "\n"
            votos_ordenados = sorted(dados["contagem_votos"].items(), key=lambda item: item[1], reverse=True)
            for item_nome, contagem in votos_ordenados:
                texto_final += f"   - {item_nome}: {contagem} voto(s)\n"
            texto_final += "\n"

        self.__tela_votacao.mostra_resultados(texto_final)