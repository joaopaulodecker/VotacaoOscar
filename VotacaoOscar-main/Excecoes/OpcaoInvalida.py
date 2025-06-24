class OpcaoInvalida(Exception):
    def __init__(self, mensagem="❌Opção inválida. Tente novamente."):
        super().__init__(mensagem)