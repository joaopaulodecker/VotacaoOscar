class ControladorIndicacoes:
    def __init__(self):
        self.__todas_indicacoes = []

    def registrar_indicacao(self, indicacao: Indicacao):
        if self.__ja_foi_indicado(indicacao):
            print("⚠️ Já existe essa indicação para essa categoria. Ignorado.")
        else:
            self.__todas_indicacoes.append(indicacao)

    def __ja_foi_indicado(self, nova_indicacao: Indicacao):
        for ind in self.__todas_indicacoes:
            if isinstance(ind, type(nova_indicacao)):
                if isinstance(ind, IndAtor) and ind.ator.nome == nova_indicacao.ator.nome and ind.categoria.nome == nova_indicacao.categoria.nome:
                    return True
                if isinstance(ind, IndDiretor) and ind.diretor.nome == nova_indicacao.diretor.nome and ind.categoria.nome == nova_indicacao.categoria.nome:
                    return True
                if isinstance(ind, IndFilme) and ind.filme.titulo == nova_indicacao.filme.titulo and ind.categoria.nome == nova_indicacao.categoria.nome:
                    return True
        return False

    def get_indicacoes_por_tipo(self, tipo):
        return [i for i in self.__todas_indicacoes if tipo in i.__class__.__name__.lower()]

