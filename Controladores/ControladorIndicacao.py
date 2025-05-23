from Limites.TelaIndicacao import TelaIndicacao
from Entidades.IndicacaoAbstract import IndicacaoAbstract
from Entidades.IndFilme import IndFilme
from Entidades.IndAtor import IndAtor
from Entidades.IndDiretor import IndDiretor
from Entidades.Categoria import Categoria
from Entidades.Filme import Filme

class ControladorIndicacao:
    def __init__(self, controlador_membros, controlador_categorias, controlador_filmes):
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

    def iniciar_indicacao(self):
        print("\n--- Nova Indicação ---")

        membros = self.__controlador_membros.buscar_por_funcao("jurado")

        if not membros:
            print("❌ Nenhum membro da academia cadastrado para fazer indicações.")
            input("🔁 Pressione Enter para continuar...")
            return

        membro_selecionado_dict = self.__tela_indicacao.seleciona_membro(membros)
        if not membro_selecionado_dict:
            print("ℹ️ Seleção de membro cancelada.")
            input("🔁 Pressione Enter para continuar...")
            return
        membro_id = membro_selecionado_dict.get("id")

        categorias_objs = self.__controlador_categorias.entidades
        if not categorias_objs:
            print("❌ Nenhuma categoria cadastrada para indicação.")
            input("🔁 Pressione Enter para continuar...")
            return

        categoria_obj_selecionada = self.__tela_indicacao.seleciona_categoria(categorias_objs)
        if not categoria_obj_selecionada or not isinstance(categoria_obj_selecionada, Categoria):
            print("ℹ️ Seleção de categoria cancelada ou inválida.")
            input("🔁 Pressione Enter para continuar...")
            return

        tipo_permitido = categoria_obj_selecionada.tipo_indicacao

        print(f"ℹ️ Esta categoria aceita indicações do tipo: {tipo_permitido.capitalize()}")

        tipo_item_indicado = self.__tela_indicacao.pega_tipo_item_indicado(categoria_obj_selecionada.nome)
        if not tipo_item_indicado:
            print("ℹ️ Tipo de indicação não definido ou cancelado.")
            input("🔁 Pressione Enter para continuar...")
            return

        tipo_permitido = categoria_obj_selecionada.tipo_indicacao.lower()
        if tipo_item_indicado.lower() != tipo_permitido:
            print(f"❌ Tipo de indicação inválido para esta categoria!")
            print(f"➡️ Esta categoria aceita apenas indicações do tipo: '{tipo_permitido.capitalize()}'")
            input("🔁 Pressione Enter para tentar novamente...")
            return

        item_indicado_obj = None
        item_indicado_id = None
        nome_display_item_indicado = "Item Desconhecido"

        if tipo_item_indicado == "filme":
            filmes_objs = self.__controlador_filmes.filmes
            if not filmes_objs:
                print("❌ Nenhum filme cadastrado para ser indicado.")
                input("🔁 Pressione Enter para continuar...")
                return
            item_indicado_obj = self.__tela_indicacao.seleciona_filme(filmes_objs)
            if not item_indicado_obj or not isinstance(item_indicado_obj, Filme):
                print("ℹ️ Seleção de filme cancelada ou inválida.")
                input("🔁 Pressione Enter para continuar...")
                return
            item_indicado_id = item_indicado_obj.id_filme
            nome_display_item_indicado = item_indicado_obj.titulo
        elif tipo_item_indicado == "ator":
            atores_dicts = self.__controlador_membros.buscar_por_funcao("ator")
            if not atores_dicts:
                print("❌ Nenhum ator cadastrado para ser indicado.")
                input("🔁 Pressione Enter para continuar...")
                return
            ator_dict_selecionado = self.__tela_indicacao.seleciona_membro_por_funcao(atores_dicts, "Ator")
            if not ator_dict_selecionado:
                print("ℹ️ Seleção de ator cancelada ou inválida.")
                input("🔁 Pressione Enter para continuar...")
                return
            item_indicado_id = ator_dict_selecionado.get("id")
            nome_display_item_indicado = ator_dict_selecionado.get("nome")
            item_indicado_obj = ator_dict_selecionado
        elif tipo_item_indicado == "diretor":
            diretores_dicts = self.__controlador_membros.buscar_por_funcao("diretor")
            if not diretores_dicts:
                print("❌ Nenhum diretor cadastrado para ser indicado.")
                input("🔁 Pressione Enter para continuar...")
                return
            diretor_dict_selecionado = self.__tela_indicacao.seleciona_membro_por_funcao(diretores_dicts, "Diretor")
            if not diretor_dict_selecionado:
                print("ℹ️ Seleção de diretor cancelada ou inválida.")
                input("🔁 Pressione Enter para continuar...")
                return
            item_indicado_id = diretor_dict_selecionado.get("id")
            nome_display_item_indicado = diretor_dict_selecionado.get("nome")
            item_indicado_obj = diretor_dict_selecionado
        else:
            print(f"❌ Tipo de indicação '{tipo_item_indicado}' não suportado.")
            input("🔁 Pressione Enter para continuar...")
            return

        if item_indicado_id is None:
            print("❌ Não foi possível identificar o item a ser indicado.")
            input("🔁 Pressione Enter para continuar...")
            return

        for indicacao_existente in self.__indicacoes:
            if (indicacao_existente.membro_id == membro_id and
                indicacao_existente.categoria.id == categoria_obj_selecionada.id and
                indicacao_existente.item_indicado_id == item_indicado_id and
                indicacao_existente.tipo_item_indicado == tipo_item_indicado):
                print(f"⚠️ O membro ID {membro_id} já indicou '{nome_display_item_indicado}' para a categoria '{categoria_obj_selecionada.nome}'.")
                input("🔁 Pressione Enter para continuar...")
                return

        id_nova_indicacao = self._gerar_proximo_id_indicacao()
        nova_indicacao_obj = None

        if tipo_item_indicado == "filme" and isinstance(item_indicado_obj, Filme):
            nova_indicacao_obj = IndFilme(id_nova_indicacao, membro_id, categoria_obj_selecionada, item_indicado_obj)
        elif tipo_item_indicado == "ator" and isinstance(item_indicado_obj, dict):
            nova_indicacao_obj = IndAtor(id_nova_indicacao, membro_id, categoria_obj_selecionada, item_indicado_obj)
        elif tipo_item_indicado == "diretor" and isinstance(item_indicado_obj, dict):
            nova_indicacao_obj = IndDiretor(id_nova_indicacao, membro_id, categoria_obj_selecionada, item_indicado_obj)
        
        if not nova_indicacao_obj:
            print("❌ Falha ao criar o objeto de indicação. Verifique os tipos e dados.")
            input("🔁 Pressione Enter para continuar...")
            return

        self.__indicacoes.append(nova_indicacao_obj)
        categoria_obj_selecionada.adicionar_indicacao(nova_indicacao_obj)

        print(f"✅ Indicação de '{nome_display_item_indicado}' para '{categoria_obj_selecionada.nome}' registrada com sucesso!")
        input("🔁 Pressione Enter para continuar...")

    def listar_indicacoes_por_categoria(self):
        print("\n--- Indicações por Categoria ---")
        categorias_objs = self.__controlador_categorias.entidades
        if not categorias_objs:
            print("❌ Nenhuma categoria cadastrada.")
            input("🔁 Pressione Enter para continuar...")
            return

        categoria_obj_selecionada = self.__tela_indicacao.seleciona_categoria(categorias_objs)
        if not categoria_obj_selecionada or not isinstance(categoria_obj_selecionada, Categoria):
            print("ℹ️ Seleção de categoria cancelada ou inválida.")
            input("🔁 Pressione Enter para continuar...")
            return
        
        print(f"\nIndicados para: {categoria_obj_selecionada.nome} (ID: {categoria_obj_selecionada.id})")
        
        indicacoes_na_categoria = categoria_obj_selecionada.indicacoes

        if not indicacoes_na_categoria:
            print("  Nenhuma indicação para esta categoria ainda.")
        else:
            for indicacao in indicacoes_na_categoria:
                nome_item_display = "Item não identificado"
                if isinstance(indicacao, IndFilme):
                    if indicacao.item_indicado and indicacao.item_indicado.titulo:
                        nome_item_display = indicacao.item_indicado.titulo
                    elif indicacao.item_indicado and indicacao.item_indicado.id:
                         nome_item_display = f"Filme ID {indicacao.item_indicado.id}"
                elif isinstance(indicacao, IndAtor):
                    if indicacao.item_indicado and indicacao.item_indicado.get("nome"):
                        nome_item_display = indicacao.item_indicado.get("nome")
                    elif indicacao.item_indicado and indicacao.item_indicado.get("id"):
                        nome_item_display = f"Ator ID {indicacao.item_indicado.get('id')}"
                elif isinstance(indicacao, IndDiretor):
                    if indicacao.item_indicado and indicacao.item_indicado.get("nome"):
                        nome_item_display = indicacao.item_indicado.get("nome")
                    elif indicacao.item_indicado and indicacao.item_indicado.get("id"):
                        nome_item_display = f"Diretor ID {indicacao.item_indicado.get('id')}"
                
                print(f"  - {nome_item_display} (Indicado pelo membro ID: {indicacao.membro_id})")
        
        input("🔁 Pressione Enter para continuar...")

    def abrir_menu_indicacoes(self):
        while True:
            opcao = self.__tela_indicacao.mostra_opcoes_indicacao()
            if opcao == 1:
                self.iniciar_indicacao()
            elif opcao == 2:
                self.listar_indicacoes_por_categoria()
            elif opcao == 0:
                break