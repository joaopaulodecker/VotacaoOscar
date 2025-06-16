from Excecoes.OpcaoInvalida import OpcaoInvalida
from Entidades.Nacionalidade import Nacionalidade
from Utils.validadores import le_num_inteiro

class TelaFilmes:

    def mostra_mensagem(self, msg: str):
        """Exibe uma mensagem genérica para o usuário."""
        print(msg)

    def espera_input(self, msg: str = "🔁 Pressione Enter para continuar..."):
        input(msg)

    def mostra_opcoes(self) -> int:
        """Exibe o menu de opções e retorna a escolha validada do usuário."""
        self.mostra_mensagem("\n----- FILMES -----")
        self.mostra_mensagem("1 - Cadastrar Filme")
        self.mostra_mensagem("2 - Alterar Filme")
        self.mostra_mensagem("3 - Excluir Filme")
        self.mostra_mensagem("4 - Listar Filmes")
        self.mostra_mensagem("5 - Listar Filmes por Nacionalidade")
        self.mostra_mensagem("0 - Voltar")

        while True:
            opcao_str = input("Escolha a opção: ").strip()
            if opcao_str.isdigit():
                valor = int(opcao_str)
                if 0 <= valor <= 5:
                    return valor
            raise OpcaoInvalida(
                "Opção de menu de filmes inválida. Escolha entre 0 e 5."
            )

    def mostra_lista_filmes(self, filmes_dados: list[dict]):
        """
        Recebe uma lista de dicionários com dados de filmes e os exibe.

        Args:
            filmes_dados (list[dict]): Lista de filmes a serem exibidos.
        """
        print("\n--- Lista de Filmes Cadastrados ---")
        for filme_info in filmes_dados:
            prefixo = f"{filme_info.get('id')}. "
            if filme_info.get('com_indice', False):
                prefixo = f"{filme_info.get('indice')}. (ID: {filme_info.get('id')}) "
            
            print(f"{prefixo}🎬 {filme_info.get('titulo')} "
                  f"({filme_info.get('ano')}) "
                  f"Nac: {filme_info.get('nacionalidade')} "
                  f"(Dir: {filme_info.get('diretor')})")

    def mostra_filmes_agrupados(self, filmes_agrupados: dict):
        """
        Recebe um dicionário de filmes agrupados por nacionalidade e os exibe.

        Args:
            filmes_agrupados (dict): Dicionário com nacionalidades como chaves
                                    e listas de dicionários de filmes como valores.
        """
        print("\n--- Filmes Agrupados por Nacionalidade ---")
        for pais, lista_filmes in filmes_agrupados.items():
            print(f"\n🌍 Nacionalidade: {pais}")
            print("------------------------------------")
            for filme_info in lista_filmes:
                print(f"  ID: {filme_info.get('id')}. 🎬 {filme_info.get('titulo')} "
                      f"({filme_info.get('ano')}) "
                      f"(Dir: {filme_info.get('diretor')})")

    def le_dados_filme(self, dados_atuais=None, diretores_disponiveis=None):
        """Coleta os dados para um novo filme ou para alteração."""
        self.mostra_mensagem("\n--- Dados do Filme ---")
        dados_coletados = {}

        if dados_atuais:
            self.mostra_mensagem(
                "(Deixe em branco para manter o valor atual: "
                f"'{dados_atuais.get('titulo', '')}')"
            )
            titulo_input = input("Novo Título do filme: ").strip()
            dados_coletados["titulo"] = (titulo_input if titulo_input
                                         else dados_atuais.get("titulo"))
        else:
            dados_coletados["titulo"] = input("Título do filme: ").strip()

        if dados_coletados.get("titulo"):
            dados_coletados["titulo"] = dados_coletados["titulo"].title()

        if not dados_coletados.get("titulo"):
            self.mostra_mensagem("❌ Título não pode ser vazio.")
            return None

        ano_str = ""
        if dados_atuais:
            self.mostra_mensagem(
                f"(Deixe em branco para manter o valor atual: '{dados_atuais.get('ano', '')}')"
            )
            ano_input = input("Novo Ano de lançamento: ").strip()
            ano_str = ano_input if ano_input else str(dados_atuais.get("ano", ""))
        else:
            ano_str = input("Ano de lançamento: ").strip()
        
        if not ano_str:
            self.mostra_mensagem("❌ Ano não pode ser vazio.")
            return None
        try:
            dados_coletados["ano"] = int(ano_str)
        except ValueError:
            self.mostra_mensagem("❌ Ano inválido. Deve ser um número inteiro.")
            return None

        nacionalidade_prompt = "Nacionalidade do Filme (país)"
        if dados_atuais and dados_atuais.get('nacionalidade_str'):
             nacionalidade_prompt += f" (atual: {dados_atuais['nacionalidade_str']})"
        nacionalidade_prompt += ": "
        
        pais_input_str = input(nacionalidade_prompt).strip()
        if dados_atuais and not pais_input_str:
            dados_coletados["nacionalidade_str"] = dados_atuais.get('nacionalidade_str')
        else:
            if not pais_input_str:
                self.mostra_mensagem("❌ Nacionalidade (país) é obrigatória.")
                return None
            dados_coletados["nacionalidade_str"] = pais_input_str.title()
        
        if diretores_disponiveis and len(diretores_disponiveis) > 0:
            self.mostra_mensagem("\n--- Diretor do Filme ---")
            for i, diretor in enumerate(diretores_disponiveis):
                self.mostra_mensagem(f"  {i+1} - {diretor.get('nome')} "
                                     f"(ID: {diretor.get('id')})")
            
            prompt_base = f"Escolha o número do diretor (1-{len(diretores_disponiveis)})"
            if dados_atuais and dados_atuais.get('diretor_id'):
                prompt_base += f" (atual: ID {dados_atuais['diretor_id']})"
                
            escolha = le_num_inteiro(prompt_base + ": ",
                                     min_val=0 if dados_atuais else 1, # Permite 0 para manter
                                     max_val=len(diretores_disponiveis))
            
            if dados_atuais and escolha == 0:
                dados_coletados["diretor_id"] = dados_atuais.get('diretor_id')
            elif escolha is not None:
                dados_coletados["diretor_id"] = diretores_disponiveis[escolha - 1].get('id')
            else:
                return None # Cancelado ou inválido
        elif not dados_atuais:
            self.mostra_mensagem("❌ Não há diretores para selecionar.")
            return None
        else:
            dados_coletados["diretor_id"] = dados_atuais.get('diretor_id')

        return dados_coletados
    
    def seleciona_filme_por_id(self, mensagem="Digite o ID do filme: "):
        id_str = input(mensagem).strip()
        if id_str.isdigit():
            return int(id_str)
        self.mostra_mensagem("❌ ID inválido. Por favor, digite um número.")
        return None

    def confirma_exclusao(self, titulo_filme) -> bool:
        confirmacao = input(
            f"Tem certeza que deseja excluir o filme '{titulo_filme}'? (S/N): "
        ).strip().upper()
        return confirmacao == 'S'