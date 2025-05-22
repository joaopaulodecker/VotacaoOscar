from Limites.TelaCadastro import TelaCadastro
from Excecoes.OpcaoInvalida import OpcaoInvalida

class ControladorCadastro:
    def __init__(self, tipo):
        self.__tipo = tipo
        self.__tela = TelaCadastro(tipo)
        self.__entidades = []

    @property
    def entidades(self):
        return self.__entidades

    def abrir_menu(self):
        while True:
            try:
                opcao = self.__tela.mostrar_menu()
                if opcao == 1:
                    self.cadastrar()
                elif opcao == 2:
                    self.alterar()
                elif opcao == 3:
                    self.excluir()
                elif opcao == 4:
                    self.listar(mostrar_msg_voltar=True)
                elif opcao == 0:
                    break
            except OpcaoInvalida as e:
                print(f"❌ {e}")
                input("🔁 Pressione Enter para tentar novamente...")


    def cadastrar(self):
        dados = self.__tela.pegar_dados()
        if dados:
            self.__entidades.append(dados)
            print(f"✅ {self.__tipo.capitalize()} cadastrado com sucesso!")
            input("🔁 Pressione Enter para continuar...")

    def alterar(self):
        self.listar()
        id_alvo = self.__tela.pegar_id()

        for entidade in self.__entidades:
            if entidade["id"] == id_alvo:
                novos_dados = self.__tela.pegar_dados()
                if novos_dados["id"] != id_alvo and any(e["id"] == novos_dados["id"] for e in self.__entidades):
                    print(f"❌ Já existe um {self.__tipo} com ID {novos_dados['id']}.")
                else:
                    entidade.update(novos_dados)
                    print("✅ Alteração realizada com sucesso!")
                input("🔁 Pressione Enter para continuar...")
                return
        print("❌ ID não encontrado.")
        input("🔁 Pressione Enter para continuar...")

    def excluir(self):
        self.listar()
        id_alvo = self.__tela.pegar_id()
        for i, entidade in enumerate(self.__entidades):
            if entidade["id"] == id_alvo:
                del self.__entidades[i]
                print("🗑️ Registro excluído com sucesso!")
                input("🔁 Pressione Enter para continuar...")
                return
        print("❌ ID não encontrado.")
        input("🔁 Pressione Enter para continuar...")

    def listar(self, mostrar_msg_voltar=False):
        if not self.__entidades:
            print(f"📭 Nenhum {self.__tipo} cadastrado.")
        else:
            print(f"\n📋 Lista de {self.__tipo.capitalize()}s:")
            for entidade in self.__entidades:
                print(f"ID: {entidade['id']} | Nome: {entidade.get('nome', 'N/A')}")
        if mostrar_msg_voltar:
            input("🔁 Pressione Enter para voltar ao menu...")

    def existe_id(self, id_busca):
        return any(entidade["id"] == id_busca for entidade in self.__entidades)