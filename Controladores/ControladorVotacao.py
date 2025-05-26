from Limites.TelaVotacao import TelaVotacao
from Entidades.Voto import Voto
from Entidades.Categoria import Categoria
from Excecoes.OpcaoInvalida import OpcaoInvalida
from collections import Counter


class ControladorVotacao:
    """
       Gerencia o processo de votação e a exibição dos resultados no sistema Oscar.

       Esta classe é responsável por:
       - Permitir que membros da academia registrem seus votos para os finalistas
         de cada categoria.
       - Validar se a votação está permitida (fase correta, membro apto a votar,
         voto único por categoria).
       - Obter os finalistas através do ControladorIndicacao.
       - Armazenar os votos registrados.
       - Calcular e apresentar os resultados da votação, mostrando os mais votados
         por categoria.

       Atributos:
           controlador_sistema (ControladorSistema): Referência ao controlador principal.
           tela_votacao (TelaVotacao): Interface com o usuário para as operações de votação.
           controlador_membros (ControladorCadastro): Acesso aos dados dos membros.
           controlador_categorias (ControladorCategorias): Acesso aos dados das categorias.
           controlador_filmes (ControladorFilmes): Acesso aos dados dos filmes.
           controlador_indicacao (ControladorIndicacao): Acesso aos dados de indicações e finalistas.
           votos_registrados (list): Lista que armazena todos os objetos de Voto.
           proximo_id_voto (int): Contador para gerar IDs únicos para novos votos.
       """
    def __init__(self, controlador_sistema, controlador_membros, controlador_categorias, controlador_filmes, controlador_indicacao):
        self.__controlador_sistema = controlador_sistema
        self.__tela_votacao = TelaVotacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__controlador_filmes = controlador_filmes
        self.__controlador_indicacao = controlador_indicacao
        self.__votos_registrados = []
        self.__proximo_id_voto = 1

    def _gerar_proximo_id_voto(self):
        """
        Gera um novo ID incremental para um voto.

        Retorna:
            int: O próximo ID disponível para um voto.
        """
        id_atual = self.__proximo_id_voto
        self.__proximo_id_voto += 1
        return id_atual

    def iniciar_votacao(self):
        """
        Conduz o processo de registro de um novo voto de um membro jurado.

        Verifica se a fase de votação está aberta. Solicita a seleção de um
        membro com a função "jurado". Em seguida, coleta a categoria e o indicado
        (dentre os finalistas). Verifica se o jurado já votou naquela categoria.
        Se válido, cria e armazena o objeto Voto.
        """
        # Verifica se a fase atual da premiação permite o início da votação.
        if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_VOTACAO_ABERTA:
            if self.__controlador_sistema.fase_atual_premiacao == self.__controlador_sistema.FASE_INDICACOES_ABERTAS:
                print("\n❌ A votação ainda não pode começar. O período de indicações precisa ser encerrado primeiro.")
            else:
                print("\n❌ A votação não está disponível nesta fase da premiação.")
            input("🔁 Pressione Enter para continuar...")
            return

        print("\n--- Iniciar Votação ---")

        membros = self.__controlador_membros.entidades

        # Filtra para pegar apenas os jurados que podem votar
        membros_aptos_a_votar = [m for m in membros if m.get("funcao") == "jurado"]  #

        if not membros_aptos_a_votar:
            print("❌ Nenhum membro da academia com função 'jurado' cadastrado para votar.")
            input("🔁 Pressione Enter para continuar...")
            return

        #Seleção do membro (jurado) votante.
        membro_votante_dict = self.__tela_votacao.seleciona_membro_votante(membros_aptos_a_votar)
        if not membro_votante_dict:
            print("ℹ️ Seleção de membro cancelada.")
            input("🔁 Pressione Enter para continuar...")
            return
        membro_id_votante = membro_votante_dict.get("id")

        # Seleção da categoria para votação.
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

        #Verifica se o membro já votou nesta categoria.
        for voto_existente in self.__votos_registrados:
            if voto_existente.membro_id == membro_id_votante and voto_existente.categoria.id == categoria_obj_selecionada.id:
                print(f"⚠️ O membro ID {membro_id_votante} já votou na categoria '{categoria_obj_selecionada.nome}'.")
                input("🔁 Pressione Enter para continuar...")
                return

        # Obtém os finalistas da categoria para apresentar ao votante.
        finalistas_para_votacao = self.__controlador_indicacao.get_finalistas_por_categoria(
            categoria_obj_selecionada.id, 
            limite=5
        )

        if not finalistas_para_votacao:
            print(f"❌ Não há finalistas suficientes ou nenhuma indicação para a categoria '{categoria_obj_selecionada.nome}'.")
            input("🔁 Pressione Enter para continuar...")
            return

        # Seleção do item indicado para o voto.
        indicado_escolhido_dict_tela = self.__tela_votacao.seleciona_indicado_para_voto(
            finalistas_para_votacao, 
            categoria_obj_selecionada.nome
        )

        if not indicado_escolhido_dict_tela:
            print("ℹ️ Votação cancelada ou nenhum indicado selecionado.")
            input("🔁 Pressione Enter para continuar...")
            return
            
        id_item_votado = indicado_escolhido_dict_tela.get("id_original_indicado")
        tipo_item_votado = indicado_escolhido_dict_tela.get("tipo_original_indicado")

        # Criação e armazenamento do objeto Voto.
        id_novo_voto = self._gerar_proximo_id_voto()
        novo_voto = Voto(
            id_voto=id_novo_voto,
            membro_id=membro_id_votante,
            categoria=categoria_obj_selecionada,
            item_indicado_id=id_item_votado,
            tipo_item_indicado=tipo_item_votado
        )

        self.__votos_registrados.append(novo_voto)
        # Adiciona o voto também à lista de votos da própria categoria.
        if hasattr(categoria_obj_selecionada, 'adicionar_voto'):
            categoria_obj_selecionada.adicionar_voto(novo_voto)

        print(f"✅ Voto para '{indicado_escolhido_dict_tela.get('nome_display')}' na categoria '{categoria_obj_selecionada.nome}' registrado com sucesso!")
        input("🔁 Pressione Enter para continuar...")

    def mostrar_resultados(self):
        """
        Calcula e exibe os resultados da votação para cada categoria.

        Agrupa os votos por categoria, conta os votos para cada item indicado
        e os exibe em ordem decrescente de votos. Se não houver votos,
        uma mensagem apropriada é exibida.
        """
        print("\n--- Resultados da Votação ---")
        if not self.__votos_registrados:
            print("📭 Nenhum voto registrado ainda.")
            input("🔁 Pressione Enter para continuar...")
            return

        # Estrutura para armazenar a contagem de votos por categoria e por item.
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
                    print("   Nenhum voto nesta categoria.")
                    continue
                
                votos_ordenados = sorted(dados_cat["contagem_votos"].items(), key=lambda item: item[1], reverse=True)
                
                for item_nome_id, contagem in votos_ordenados:
                    print(f"   - {item_nome_id}: {contagem} voto(s)")
        
        input("🔁 Pressione Enter para continuar...")

    def abrir_menu_votacao(self):
        """
        Exibe o menu de votação e processa a escolha do usuário.

        Permite ao usuário registrar novos votos ou ver os resultados da votação
        até que ele escolha a opção de voltar. Trata exceções de opção inválida.
        """
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
                print(f"❌ {e}")
                input("🔁 Pressione Enter para continuar...")
            except Exception as e:
                print(f"❌ Erro inesperado no menu de votação: {e}")
                input("🔁 Pressione Enter para continuar...")