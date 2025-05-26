from Limites.TelaCadastro import TelaCadastro
from Excecoes.OpcaoInvalida import OpcaoInvalida
from datetime import date

class ControladorCadastro:
    """
    Controlador genérico responsável pelas operações de Cadastro, Leitura,
    Atualização e Exclusão (CRUD) de uma entidade específica.

    A entidade gerenciada é definida pelo `tipo_entidade` passado
    durante a inicialização. Interage com `TelaCadastro` para a
    entrada e saída de dados do usuário.
    """
    def __init__(self, tipo_entidade):
        """Inicializa o controlador para um tipo específico de entidade.

        Args:
            tipo_entidade (str): O nome do tipo de entidade que este
                                 controlador irá gerenciar (e.g., "membro", "categoria").
                                 Este nome é usado em mensagens para o usuário.
        """
        self.__tipo_entidade = tipo_entidade
        self.__tela = TelaCadastro(tipo_entidade)
        self.__entidades = []
        self.__proximo_id = 1

    @property
    def entidades(self):
        """
        Retorna a lista de entidades gerenciadas por este controlador.

        Returns:
            list: Uma lista contendo as entidades (atualmente como dicionários
                  ou objetos, dependendo da implementação da subclasse).
        """
        return self.__entidades

    def _gerar_proximo_id(self):
        """
        Gera um ID numérico sequencial para uma nova entidade.

        Returns:
            int: O próximo ID disponível.
        """
        id_atual = self.__proximo_id
        self.__proximo_id += 1
        return id_atual

    def abrir_menu(self):
        """
        Exibe o menu principal de cadastro para a entidade gerenciada
        e processa a escolha do usuário (Cadastrar, Alterar, Excluir, Listar).

        O loop continua até que o usuário escolha a opção de voltar (0).
        Trata OpcaoInvalida levantada pela tela.
        """
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
        """
        Solicita os dados de uma nova entidade através da tela e a adiciona
        à lista de entidades gerenciadas, atribuindo um novo ID.
        """
        print(f"\n--- Cadastro de Novo {self.__tipo_entidade.capitalize()} ---")
        dados = self.__tela.pegar_dados()
        if dados:
            dados["id"] = self._gerar_proximo_id()
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
                novos_dados.pop('id', None)
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
        """
        Lista todas as entidades cadastradas na tela.

        Args:
            mostrar_msg_voltar (bool, optional): Se True, exibe uma mensagem
                                                 para o usuário pressionar Enter
                                                 para voltar ao menu após a listagem.
                                                 Default é False.
        Returns:
            bool: True se houver entidades para listar, False caso contrário.
        """
        if not self.__entidades:
            print(f"📭 Nenhum(a) {self.__tipo_entidade} cadastrado(a).")
            if mostrar_msg_voltar:
                 input("🔁 Pressione Enter para voltar ao menu...")
            return False
        else:
            print(f"\n--- Lista de {self.__tipo_entidade.capitalize()}s ---")
            ano_atual = date.today().year
            for entidade in self.__entidades:
                id_entidade = entidade.get('id', 'N/A')
                nome_entidade = entidade.get('nome', 'N/A')

                info_str = f"ID: {id_entidade} | Nome: {nome_entidade}"

                if self.__tipo_entidade == "membro":
                    funcao_entidade = entidade.get('funcao', '')
                    if funcao_entidade:
                        info_str += f" | Função: {funcao_entidade.capitalize()}"

                    ano_nascimento = entidade.get('ano_nascimento')
                    if ano_nascimento:
                        try:
                            idade = ano_atual - int(ano_nascimento)
                            info_str += f" | Idade: {idade} anos"
                        except ValueError:
                            info_str += f" | Ano Nasc.: {ano_nascimento} (inválido)"
                    else:
                        info_str += " | Idade: (Não informada)"

                elif self.__tipo_entidade == "categoria":
                    tipo_indicacao = entidade.get('tipo_indicacao', '')
                    if tipo_indicacao:
                        info_str += f" | Tipo de Indicação: {tipo_indicacao.capitalize()}"

                print(info_str)
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