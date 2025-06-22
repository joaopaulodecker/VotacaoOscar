from Utils.validadores import le_num_inteiro, le_string_nao_vazia
from datetime import date


class TelaMembros:

    def __init__(self):
        pass

    def mostra_mensagem(self, msg: str):
        print(f"\n{msg}")

    def espera_input(self, msg: str = "🔁 Pressione Enter para continuar..."):
        """Exibe uma mensagem e aguarda o input do usuário para pausar."""
        input(msg)

    def mostra_menu_membros(self) -> int:
        """Exibe o menu específico para o gerenciamento de membros."""
        self.mostra_mensagem("\n----- GERENCIAR PESSOAS -----")
        self.mostra_mensagem("1 - Cadastrar Nova Pessoa")
        self.mostra_mensagem("2 - Alterar Pessoa")
        self.mostra_mensagem("3 - Excluir Pessoa")
        self.mostra_mensagem("4 - Listar Pessoas")
        self.mostra_mensagem("0 - Voltar ao Menu Principal")
        return le_num_inteiro("Escolha uma opção: ", min_val=0, max_val=4)

    def mostra_lista_membros(self, membros_dados: list[str]):
        self.mostra_mensagem("\n--- Lista de Pessoas Cadastradas ---")
        if not membros_dados:
            self.mostra_mensagem("📭 Nenhuma pessoa cadastrada.")
            return

        for info_str in membros_dados:
            self.mostra_mensagem(f"- {info_str}")

    def pega_dados_membro(self, dados_atuais: dict = None) -> dict | None:
        """Coleta dados para cadastrar OU alterar um membro. Se 'dados_atuais' for
        fornecido, entra em modo de alteração, senão, entra em modo de cadastro."""

        # Modo Alteração
        if dados_atuais:
            self.mostra_mensagem("\n--- Alteração de Membro ---")
            self.mostra_mensagem("Dica: Deixe em branco e pressione Enter para manter o valor atual.")

            nome_prompt = f"Novo nome (atual: {dados_atuais.get('nome')}): "
            nome_input = input(nome_prompt)
            nome_final = nome_input.strip() if nome_input else dados_atuais.get("nome")

            data_atual = dados_atuais.get('data_nascimento')
            data_prompt = f"Novo ano de nascimento (atual: {data_atual}): "
            data_input = input(data_prompt)
            data_final = int(data_input) if data_input.isdigit() else data_atual

            return {"nome": nome_final, "data_nascimento": data_final}

        else:
            self.mostra_mensagem("\n--- Cadastro de Nova Pessoa ---")
            # 1. Pergunta o tipo de pessoa
            self.mostra_mensagem("Qual o tipo de pessoa a ser cadastrada?")
            self.mostra_mensagem("1 - Ator/Atriz")
            self.mostra_mensagem("2 - Diretor(a)")
            self.mostra_mensagem("3 - Membro da Academia")
            tipo_num = le_num_inteiro("Escolha o tipo (deixe em branco para cancelar): ", min_val=1, max_val=3,
                                      permitir_vazio=True)
            if tipo_num is None: return None
            mapa_tipos = {1: 'ator', 2: 'diretor', 3: 'membro'}
            tipo_pessoa = mapa_tipos[tipo_num]

            # 2. Coleta os dados comuns usando os validadores
            nome = le_string_nao_vazia("Nome completo: ")
            if nome is None: return None

            # Usando a importação date.today()
            ano_atual = date.today().year
            data_nascimento = le_num_inteiro(f"Ano de nascimento (ex: 1980): ", min_val=1900, max_val=ano_atual)
            if data_nascimento is None: return None

            nacionalidade_str = le_string_nao_vazia("País de nacionalidade: ")
            if nacionalidade_str is None: return None

            dados_retorno = {
                "tipo_pessoa": tipo_pessoa,
                "nome": nome,
                "data_nascimento": data_nascimento,
                "nacionalidade_str": nacionalidade_str
            }

            # 3. Coleta dados específicos apenas se for Ator
            if tipo_pessoa == 'ator':
                self.mostra_mensagem("\nQual o gênero artístico?")
                self.mostra_mensagem("1 - Ator")
                self.mostra_mensagem("2 - Atriz")
                genero_num = le_num_inteiro("Escolha o gênero: ", min_val=1, max_val=2)
                if genero_num is None: return None
                dados_retorno["genero_artistico"] = "Ator" if genero_num == 1 else "Atriz"

            return dados_retorno

    def pegar_id(self, mensagem="Digite o ID: ") -> int | None:
        """Pede um ID ao usuário e o retorna como inteiro."""
        return le_num_inteiro(mensagem, permitir_vazio=True)

    def confirma_exclusao(self, nome_item: str) -> bool:
        """Pede confirmação do usuário para uma exclusão."""
        resposta = le_string_nao_vazia(f"Tem certeza que deseja excluir '{nome_item}'? (S/N): ")
        return resposta is not None and resposta.upper().startswith('S')