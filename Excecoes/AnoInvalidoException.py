class AnoInvalidoException(Exception):
    def __init__(self, ano_str: str):
        super().__init__(f"O valor '{ano_str}' não é um ano válido.")