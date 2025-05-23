from Excecoes.OpcaoInvalida import OpcaoInvalida
from Entidades.Categoria import Categoria

class TelaVotacao:

    def mostra_opcoes_votacao(self):
        print("\n----- VOTAÇÃO -----")
        print("1 - Registrar Novo Voto")
        print("2 - Ver Resultados da Votação")
        print("0 - Voltar ao Menu Principal")
        while True:
            opcao_str = input("Escolha a opção: ").strip()
            if opcao_str.isdigit():
                valor = int(opcao_str)
                if 0 <= valor <= 2:
                    return valor
            raise OpcaoInvalida("Opção de menu de votação inválida. Escolha entre 0 e 2.")

    def seleciona_membro_votante(self, membros: list) -> dict | None:
        if not membros:
            print("Nenhum membro da academia disponível para votar.")
            return None
        
        print("\n--- Selecionar Membro Votante ---")
        for i, membro in enumerate(membros):
            print(f"{i + 1}. ID: {membro.get('id')} - Nome: {membro.get('nome')}")
        
        while True:
            try:
                escolha_str = input(f"Escolha o número do membro (1-{len(membros)}) ou 0 para cancelar: ").strip()
                if not escolha_str: # Permite cancelar com Enter
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

    def seleciona_categoria_para_voto(self, categorias: list) -> Categoria | None:
        if not categorias:
            print("Nenhuma categoria disponível para votação.")
            return None

        print("\n--- Selecionar Categoria para Votar ---")
        for i, categoria_obj in enumerate(categorias):
            if isinstance(categoria_obj, Categoria):
                print(f"{i + 1}. ID: {categoria_obj.id} - Nome: {categoria_obj.nome}")
            else:
                print(f"{i + 1}. Categoria inválida (não é objeto Categoria)")


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
                    if isinstance(categorias[escolha - 1], Categoria):
                        return categorias[escolha - 1]
                    else:
                        print("Item selecionado não é um objeto Categoria válido. Tente novamente.")
                else:
                    print(f"Número inválido. Escolha entre 1 e {len(categorias)} ou 0.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

    def seleciona_indicado_para_voto(self, indicados_formatados: list, nome_categoria: str) -> dict | None:
        if not indicados_formatados:
            print(f"Nenhum indicado disponível na categoria '{nome_categoria}' para votação.")
            return None

        print(f"\n--- Votar em Indicados para '{nome_categoria}' ---")
        for i, indicado_info in enumerate(indicados_formatados):
            print(f"{i + 1}. {indicado_info.get('nome_display', 'Item Desconhecido')}")
        
        while True:
            try:
                escolha_str = input(f"Escolha o número do seu voto (1-{len(indicados_formatados)}) ou 0 para cancelar: ").strip()
                if not escolha_str:
                    print("Votação cancelada.")
                    return None
                escolha = int(escolha_str)
                if escolha == 0:
                    print("Votação cancelada.")
                    return None
                if 1 <= escolha <= len(indicados_formatados):
                    return indicados_formatados[escolha - 1]
                print(f"Número inválido. Escolha entre 1 e {len(indicados_formatados)} ou 0.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")
    
    def mostra_mensagem(self, msg: str):
        print(f"\n{msg}")
