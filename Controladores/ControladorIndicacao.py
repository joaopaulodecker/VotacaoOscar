from Entidades.Ator import Ator
from Entidades.Diretor import Diretor
from Entidades.Filme import Filme
from Entidades.IndAtor import IndAtor
from Entidades.IndDiretor import IndDiretor
from Entidades.IndFilme import IndFilme
from collections import Counter

class ControladorIndicacao:
    def __init__(self, categorias: dict, membro):
        self.categorias = categorias
        self.membro = membro

    def indicar_ator(self, nome):
        ator = Ator(nome, self.membro.data_nascimento, self.membro.nacionalidade)
        IndAtor(ator, self.categorias["ator"], self.membro)
        self._listar("ator")

    def indicar_diretor(self, nome):
        diretor = Diretor(nome, self.membro.data_nascimento, self.membro.nacionalidade)
        IndDiretor(diretor, self.categorias["diretor"], self.membro)
        self._listar("diretor")

    def indicar_filme(self, titulo):
        diretor = Diretor("Fictício", self.membro.data_nascimento, self.membro.nacionalidade)
        filme = Filme(titulo, diretor, 2024, self.membro.nacionalidade)
        IndFilme(filme, self.categorias["filme"], self.membro)
        self._listar("filme")

    def _listar(self, tipo):
        cat = self.categorias[tipo]
        nomes = []
        for ind in cat.indicacoes:
            if tipo == "ator": nomes.append(ind.ator.nome)
            elif tipo == "diretor": nomes.append(ind.diretor.nome)
            else: nomes.append(ind.filme.titulo)
        cont = Counter(nomes)
        print("\nIndicados:")
        for nome, qtd in cont.items():
            print(f"- {nome}: {qtd} indicação(ões)")
