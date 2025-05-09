class TelaIndicacao:
    def __init__(self, controlador):
        self.controlador = controlador

    def mostrar(self):
        print("\n=== Tela de Indicação ===")
        print("1. Indicar Ator")
        print("2. Indicar Diretor")
        print("3. Indicar Filme")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            nome = input("Nome do ator: ")
            self.controlador.indicar_ator(nome)

        elif escolha == "2":
            nome = input("Nome do diretor: ")
            self.controlador.indicar_diretor(nome)

        elif escolha == "3":
            titulo = input("Título do filme: ")
            self.controlador.indicar_filme(titulo)