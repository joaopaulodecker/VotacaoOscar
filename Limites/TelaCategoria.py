class TelaCategoria:
    def __init__(self):
        pass

    def mostrar_tela(self):
        print("\n--- Menu Categoria ---")
        print("1 - Incluir categoria")
        print("2 - Alterar categoria")
        print("3 - Listar categorias")
        print("4 - Remover categoria")
        print("0 - Voltar")
        return int(input("Escolha uma opção:"))

    def pega_dados_categoria(self):
        nome = input("Digite o nome da categoria:")
        return {"nome": nome}

    def mostra_mensagem(self, msg):
        print(f"\n{msg}")

