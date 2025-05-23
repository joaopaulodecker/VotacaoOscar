from Limites.TelaVotacao import TelaVotacao
from Entidades.Voto import Voto
from Entidades.Categoria import Categoria
from Entidades.IndicacaoAbstract import IndicacaoAbstract
from Entidades.IndFilme import IndFilme
from Entidades.IndAtor import IndAtor
from Entidades.IndDiretor import IndDiretor
from collections import Counter

class ControladorVotacao:
    def __init__(self, controlador_membros, controlador_categorias, controlador_filmes, controlador_indicacao):
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

    def iniciar_votacao(self):
        print("\n--- Iniciar Votação ---")

        membros = self.__controlador_membros.entidades
        if not membros:
            print("❌ Nenhum membro da academia cadastrado para votar.")
            input("🔁 Pressione Enter para continuar...")
            return

        membro_votante_dict = self.__tela_votacao.seleciona_membro_votante(membros)
        if not membro_votante_dict:
            print("ℹ️ Seleção de membro cancelada.")
            input("🔁 Pressione Enter para continuar...")
            return
        membro_id_votante = membro_votante_dict.get("id")

        categorias_objs = self.__controlador_categorias.entidades
        if not categorias_objs:
            print("❌ Nenhuma categoria cadastrada para votação.")
            input("🔁 Pressione Enter para continuar...")
            return

        categoria_obj_selecionada = self.__tela_votacao.seleciona_categoria_para_voto(categorias_objs)
        if not categoria_obj_selecionada or not isinstance(categoria_obj_selecionada, Categoria):
            print("ℹ️ Seleção de categoria cancelada ou inválida.")
            input("🔁 Pressione Enter para continuar...")
            return

        for voto_existente in self.__votos_registrados:
            if voto_existente.membro_id == membro_id_votante and voto_existente.categoria.id == categoria_obj_selecionada.id:
                print(f"⚠️ O membro ID {membro_id_votante} já votou na categoria '{categoria_obj_selecionada.nome}'.")
                input("🔁 Pressione Enter para continuar...")
                return
        
        indicacoes_para_categoria = [
            ind for ind in self.__controlador_indicacao._ControladorIndicacao__indicacoes
            if ind.categoria.id == categoria_obj_selecionada.id
        ]

        if not indicacoes_para_categoria:
            print(f"❌ Não há indicados para a categoria '{categoria_obj_selecionada.nome}'.")
            input("🔁 Pressione Enter para continuar...")
            return

        itens_indicados_para_tela = []
        for indicacao_obj in indicacoes_para_categoria:
            item = indicacao_obj.item_indicado 
            tipo_item = indicacao_obj.tipo_item_indicado
            item_id = indicacao_obj.item_indicado_id
            
            nome_display = "Item Desconhecido"
            if tipo_item == "filme" and hasattr(item, 'titulo'):
                nome_display = item.titulo
            elif tipo_item in ["ator", "diretor"] and isinstance(item, dict) and 'nome' in item:
                nome_display = item.get('nome')
            
            itens_indicados_para_tela.append({
                "id_original_indicado": item_id,
                "nome_display": nome_display,
                "tipo_original_indicado": tipo_item,
                "objeto_indicacao_completo": indicacao_obj
            })

        indicado_escolhido_dict_tela = self.__tela_votacao.seleciona_indicado_para_voto(itens_indicados_para_tela, categoria_obj_selecionada.nome)

        if not indicado_escolhido_dict_tela:
            print("ℹ️ Votação cancelada ou nenhum indicado selecionado.")
            input("🔁 Pressione Enter para continuar...")
            return
            
        id_item_votado = indicado_escolhido_dict_tela.get("id_original_indicado")
        tipo_item_votado = indicado_escolhido_dict_tela.get("tipo_original_indicado")

        id_novo_voto = self._gerar_proximo_id_voto()
        novo_voto = Voto(
            id_voto=id_novo_voto,
            membro_id=membro_id_votante,
            categoria=categoria_obj_selecionada,
            item_indicado_id=id_item_votado,
            tipo_item_indicado=tipo_item_votado
        )

        self.__votos_registrados.append(novo_voto)
        if hasattr(categoria_obj_selecionada, 'adicionar_voto'):
            categoria_obj_selecionada.adicionar_voto(novo_voto)

        print(f"✅ Voto para '{indicado_escolhido_dict_tela.get('nome_display')}' na categoria '{categoria_obj_selecionada.nome}' registrado com sucesso!")
        input("🔁 Pressione Enter para continuar...")

    def mostrar_resultados(self):
        print("\n--- Resultados da Votação ---")
        if not self.__votos_registrados:
            print("📭 Nenhum voto registrado ainda.")
            input("🔁 Pressione Enter para continuar...")
            return

        resultados_por_categoria = {}
        for voto_obj in self.__votos_registrados:
            cat_id = voto_obj.categoria.id
            if cat_id not in resultados_por_categoria:
                resultados_por_categoria[cat_id] = {
                    "nome_categoria": voto_obj.categoria.nome,
                    "contagem_votos": Counter()
                }
            nome_item_votado = "Item Desconhecido"
            if voto_obj.tipo_item_indicado == "filme":
                filme = self.__controlador_filmes.buscar_filme_por_id(voto_obj.item_indicado_id)
                if filme:
                    nome_item_votado = filme.titulo
            elif voto_obj.tipo_item_indicado in ["ator", "diretor"]:
                membro = self.__controlador_membros.buscar_por_id(voto_obj.item_indicado_id)
                if membro:
                    nome_item_votado = membro.get("nome", f"ID {voto_obj.item_indicado_id}")
            
            resultados_por_categoria[cat_id]["contagem_votos"][f"{nome_item_votado} (ID: {voto_obj.item_indicado_id})"] += 1

        if not resultados_por_categoria:
            print("Nenhuma contagem de votos para exibir.")
        else:
            for cat_id, dados_cat in resultados_por_categoria.items():
                print(f"\n🏆 Categoria: {dados_cat['nome_categoria']}")
                if not dados_cat["contagem_votos"]:
                    print("  Nenhum voto nesta categoria.")
                    continue
                
                votos_ordenados = sorted(dados_cat["contagem_votos"].items(), key=lambda item: item[1], reverse=True)
                
                for item_nome_id, contagem in votos_ordenados:
                    print(f"  - {item_nome_id}: {contagem} voto(s)")
        
        input("🔁 Pressione Enter para continuar...")

    def abrir_menu_votacao(self):
        while True:
            opcao = self.__tela_votacao.mostra_opcoes_votacao()
            if opcao == 1:
                self.iniciar_votacao()
            elif opcao == 2:
                self.mostrar_resultados()
            elif opcao == 0:
                break