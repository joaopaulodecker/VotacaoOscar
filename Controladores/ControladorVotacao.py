from datetime import date
from Entidades.Voto import Voto

class ControladorVotacao:
    def __init__(self, categorias: dict, membro):
        self.categorias = categorias
        self.membro = membro

    def votar(self):
        print("Categorias disponíveis:")
        for chave, cat in self.categorias.items():
            print(f"- {chave} ({cat.nome})")

        tipo = input("Digite o tipo da categoria: ").lower()

        if tipo in self.categorias:
            cat = self.categorias[tipo]
            if not cat.indicacoes:
                print("Nenhum indicado nesta categoria.")
                return

            print(f"\nIndicados na categoria {cat.nome}:")
            for i, ind in enumerate(cat.indicacoes):
                nome = ind.ator.nome if tipo == "ator" else ind.diretor.nome if tipo == "diretor" else ind.filme.titulo
                print(f"{i+1}. {nome}")

            idx = int(input("Escolha o número do indicado: ")) - 1
            Voto(self.membro, cat, date.today())
            print("Voto registrado com sucesso!")
        else:
            print("Categoria inválida.")