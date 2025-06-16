from Entidades.Categoria import Categoria
from Utils.validadores import le_num_inteiro

class TelaCategoria:

    def mostra_mensagem(self, msg: str):
        """Exibe uma mensagem genérica para o usuário."""
        print(f"\n{msg}")

    def espera_input(self, msg: str = "🔁 Pressione Enter para continuar..."):
        """Exibe uma mensagem e aguarda o input do usuário para pausar."""
        input(msg)

    def mostra_opcoes(self) -> int:
        """Exibe o menu de opções e retorna a escolha validada do usuário."""
        self.mostra_mensagem("----- CATEGORIAS -----")
        self.mostra_mensagem("1 - Cadastrar Categoria")
        self.mostra_mensagem("2 - Alterar Categoria")
        self.mostra_mensagem("3 - Excluir Categoria")
        self.mostra_mensagem("4 - Listar Categorias")
        self.mostra_mensagem("0 - Voltar")

        return le_num_inteiro("Escolha uma opção: ", min_val=0, max_val=4)

    def mostra_lista_categorias(self, categorias_dados: list[dict]):
        """
        Recebe uma lista de dicionários com dados de categorias e os exibe.
        """
        self.mostra_mensagem("--- Lista de Categorias Cadastradas ---")
        if not categorias_dados:
            self.mostra_mensagem("📭 Nenhuma categoria cadastrada.")
        else:
            for categoria_info in categorias_dados:
                self.mostra_mensagem(
                    f"ID: {categoria_info.get('id')} | "
                    f"Nome: {categoria_info.get('nome')} | "
                    f"Tipo: {categoria_info.get('tipo_indicacao', '').capitalize()}"
                )
        self.mostra_mensagem("------------------------------------")

    def pega_dados_categoria(self, dados_atuais=None):
        """Coleta do usuário os dados para cadastrar ou alterar uma categoria."""
        if dados_atuais:
            self.mostra_mensagem(f"--- Alteração de Categoria (ID: {dados_atuais.get('id')}) ---")
            self.mostra_mensagem("Deixe em branco para manter o valor atual.")
        else:
            self.mostra_mensagem("--- Cadastro de Nova Categoria ---")

        nome_prompt = "Nome da categoria"
        if dados_atuais and dados_atuais.get('nome'):
            nome_prompt += f" (atual: {dados_atuais['nome']})"
        
        nome_input = input(f"{nome_prompt}: ").strip()
        nome_final = nome_input if nome_input else dados_atuais.get("nome")
        
        if not nome_final:
            self.mostra_mensagem("❌ Nome da categoria não pode ser vazio.")
            return None

        # O tipo de indicação só pode ser definido na criação da categoria.
        if not dados_atuais:
            self.mostra_mensagem("\nTipo de Indicação para a Categoria:")
            tipos_validos = Categoria.TIPOS_VALIDOS
            for i, tipo in enumerate(tipos_validos):
                self.mostra_mensagem(f"  {i+1} - {tipo.capitalize()}")

            escolha = le_num_inteiro(
                f"Escolha o número do tipo (1-{len(tipos_validos)}): ",
                min_val=1, max_val=len(tipos_validos)
            )
            if escolha is None:
                self.mostra_mensagem("❌ Seleção de tipo cancelada.")
                return None
            tipo_final = tipos_validos[escolha - 1]
            return {"nome": nome_final, "tipo_indicacao": tipo_final}
        
        return {"nome": nome_final}

    def seleciona_categoria_por_id(self, mensagem="Digite o ID da categoria: ") -> int | None:
        """Pede um ID ao usuário e o retorna como inteiro."""
        return le_num_inteiro(mensagem, permitir_vazio=True)

    def confirma_exclusao(self, nome_categoria: str) -> bool:
        """Pede confirmação do usuário para uma exclusão."""
        confirmacao = input(
            f"Tem certeza que deseja excluir a categoria '{nome_categoria}'? (S/N): "
        ).strip().upper()
        return confirmacao == 'S'