from Entidades.MembroAcademia import MembroAcademia
from Entidades.Nacionalidade import Nacionalidade
from Entidades.Categoria import Categoria
from datetime import date
from Controladores.ControladorIndicacao import ControladorIndicacao
from Controladores.ControladorVotacao import ControladorVotacao
from Limites.TelaIndicacao import TelaIndicacao
from Limites.TelaVotacao import TelaVotacao

def main():
    # Nacionalidade comum
    brasileira = Nacionalidade("Brasileira")

    # Membros da academia
    membro_indicador = MembroAcademia("João", date(1980, 1, 1), brasileira, 1, "Diretor")
    membro_votante = MembroAcademia("Cecília", date(1985, 5, 5), brasileira, 2, "Crítica de Cinema")

    # Categorias compartilhadas
    categorias = {
        "ator": Categoria("Melhor Ator"),
        "diretor": Categoria("Melhor Diretor"),
        "filme": Categoria("Melhor Filme")
    }

    # Controladores
    controlador_indicacao = ControladorIndicacao(categorias, membro_indicador)
    controlador_votacao = ControladorVotacao(categorias, membro_votante)

    # Telas
    tela_indicacao = TelaIndicacao(controlador_indicacao)
    tela_votacao = TelaVotacao(controlador_votacao)

    # Menu principal
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Fazer Indicação")
        print("2. Realizar Votação")
        print("0. Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            tela_indicacao.mostrar()
        elif opcao == "2":
            tela_votacao.mostrar()
        elif opcao == "0":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
