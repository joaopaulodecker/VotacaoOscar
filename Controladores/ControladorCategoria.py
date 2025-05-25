from Entidades.Categoria import Categoria
from Limites.TelaCategoria import TelaCategoria
from Controladores.ControladorCadastro import ControladorCadastro

class ControladorCategorias(ControladorCadastro):
    def __init__(self):
        super().__init__("categoria")
        self.__tela_categoria = TelaCategoria()
        self.__proximo_id = 1

    def _gerar_proximo_id(self):
        id_atual = self.__proximo_id
        self.__proximo_id += 1
        return id_atual

    def _buscar_categoria_por_id(self, id_categoria: int):
        for categoria in self.entidades:
            if isinstance(categoria, Categoria) and categoria.id == id_categoria:
                return categoria
        return None

    def _existe_nome_categoria(self, nome: str, id_excluir: int = None):
        for categoria in self.entidades:
            if isinstance(categoria, Categoria):
                if categoria.id == id_excluir:
                    continue
                if categoria.nome.casefold() == nome.casefold():
                    return True
        return False

    def cadastrar(self):
        print("\n--- Cadastro de Nova Categoria ---")
        dados_tela = self.__tela_categoria.pega_dados_categoria()

        if not dados_tela or not dados_tela.get("nome"):
            print("❌ Nome da categoria não pode ser vazio.")
            input("🔁 Pressione Enter para continuar...")
            return

        nome_categoria = dados_tela["nome"].title()
        if self._existe_nome_categoria(nome_categoria):
            print(f"❌ Já existe uma categoria com o nome '{nome_categoria}'.")
            input("🔁 Pressione Enter para continuar...")
            return

        tipo_str = ""
        while True:
            tipo_str = input(f"O que será indicado nesta categoria? ({'/'.join(Categoria.TIPOS_VALIDOS)}): ").strip().lower()
            if tipo_str in Categoria.TIPOS_VALIDOS:
                break
            else:
                print(f"❌ Tipo inválido! Use: {', '.join(Categoria.TIPOS_VALIDOS)}.")
        
        novo_id = self._gerar_proximo_id()
        nova_categoria = Categoria(id_categoria=novo_id, nome=nome_categoria, tipo_indicacao=tipo_str)
        self.entidades.append(nova_categoria) 
        print(f"✅ Categoria ID {nova_categoria.id} - '{nova_categoria.nome}' (Tipo: {nova_categoria.tipo_indicacao.capitalize()}) cadastrada com sucesso!")
        input("🔁 Pressione Enter para continuar...")

    def listar(self, mostrar_msg_voltar: bool = False):
        if not self.entidades:
            print("📭 Nenhuma categoria cadastrada.")
            if mostrar_msg_voltar:
                input("🔁 Pressione Enter para voltar ao menu...")
            return False

        print("\n--- Lista de Categorias Cadastradas ---")
        for categoria_obj in self.entidades:
            if isinstance(categoria_obj, Categoria):
                print(f"ID: {categoria_obj.id} | Nome: {categoria_obj.nome.title()} | Tipo para Indicação: {categoria_obj.tipo_indicacao.capitalize()}")
            else:
                print(f"  Item inesperado na lista: {str(categoria_obj)}")
        
        print("------------------------------------")
        if mostrar_msg_voltar:
            input("\n🔁 Pressione Enter para voltar ao menu...")
        return True

    def alterar(self):
        print("\n--- Alteração de Categoria ---")
        if not self.listar():
            return

        try:
            id_alvo_str = self.__tela_categoria.seleciona_categoria_por_id(mensagem="Digite o ID da categoria que deseja alterar: ")
            if id_alvo_str is None:
                print("ℹ️ Alteração cancelada.")
                input("🔁 Pressione Enter para continuar...")
                return
            id_alvo = int(id_alvo_str)
        except ValueError:
            print("❌ ID inválido. Deve ser um número.")
            input("🔁 Pressione Enter para continuar...")
            return

        categoria_alvo = self._buscar_categoria_por_id(id_alvo)

        if not categoria_alvo:
            print(f"❌ Categoria com ID {id_alvo} não encontrada.")
            input("🔁 Pressione Enter para continuar...")
            return

        print(f"\nEditando categoria: ID {categoria_alvo.id} - '{categoria_alvo.nome}' (Tipo atual: {categoria_alvo.tipo_indicacao.capitalize()})")
        novos_dados_tela = self.__tela_categoria.pega_dados_categoria(dados_atuais={"nome": categoria_alvo.nome, "tipo_indicacao": categoria_alvo.tipo_indicacao})


        if not novos_dados_tela or not novos_dados_tela.get("nome"):
            print("❌ Nome da categoria não pode ser vazio para alteração.")
            input("🔁 Pressione Enter para continuar...")
            return
        
        novo_nome = novos_dados_tela["nome"].title()
        if categoria_alvo.nome.casefold() != novo_nome.casefold() and self._existe_nome_categoria(novo_nome, id_excluir=categoria_alvo.id):
            print(f"❌ Já existe outra categoria com o nome '{novo_nome}'.")
            input("🔁 Pressione Enter para continuar...")
            return

        categoria_alvo.nome = novo_nome
        print(f"✅ Categoria ID {categoria_alvo.id} - '{categoria_alvo.nome}' alterada com sucesso.")
        input("🔁 Pressione Enter para continuar...")

    def excluir(self):
        print("\n--- Exclusão de Categoria ---")
        if not self.listar():
            return

        try:
            id_alvo_str = self.__tela_categoria.seleciona_categoria_por_id(mensagem="Digite o ID da categoria que deseja excluir: ")
            if id_alvo_str is None:
                print("ℹ️ Exclusão cancelada.")
                input("🔁 Pressione Enter para continuar...")
                return
            id_alvo = int(id_alvo_str)
        except ValueError:
            print("❌ ID inválido. Deve ser um número.")
            input("🔁 Pressione Enter para continuar...")
            return

        categoria_alvo = self._buscar_categoria_por_id(id_alvo)

        if not categoria_alvo:
            print(f"❌ Categoria com ID {id_alvo} não encontrada.")
            input("🔁 Pressione Enter para continuar...")
            return
        
        self.entidades.remove(categoria_alvo)
        print(f"🗑️ Categoria ID {categoria_alvo.id} - '{categoria_alvo.nome}' removida com sucesso.")
        input("🔁 Pressione Enter para continuar...")