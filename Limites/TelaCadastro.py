from Utils.validadores import le_num_inteiro, le_texto_alpha_espacos
from Excecoes.OpcaoInvalida import OpcaoInvalida
from datetime import date


class TelaCadastro:

    def __init__(self, tipo):
        self.__tipo = tipo

    def mostra_mensagem(self, msg: str):
        print(msg)

    def espera_input(self, msg: str = "🔁 Pressione Enter para continuar..."):
        """Exibe uma mensagem e aguarda o input do usuário para pausar."""
        input(msg)

    def mostra_cabecalho_operacao(self, operacao: str):
        self.mostra_mensagem(f"\n--- {operacao} de {self.__tipo.capitalize()} ---")

    def mostra_menu(self) -> int:
        self.mostra_mensagem(f"\n===== MENU {self.__tipo.upper()} =====")
        self.mostra_mensagem("1 - Cadastrar")
        self.mostra_mensagem("2 - Alterar")
        self.mostra_mensagem("3 - Excluir")
        self.mostra_mensagem("4 - Listar")
        self.mostra_mensagem("0 - Voltar")

        opcao = le_num_inteiro("Escolha uma opção: ", min_val=0, max_val=4)
        if opcao is None:
            raise OpcaoInvalida("Entrada de opção inválida.")
        return opcao

    def mostra_lista_entidades(self, lista_dados: list[dict]):
        self.mostra_cabecalho_operacao(f"Lista de {self.__tipo.capitalize()}s")
        if not lista_dados:
            self.mostra_mensagem(f"📭 Nenhum(a) {self.__tipo} cadastrado(a).")
        else:
            for dados_entidade in lista_dados:
                self.mostra_mensagem(dados_entidade.get('info_str', 'Dados indisponíveis'))
        self.mostra_mensagem("------------------------------------")

    def pegar_dados(self, dados_atuais=None):
        """Coleta do usuário os dados para cadastrar ou alterar uma entidade."""
        if dados_atuais:
            self.mostra_cabecalho_operacao(
                f"Alteração de {self.__tipo.capitalize()} "
                f"(ID: {dados_atuais.get('id', 'N/A')})"
            )
            self.mostra_mensagem(
                "Deixe o campo em branco para manter o valor atual (quando aplicável)."
            )
        else:
            self.mostra_cabecalho_operacao(
                f"Cadastro de {self.__tipo.capitalize()}"
            )
            self.mostra_mensagem("(Deixe um campo obrigatório em branco para cancelar)")

        try:
            nome_prompt = "Nome"
            if dados_atuais and dados_atuais.get('nome'):
                nome_prompt += f" (atual: {dados_atuais['nome']})"
            nome_final = le_texto_alpha_espacos(f"{nome_prompt}: ", permitir_vazio_cancela=True)
            if dados_atuais and nome_final is None:
                nome_final = dados_atuais.get('nome')

            if not nome_final or not nome_final.strip():
                self.mostra_mensagem("Nome é obrigatório. Operação cancelada.")
                return None

            dados_coletados = {"nome": nome_final.title()}

            if self.__tipo == "membro":
                nac_prompt = "Nacionalidade"
                if dados_atuais and dados_atuais.get('nacionalidade'):
                    nac_prompt += f" (atual: {dados_atuais['nacionalidade']})"
                nac_final = le_texto_alpha_espacos(f"{nac_prompt}: ", permitir_vazio_cancela=True)
                if dados_atuais and nac_final is None:
                    nac_final = dados_atuais.get('nacionalidade')

                if not nac_final or not nac_final.strip():
                    self.mostra_mensagem("Nacionalidade é obrigatória. Operação cancelada.")
                    return None
                dados_coletados["nacionalidade"] = nac_final.title()

                ano_prompt = "Ano de Nascimento"
                if dados_atuais and dados_atuais.get('ano_nascimento'):
                    ano_prompt += f" (atual: {dados_atuais['ano_nascimento']})"
                ano_nasc_final = le_num_inteiro(
                    f"{ano_prompt}: ", min_val=1900, max_val=date.today().year,
                    permitir_vazio=bool(dados_atuais)
                )
                if dados_atuais and ano_nasc_final is None:
                    ano_nasc_final = dados_atuais.get('ano_nascimento')

                if ano_nasc_final is None and not dados_atuais:
                    self.mostra_mensagem("Ano de Nascimento é obrigatório. Operação cancelada.")
                    return None
                dados_coletados["ano_nascimento"] = ano_nasc_final

                funcoes_permitidas = ["ator", "diretor", "jurado"]
                self.mostra_mensagem("\nFunção do membro:")
                for i, opt in enumerate(funcoes_permitidas):
                    self.mostra_mensagem(f"  {i + 1} - {opt.capitalize()}")
                
                funcao_prompt = f"Escolha o número da função (1-{len(funcoes_permitidas)})"
                if dados_atuais and dados_atuais.get('funcao'):
                    funcao_prompt += f" (atual: {dados_atuais.get('funcao').capitalize()})"

                escolha = le_num_inteiro(funcao_prompt + ": ", min_val=0, max_val=len(funcoes_permitidas), permitir_vazio=bool(dados_atuais))
                
                funcao_final = dados_atuais.get('funcao') if dados_atuais else None
                if escolha is not None and escolha > 0:
                    funcao_final = funcoes_permitidas[escolha - 1]
                
                if not funcao_final:
                    self.mostra_mensagem("Função é obrigatória. Operação cancelada.")
                    return None
                dados_coletados["funcao"] = funcao_final

                if funcao_final == 'ator':
                    generos_permitidos = ["Ator", "Atriz"]
                    self.mostra_mensagem("\nGênero Artístico:")
                    self.mostra_mensagem("  1 - Ator")
                    self.mostra_mensagem("  2 - Atriz")

                    genero_prompt = f"Escolha o gênero (1-2)"
                    # Mostra o valor atual se estiver alterando
                    genero_atual = dados_atuais.get('genero_artistico') if dados_atuais else None
                    if genero_atual:
                        genero_prompt += f" (atual: {genero_atual})"

                    # Permite deixar em branco na alteração para manter o valor
                    escolha_genero = le_num_inteiro(
                        genero_prompt + ": ", min_val=1, max_val=2,
                        permitir_vazio=bool(dados_atuais)
                    )

                    genero_final = genero_atual
                    if escolha_genero is not None:
                        genero_final = generos_permitidos[escolha_genero - 1]

                    if not genero_final:
                        self.mostra_mensagem("Gênero é obrigatório para atores. Operação cancelada.")
                        return None
                    # Adiciona a nova informação ao dicionário
                    dados_coletados["genero_artistico"] = genero_final

            return dados_coletados

        except (KeyboardInterrupt, EOFError):
            self.mostra_mensagem("\nOperação cancelada pelo usuário.")
            return None

    def pegar_id(self, mensagem: str) -> int | None:
        """Pede um ID ao usuário e o retorna como inteiro."""
        return le_num_inteiro(mensagem)