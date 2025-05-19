class VotoDuplicadoException(Exception):
    def __init__(self):
        super().__init__("O membro já votou nesta categoria.")