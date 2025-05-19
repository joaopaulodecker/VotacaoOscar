class ControladorCategorias:
    def __init__(self):
        self.__categorias = []  # Exemplo: [{"id": 1, "nome": "Melhor Filme"}]

    def listar_categorias(self):
        return self.__categorias

    def adicionar_categoria(self, categoria):
        self.__categorias.append(categoria)

