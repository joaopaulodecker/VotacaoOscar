from Limites.TelaCadastro import TelaCadastro

class ControladorCadastro:
    def __init__(self, tipo):
        self.__tipo = tipo  # "membro", "ator", etc.
        self.__tela = TelaCadastro(tipo)
        self.__entidades = []  # Lista simples como armazenamento inicial

    def abrir_menu(self):
        while True:
            opcao = self.__tela.mostrar_menu()
            if opcao == 1:
                self.cadastrar()
            elif opcao == 2:
                self.alterar()
            elif opcao == 3:
                self.excluir()
            elif opcao == 4:
                self.listar()
            elif opcao == 0:
                break
            else:
                print("❌ Opção inválida.")

    def cadastrar(self):
        dados = self.__tela.pegar_dados()
        self.__entidades.append(dados)
        print(f"✅ {self.__tipo.capitalize()} cadastrado com sucesso!")

    def alterar(self):
        id_alvo = self.__tela.pegar_id()
        for entidade in self.__entidades:
            if entidade["id"] == id_alvo:
                novos_dados = self.__tela.pegar_dados()
                entidade.update(novos_dados)
                print("✅ Alteração realizada com sucesso!")
                return
        print("❌ ID não encontrado.")

    def excluir(self):
        id_alvo = self.__tela.pegar_id()
        for i, entidade in enumerate(self.__entidades):
            if entidade["id"] == id_alvo:
                del self.__entidades[i]
                print("🗑️ Registro excluído.")
                return
        print("❌ ID não encontrado.")

    def listar(self):
        if not self.__entidades:
            print(f"📭 Nenhum {self.__tipo} cadastrado.")
        for entidade in self.__entidades:
            print(entidade)
