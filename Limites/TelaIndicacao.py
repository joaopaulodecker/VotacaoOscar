from Utils.validadores import le_num_inteiro
from Excecoes.OpcaoInvalida import OpcaoInvalida
from Entidades.Categoria import Categoria
from Entidades.Filme import Filme

class TelaIndicacao:

    def mostra_opcoes_indicacao(self):
        print("\n----- INDICAÇÕES -----")
        print("1 - Registrar Nova Indicação")
        print("2 - Listar Indicações por Categoria")
        print("0 - Voltar ao Menu Principal")
        print("0 - Voltar ao Menu Principal")
        while True:
            opcao_str = input("Escolha a opção: ").strip()
            if opcao_str.isdigit():
                valor = int(opcao_str)
                if 0 <= valor <= 2:
                    return valor
            raise OpcaoInvalida("Opção de menu de indicações inválida. Escolha entre 0 e 2.")

    def seleciona_membro(self, membros: list) -> dict | None:
        if not membros:
            print("Nenhum membro da academia disponível para seleção.")
            return None
        
        print("\n--- Selecionar Membro da Academia ---")
        for i, membro in enumerate(membros):
            print(f"{i + 1}. ID: {membro.get('id')} - Nome: {membro.get('nome')}")
        
        while True:
            try:
                escolha_str = input(f"Escolha o número do membro (1-{len(membros)}) ou 0 para cancelar: ").strip()
                if not escolha_str:
                    print("Seleção cancelada.")
                    return None
                escolha = int(escolha_str)
                if escolha == 0:
                    print("Seleção cancelada.")
                    return None
                if 1 <= escolha <= len(membros):
                    return membros[escolha - 1]
                print(f"Número inválido. Escolha entre 1 e {len(membros)} ou 0.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

    def seleciona_categoria(self, categorias: list) -> Categoria | None:
        if not categorias:
            print("Nenhuma categoria disponível para seleção.")
            return None

        print("\n--- Selecionar Categoria ---")
        for i, categoria_obj in enumerate(categorias):
            if isinstance(categoria_obj, Categoria):
                print(f"{i + 1}. ID: {categoria_obj.id} - Nome: {categoria_obj.nome}")
            else:
                print(f"{i + 1}. {categoria_obj}")


        while True:
            try:
                escolha_str = input(f"Escolha o número da categoria (1-{len(categorias)}) ou 0 para cancelar: ").strip()
                if not escolha_str:
                    print("Seleção cancelada.")
                    return None
                escolha = int(escolha_str)
                if escolha == 0:
                    print("Seleção cancelada.")
                    return None
                if 1 <= escolha <= len(categorias):
                    return categorias[escolha - 1]
                print(f"Número inválido. Escolha entre 1 e {len(categorias)} ou 0.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

    def pega_tipo_item_indicado(self, nome_categoria_para_contexto: str = None) -> str | None:
        if nome_categoria_para_contexto:
            print(f"\nPara a categoria '{nome_categoria_para_contexto}', você quer indicar:")
        else:
            print("\n📌 Você quer indicar:")
        print("1 - Filme 🎬")
        print("2 - Ator/Atriz 🎭")
        print("3 - Diretor(a) 🎬")
        print("0 - Cancelar Indicação")
        
        while True:
            opcao = le_num_inteiro("👉 Escolha uma opção (0-3): ", min_val=0, max_val=3)
            if opcao == 1:
                return "filme"
            elif opcao == 2:
                return "ator"
            elif opcao == 3:
                return "diretor"
            elif opcao == 0:
                return None # Cancelamento

    def seleciona_filme(self, filmes: list) -> Filme | None:
        if not filmes:
            print("Nenhum filme disponível para seleção.")
            return None

        print("\n--- Selecionar Filme ---")
        for i, filme_obj in enumerate(filmes):
             if isinstance(filme_obj, Filme):
                print(f"{i + 1}. ID: {filme_obj.id_filme} - Título: {filme_obj.titulo} ({filme_obj.ano})")
             else:
                print(f"{i + 1}. {filme_obj}")


        while True:
            try:
                escolha_str = input(f"Escolha o número do filme (1-{len(filmes)}) ou 0 para cancelar: ").strip()
                if not escolha_str:
                    print("Seleção cancelada.")
                    return None
                escolha = int(escolha_str)
                if escolha == 0:
                    print("Seleção cancelada.")
                    return None
                if 1 <= escolha <= len(filmes):
                    return filmes[escolha - 1]
                print(f"Número inválido. Escolha entre 1 e {len(filmes)} ou 0.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

    def seleciona_membro_por_funcao(self, membros_funcao: list, funcao_nome: str) -> dict | None:
        if not membros_funcao:
            print(f"Nenhum(a) {funcao_nome} disponível para seleção.")
            return None

        print(f"\n--- Selecionar {funcao_nome} ---")
        for i, membro_dict in enumerate(membros_funcao):
            print(f"{i + 1}. ID: {membro_dict.get('id')} - Nome: {membro_dict.get('nome')}")

        while True:
            try:
                escolha_str = input(f"Escolha o número do(a) {funcao_nome} (1-{len(membros_funcao)}) ou 0 para cancelar: ").strip()
                if not escolha_str:
                    print("Seleção cancelada.")
                    return None
                escolha = int(escolha_str)
                if escolha == 0:
                    print("Seleção cancelada.")
                    return None
                if 1 <= escolha <= len(membros_funcao):
                    return membros_funcao[escolha - 1]
                print(f"Número inválido. Escolha entre 1 e {len(membros_funcao)} ou 0.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")
    
    def mostra_mensagem(self, msg: str):
        print(f"\n{msg}")