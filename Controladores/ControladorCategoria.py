from Controladores.ControladorCadastro import ControladorCadastro
from Limites.TelaCategoria import TelaCategoria

class ControladorCategorias(ControladorCadastro):
    def __init__(self):
        super().__init__("categoria")
        self.__tela_categoria = TelaCategoria()  # Tela específica
        self.__proximo_id = 1  # Auto-incremento


    def pegar_dados(self):
        """Usa TelaCategoria e gera ID automaticamente"""
        dados = self.__tela_categoria.pega_dados_categoria()
        return {
            "id": self.__proximo_id,
            "nome": dados["nome"]
        }

    def cadastrar(self):
        """Versão customizada com com UX personalizado"""
        dados = self.pegar_dados()
        if dados:
            self.entidades.append(dados)
            self.__proximo_id += 1
            print(f"✅ Categoria '{dados['nome']}' cadastrada com sucesso!")
            input("🔁 Pressione Enter para continuar...")

    def listar(self, mostrar_msg_voltar=False):
        if not self.entidades:
            print("📭 Nenhuma categoria cadastrada.")
        else:
            print("\n🏆 Categorias Disponíveis:")
            for cat in self.entidades:
                print(f"ID: {cat['id']} | Nome: {cat['nome']}")
        if mostrar_msg_voltar:
            input("🔁 Pressione Enter para voltar ao menu...")
        return self.entidades

    def listar_categorias(self, *args, **kwargs):
        return self.listar(*args, **kwargs)