from Limites.TelaSistema import TelaSistema

class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema()

    def inicializa_sistema(self):
        while True:
            opcao = self.__tela_sistema.mostra_opcoes()

            if opcao == 1:
                print(">> Entrou em Membros")
            elif opcao == 2:
                print(">> Entrou em Atores")
            elif opcao == 3:
                print(">> Entrou em Diretores")
            elif opcao == 4:
                print(">> Entrou em Filmes")
            elif opcao == 5:
                print(">> Entrou em Categorias")
            elif opcao == 6:
                print(">> Entrou em Indicar")
            elif opcao == 7:
                print(">> Entrou em Votar")
            elif opcao == 0:
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida.")
