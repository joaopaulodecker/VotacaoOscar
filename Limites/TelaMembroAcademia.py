from Utils.validadores import le_data, le_string_permitindo_vazio, le_num_inteiro
from Excecoes.OpcaoInvalida import OpcaoInvalida
from datetime import date


class TelaMembroAcademia:
    def __init__(self):
        pass

    def mostra_mensagem(self, msg: str):
        print(f"\n{msg}")

    def espera_input(self, msg: str = "🔁 Pressione Enter para continuar..."):
        """Exibe uma mensagem e aguarda o input do usuário para pausar."""
        input(msg)

    def mostra_lista_membros(self, lista_dados_membros: list[dict]):

        self.mostra_mensagem("👥 Lista de Membros:")
        for dados_membro in lista_dados_membros:
            self.mostra_mensagem(dados_membro.get('info_str', 'Dados indisponíveis'))

    def mostrar_menu(self) -> int:
        self.mostra_mensagem("\n----- Menu Membro da Academia -----")
        self.mostra_mensagem("1 - Cadastrar Membro")
        self.mostra_mensagem("2 - Alterar Membro")
        self.mostra_mensagem("3 - Excluir Membro")
        self.mostra_mensagem("4 - Listar Membros")
        self.mostra_mensagem("0 - Voltar")

        while True:
            opcao_str = input("Escolha uma opção: ").strip()
            if opcao_str.isdigit():
                opcao = int(opcao_str)
                if 0 <= opcao <= 4:
                    return opcao
            raise OpcaoInvalida("Opção de menu inválida. Escolha entre 0 e 4.")

    def pegar_dados(self, dados_atuais: dict | None = None) -> dict | None:

        self.mostra_mensagem("\n--- Dados do Membro da Academia ---")

        nome_atual = dados_atuais.get("nome", "") if dados_atuais else ""
        prompt_nome = f"Nome ({'manter: ' + nome_atual if nome_atual else 'obrigatório'}): "
        nome = le_string_permitindo_vazio(prompt_nome)
        if dados_atuais and not nome:
            nome = nome_atual
        elif not nome:
            self.mostra_mensagem("❌ Nome é obrigatório.")
            return None

        data_nasc_atual_obj = dados_atuais.get("data_nascimento") if dados_atuais else None
        data_nasc_atual_str = data_nasc_atual_obj.strftime("%d/%m/%Y") if isinstance(data_nasc_atual_obj, date) else ""
        
        prompt_data = f"Data de Nascimento ({'manter: ' + data_nasc_atual_str if data_nasc_atual_str else 'DD/MM/AAAA, obrigatório'}): "
        data_nascimento = le_data(prompt_data, permitir_vazio=bool(dados_atuais))
        
        if dados_atuais and data_nascimento is None:
            data_nascimento = data_nasc_atual_obj
        elif data_nascimento is None and not dados_atuais:
            self.mostra_mensagem("❌ Data de nascimento é obrigatória.")
            return None

        nacionalidade_atual = dados_atuais.get("nacionalidade_pais", "") if dados_atuais else ""
        prompt_nac = f"País da Nacionalidade ({'manter: ' + nacionalidade_atual if nacionalidade_atual else 'obrigatório'}): "
        nacionalidade_pais = le_string_permitindo_vazio(prompt_nac)
        if dados_atuais and not nacionalidade_pais:
            nacionalidade_pais = nacionalidade_atual
        elif not nacionalidade_pais:
            self.mostra_mensagem("❌ Nacionalidade (país) é obrigatória.")
            return None

        funcao_atual = dados_atuais.get("funcao", "") if dados_atuais else ""
        prompt_funcao = f"Função (ex: ator, diretor) ({'manter: ' + funcao_atual if funcao_atual else 'obrigatório'}): "
        funcao = le_string_permitindo_vazio(prompt_funcao)
        if dados_atuais and not funcao:
            funcao = funcao_atual
        elif not funcao:
            self.mostra_mensagem("❌ Função é obrigatória.")
            return None

        return {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "nacionalidade_pais": nacionalidade_pais,
            "funcao": funcao.lower()
        }

    def pegar_id(self, mensagem: str = "Digite o ID do membro: ") -> int | None:
        while True:
            id_str = input(mensagem).strip()
            if not id_str:
                self.mostra_mensagem("ℹ️ Operação de busca por ID cancelada.")
                return None
            if id_str.isdigit():
                return int(id_str)
            self.mostra_mensagem("❌ ID inválido. Deve ser um número inteiro.")