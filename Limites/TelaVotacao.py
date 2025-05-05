class TelaVotacao:
    def __init__(self, controlador):
        self.controlador = controlador

    def mostrar(self):
        print("\n=== Tela de Votação ===")
        self.controlador.votar()
