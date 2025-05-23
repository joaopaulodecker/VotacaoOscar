from Excecoes.OpcaoInvalida import OpcaoInvalida

class TelaCategoria:
    def __init__(self):
        pass

    def mostra_opcoes(self):
        print("\n----- CATEGORIAS -----")
        print("1 - Cadastrar Categoria")
        print("2 - Alterar Categoria")
        print("3 - Excluir Categoria")
        print("4 - Listar Categorias")
        print("0 - Voltar")

        while True:
            opcao_str = input("Escolha a opção: ").strip()
            if opcao_str.isdigit():
                valor = int(opcao_str)
                if 0 <= valor <= 4:
                    return valor
            raise OpcaoInvalida("Opção de menu de categorias inválida. Escolha entre 0 e 4.")

    def pega_dados_categoria(self, dados_atuais=None):
        print("\n--- Dados da Categoria ---")
        if dados_atuais:
            print(f"(Deixe em branco para manter o valor atual: '{dados_atuais.get('nome', '')}')")
            nome_input = input("Novo nome da categoria: ").strip()
            nome = nome_input if nome_input else dados_atuais.get("nome")
        else:
            nome = input("Nome da categoria: ").strip()

        if not nome:
            print("❌ Nome da categoria não pode ser vazio.")
            return None
        
        return {"nome": nome}

    def seleciona_categoria_por_id(self, mensagem="Digite o ID da categoria: "):
        while True:
            id_str = input(mensagem).strip()
            if not id_str:
                return None
            if id_str.isdigit():
                return id_str
            print("❌ ID inválido. Por favor, digite um número.")

    def confirma_exclusao(self, nome_categoria: str):
        while True:
            confirmacao = input(f"Tem certeza que deseja excluir a categoria '{nome_categoria}'? (S/N): ").strip().upper()
            if confirmacao == 'S':
                return True
            elif confirmacao == 'N':
                return False
            print("❌ Opção inválida. Digite S para Sim ou N para Não.")
            
    def mostra_mensagem(self, msg: str):
        print(f"\n{msg}")
