from Limites.TelaIndicacao import TelaIndicacao
from Excecoes.OpcaoInvalida import OpcaoInvalida
from Entidades.IndFilme import IndFilme
from Entidades.IndAtor import IndAtor 
from Entidades.IndDiretor import IndDiretor 
from Entidades.Categoria import Categoria
from Entidades.Filme import Filme
from collections import Counter

class ControladorIndicacao:
    """ Gerencia todo o processo de indicações no sistema do Oscar.

    Esta classe é responsável por:
    - Permitir que membros da academia registrem novas indicações para filmes,
      atores ou diretores em categorias específicas.
    - Validar se as indicações são permitidas (fase correta da premiação,
      compatibilidade entre item e categoria).
    - Armazenar e listar as indicações realizadas.
    - Determinar os finalistas para cada categoria com base no número de indicações recebidas.
"""
    def __init__(self, controlador_sistema, controlador_membros, controlador_categorias, controlador_filmes):
        self.__controlador_sistema = controlador_sistema 
        self.__tela_indicacao = TelaIndicacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__controlador_filmes = controlador_filmes
        self.__indicacoes = []
        self.__proximo_id_indicacao = 1

    def _gerar_proximo_id_indicacao(self):
        """Gera um novo ID incremental para uma indicação.
        Retorna:
            int: O próximo ID disponível.
        """
        id_atual = self.__proximo_id_indicacao
        self.__proximo_id_indicacao += 1
        return id_atual

    def iniciar_indicacao(self):
        """
            Conduz o processo de registro de uma nova indicação.
           Verifica a fase da premiação, coleta dados do membro, categoria e item a ser indicado
           através da tela. Valida a compatibilidade e, se tudo estiver correto,
           cria e armazena o objeto de indicação apropriado (IndFilme, IndAtor ou IndDiretor).
               """
        # Verifica se o sistema está na fase correta para aceitar indicações.
        if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_INDICACOES_ABERTAS:
            print("\n❌ O período de indicações já foi encerrado ou a premiação está em outra fase.")
            input("🔁 Pressione Enter para continuar...")
            return

        print("\n--- Nova Indicação ---")

        membros = self.__controlador_membros.entidades 

        if not membros:
            print("❌ Nenhum membro da academia cadastrado para fazer indicações.")
            input("🔁 Pressione Enter para continuar...")
            return

        #### Seleção do membro que está fazendo a indicação.
        membro_selecionado_dict = self.__tela_indicacao.seleciona_membro(membros)
        if not membro_selecionado_dict:
            print("ℹ️ Seleção de membro cancelada.")
            input("🔁 Pressione Enter para continuar...")
            return
        membro_id = membro_selecionado_dict.get("id")

        ### Seleção da categoria para a qual a indicação será feita.
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

        ### Validação do tipo de item indicado versus o tipo esperado pela categoria.
        tipo_item_permitido_pela_categoria = categoria_obj_selecionada.tipo_indicacao.lower()
        print(f"ℹ️ Esta categoria ('{categoria_obj_selecionada.nome}') aceita indicações do tipo: {tipo_item_permitido_pela_categoria.capitalize()}")

        tipo_item_usuario_quer_indicar = self.__tela_indicacao.pega_tipo_item_indicado(categoria_obj_selecionada.nome)
        
        if not tipo_item_usuario_quer_indicar:
            print("ℹ️ Tipo de indicação não definido ou cancelado.")
            input("🔁 Pressione Enter para continuar...")
            return

        if tipo_item_usuario_quer_indicar.lower() != tipo_item_permitido_pela_categoria:
            print(f"❌ Tipo de indicação '{tipo_item_usuario_quer_indicar.capitalize()}' "
                  f"não é compatível com a categoria '{categoria_obj_selecionada.nome}', "
                  f"que espera '{tipo_item_permitido_pela_categoria.capitalize()}'.")
            input("🔁 Pressione Enter para tentar novamente...")
            return

        item_indicado_obj = None
        item_indicado_id = None
        nome_display_item_indicado = "Item Desconhecido"

        ### Bloco condicional para selecionar o item específico (Filme, Ator, Diretor).
        if tipo_item_permitido_pela_categoria == "filme":
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
        elif tipo_item_permitido_pela_categoria == "ator":
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
        elif tipo_item_permitido_pela_categoria == "diretor":
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
            print(f"❌ Tipo de indicação '{tipo_item_permitido_pela_categoria}' não suportado internamente.")
            input("🔁 Pressione Enter para continuar...")
            return

        if item_indicado_id is None:
            print("❌ Não foi possível identificar o item a ser indicado.")
            input("🔁 Pressione Enter para continuar...")
            return

        ###Verifica se este membro já fez esta indicação específica para esta categoria.
        for indicacao_existente in self.__indicacoes:
            if (indicacao_existente.membro_id == membro_id and
                indicacao_existente.categoria.id == categoria_obj_selecionada.id and
                indicacao_existente.item_indicado_id == item_indicado_id and
                indicacao_existente.tipo_item_indicado == tipo_item_permitido_pela_categoria):
                print(f"⚠️ O membro ID {membro_id} já indicou '{nome_display_item_indicado}' para a categoria '{categoria_obj_selecionada.nome}'.")
                input("🔁 Pressione Enter para continuar...")
                return

        id_nova_indicacao = self._gerar_proximo_id_indicacao()
        nova_indicacao_obj = None

        if tipo_item_permitido_pela_categoria == "filme" and isinstance(item_indicado_obj, Filme):
            nova_indicacao_obj = IndFilme(id_nova_indicacao, membro_id, categoria_obj_selecionada, item_indicado_obj)
        elif tipo_item_permitido_pela_categoria == "ator" and isinstance(item_indicado_obj, dict):
            nova_indicacao_obj = IndAtor(id_nova_indicacao, membro_id, categoria_obj_selecionada, item_indicado_obj)
        elif tipo_item_permitido_pela_categoria == "diretor" and isinstance(item_indicado_obj, dict):
            nova_indicacao_obj = IndDiretor(id_nova_indicacao, membro_id, categoria_obj_selecionada, item_indicado_obj)
        
        if not nova_indicacao_obj:
            print("❌ Falha ao criar o objeto de indicação. Verifique os tipos e dados.")
            input("🔁 Pressione Enter para continuar...")
            return

        self.__indicacoes.append(nova_indicacao_obj)
        if hasattr(categoria_obj_selecionada, 'adicionar_indicacao'):
            categoria_obj_selecionada.adicionar_indicacao(nova_indicacao_obj)

        print(f"✅ Indicação de '{nome_display_item_indicado}' para '{categoria_obj_selecionada.nome}' registrada com sucesso!")
        input("🔁 Pressione Enter para continuar...")

    def listar_indicacoes_por_categoria(self):
        """
        Permite ao usuário selecionar uma categoria e lista todas as indicações
        registradas para ela.
        """
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
        
        indicacoes_na_categoria = []

        ### Acessa as indicações diretamente do objeto Categoria, se disponível.
        if hasattr(categoria_obj_selecionada, 'indicacoes'):
            indicacoes_na_categoria = categoria_obj_selecionada.indicacoes
        else:
            indicacoes_na_categoria = [ind for ind in self.__indicacoes if ind.categoria.id == categoria_obj_selecionada.id]

        if not indicacoes_na_categoria:
            print("   Nenhuma indicação para esta categoria ainda.")
        else:
            for indicacao in indicacoes_na_categoria:
                nome_item_display = "Item não identificado"
                if hasattr(indicacao, 'obter_detalhes_item_indicado'):
                    nome_item_display = indicacao.obter_detalhes_item_indicado()
                elif isinstance(indicacao, IndFilme): 
                    if indicacao.item_indicado: nome_item_display = indicacao.item_indicado.titulo
                
                print(f"   - {nome_item_display} (Indicado pelo membro ID: {indicacao.membro_id})")
        
        input("🔁 Pressione Enter para continuar...")

    def get_finalistas_por_categoria(self, categoria_id: int, limite: int = 5) -> list[dict]:
        """
           Determina os finalistas para uma dada categoria com base no número de indicações.

           Conta as indicações para cada item único (ID e tipo) dentro da categoria.
           Os itens com mais indicações são selecionados como finalistas, respeitando
           um limite e regras de desempate (incluindo todos os empatados na última posição do limite).

           Parâmetros:
               categoria_id (int): O ID da categoria para a qual os finalistas serão determinados.
               limite (int): O número máximo desejado de finalistas. Default é 5.

           Retorna:
               list[dict]: Uma lista de dicionários, onde cada dicionário representa um
                           finalista e contém 'id_original_indicado', 'nome_display',
                           e 'tipo_original_indicado'.
        """

        ### Filtra todas as indicações pertencentes à categoria especificada.
        indicacoes_da_categoria = [
            ind for ind in self.__indicacoes 
            if ind.categoria.id == categoria_id
        ]

        if not indicacoes_da_categoria:
            return []

        ### Usa Counter para contar ocorrências de cada item indicado (por ID e tipo).
        contagem_itens = Counter()
        itens_info_map = {} 

        for ind in indicacoes_da_categoria:
            chave_item = (ind.item_indicado_id, ind.tipo_item_indicado)
            contagem_itens[chave_item] += 1

            ### Armazena informações detalhadas do item para exibição posterior, evitando duplicidade.
            if chave_item not in itens_info_map:
                nome_display = "Item Desconhecido"
                obj_real_indicado = ind.item_indicado 

                if ind.tipo_item_indicado == "filme" and isinstance(obj_real_indicado, Filme):
                    nome_display = obj_real_indicado.titulo
                elif ind.tipo_item_indicado in ["ator", "diretor"] and isinstance(obj_real_indicado, dict):
                    nome_display = obj_real_indicado.get("nome", "Nome Indisponível")
                
                itens_info_map[chave_item] = {
                    "id_original_indicado": ind.item_indicado_id,
                    "nome_display": nome_display,
                    "tipo_original_indicado": ind.tipo_item_indicado
                }
        
        if not contagem_itens:
            return []

        ###Obtém os itens mais indicados, ordenados pela contagem
        todos_itens_ordenados_com_contagem = contagem_itens.most_common()
        
        finalistas_chaves = []

        ### Lógica para selecionar os finalistas, incluindo empates na linha de corte.
        if len(todos_itens_ordenados_com_contagem) <= limite:
            #### Se o número total de itens únicos indicados for menor ou igual ao limite, todos são finalistas.
            for chave, _ in todos_itens_ordenados_com_contagem:
                finalistas_chaves.append(chave)
        else:
            ### Se houver mais itens do que o limite, pega os 'limite' primeiros e verifica empates.
            contagem_de_corte = todos_itens_ordenados_com_contagem[limite - 1][1]
            for chave, contagem_atual in todos_itens_ordenados_com_contagem:
                if contagem_atual >= contagem_de_corte:
                    finalistas_chaves.append(chave)
                else:
                    break 
                
        finalistas = []
        for chave in finalistas_chaves:
            if chave in itens_info_map:
                info_item = itens_info_map[chave]
                finalistas.append(info_item)
            
        return finalistas

    def abrir_menu_indicacoes(self):
        """
        Exibe o menu de indicações e processa a escolha do usuário.

        Permite ao usuário registrar novas indicações ou listar indicações existentes
        até que ele escolha a opção de voltar.
        """
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
                print(f"❌ {e}")
                input("🔁 Pressione Enter para continuar...")
            except Exception as e:
                print(f"❌ Erro inesperado no menu de indicações: {e}")
                input("🔁 Pressione Enter para continuar...")