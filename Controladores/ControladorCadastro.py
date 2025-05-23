from Limites.TelaCadastro import TelaCadastro
from Excecoes.OpcaoInvalida import OpcaoInvalida

class ControladorCadastro:
    def __init__(self, tipo_entidade):
        self.__tipo_entidade = tipo_entidade
        self.__tela = TelaCadastro(tipo_entidade)
        self.__entidades = []
        self.__proximo_id = 1

    @property
    def entidades(self):
        return self.__entidades

    def _gerar_proximo_id(self):
        id_atual = self.__proximo_id
        self.__proximo_id += 1
        return id_atual

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
        print(f"\n--- Cadastro de Novo {self.__tipo_entidade.capitalize()} ---")
        dados = self.__tela.pegar_dados()
        if dados:
            dados["id"] = self._gerar_proximo_id()  # ID gerado automaticamente
            self.__entidades.append(dados)
            print(f"✅ {self.__tipo_entidade.capitalize()} cadastrado(a) com sucesso! (ID: {dados['id']})")
        else:
            print(f"ℹ️ Cadastro de {self.__tipo_entidade} cancelado.")
        input("🔁 Pressione Enter para continuar...")

    def alterar(self):
        print(f"\n--- Alteração de {self.__tipo_entidade.capitalize()} ---")
        if not self.listar():
            input("🔁 Pressione Enter para continuar...")
            return

        id_alvo = self.__tela.pegar_id(mensagem=f"Digite o ID do(a) {self.__tipo_entidade} que deseja alterar: ")
        if id_alvo is None:
            print("ℹ️ Alteração cancelada.")
            input("🔁 Pressione Enter para continuar...")
            return

        entidade_encontrada = None
        for entidade in self.__entidades:
            if entidade.get("id") == id_alvo:
                entidade_encontrada = entidade
                break

        if entidade_encontrada:
            print(f"\nEditando dados do(a) {self.__tipo_entidade} com ID: {id_alvo}")
            novos_dados = self.__tela.pegar_dados(dados_atuais=entidade_encontrada)

            if novos_dados:
                entidade_encontrada.update(novos_dados)
                print("✅ Alteração realizada com sucesso!")
            else:
                print("ℹ️ Nenhuma alteração realizada.")
        else:
            print(f"❌ {self.__tipo_entidade.capitalize()} com ID {id_alvo} não encontrado.")

        input("🔁 Pressione Enter para continuar...")

    def excluir(self):
        print(f"\n--- Exclusão de {self.__tipo_entidade.capitalize()} ---")
        if not self.listar():
            input("🔁 Pressione Enter para continuar...")
            return

        id_alvo = self.__tela.pegar_id(mensagem=f"Digite o ID do(a) {self.__tipo_entidade} que deseja excluir: ")
        if id_alvo is None:
            print("ℹ️ Exclusão cancelada.")
            input("🔁 Pressione Enter para continuar...")
            return

        entidade_para_excluir = None
        indice_entidade = -1

        for i, entidade in enumerate(self.__entidades):
            if entidade.get("id") == id_alvo:
                entidade_para_excluir = entidade
                indice_entidade = i
                break

        if entidade_para_excluir:
            del self.__entidades[indice_entidade]
            print("🗑️ Registro excluído com sucesso!")
        else:
            print(f"❌ {self.__tipo_entidade.capitalize()} com ID {id_alvo} não encontrado.")

        input("🔁 Pressione Enter para continuar...")

    def listar(self, mostrar_msg_voltar=False):
        if not self.__entidades:
            print(f"📭 Nenhum(a) {self.__tipo_entidade} cadastrado(a).")
            return False
        else:
            print(f"\n--- Lista de {self.__tipo_entidade.capitalize()}s ---")
            for entidade in self.__entidades:
                id_entidade = entidade.get('id', 'N/A')
                nome_entidade = entidade.get('nome', 'N/A')
                funcao_entidade = entidade.get('funcao', '')
                if funcao_entidade:
                    print(f"ID: {id_entidade} | Nome: {nome_entidade} | Função: {funcao_entidade.capitalize()}")
                else:
                    print(f"ID: {id_entidade} | Nome: {nome_entidade}")
            print("------------------------------------")
            if mostrar_msg_voltar:
                input("🔁 Pressione Enter para voltar ao menu...")
            return True

    def existe_id(self, id_busca):
        return any(entidade.get("id") == id_busca for entidade in self.__entidades)

    def buscar_por_id(self, id_busca):
        for entidade in self.__entidades:
            if entidade.get("id") == id_busca:
                return entidade
        return None

    def buscar_por_funcao(self, funcao_busca):
        encontrados = []
        for entidade in self.__entidades:
            if entidade.get("funcao") == funcao_busca:
                encontrados.append(entidade)
        return encontrados
