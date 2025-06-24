class EntidadeDuplicadaException(Exception):
    def __init__(self, mensagem="Erro: Já existe um registro com os dados informados."):
        super().__init__(mensagem)