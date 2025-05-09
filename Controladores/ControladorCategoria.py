from Entidades.Categoria import Categoria
from Limites.TelaCategoria import TelaCategoria
from Entidades.Voto import Voto
from Entidades.IndicacaoAbstract import Indicacao
from Entidades.IndAtor import IndAtor
from Entidades.IndFilme import IndFilme
from Entidades.IndDiretor import IndDiretor

class ControladorCategoria:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_categoria = TelaCategoria()
        self.__categorias = categorias




    def get_categoria_por_nome(self, nome):
        for categoria in self.__categorias:
            if categoria.nome == nome:
                return categoria
        return None

    def incluir_categoria(self):
        dados = self.__tela_categoria.pega_dados_categoria()
        if not self.get_categoria_por_nome(dados["nome"]):
            categoria = Categoria(dados["nome"])
            self.__categorias.append(categoria)
            self.__tela_categoria.mostra_mensagem("Categoria adicionada com sucesso!")
        else:
            self.__tela_categoria.mostra_mensagem("Categoria já registrada.")
        pass

    def remover_categoria(self):
        self.listar()
        nome = self.__tela_categoria.pega_dados_categoria()

        if nome is not None:
            self.__categorias.pop(nome)
            self.listar()
            self.__tela_categoria.mostra_mensagem("Categoria removida com sucesso!")

        else:
            self.__tela_categoria.mostra_mensagem("ATENÇÃO: Categoria não cadastrada.")


    def alterar_categoria(self):
        self.listar()
        nome = input("Digite o nome da categoria que deseja alterar: ")
        categoria = self.get_categoria_por_nome(nome)

        if categoria:
            nova_categoria = self.__tela_categoria.pega_dados_categoria()
            categoria.nome = nova_categoria["nome"]
            self.__tela_categoria.mostra_mensagem("Categoria alterada com sucesso!")

        else:
            self.__tela_categoria.mostra_mensagem("ATENÇÃO: Categoria não cadastrada.")

    def pega_categoria_por_nome(self, nome):
        for categoria in self.__categorias:
            if categoria.nome == nome:
                return categoria
        return None

    def quant_categoria_votos(self):
        nome = input("Digite o nome da categoria que deseja alterar: ")
        categoria = self.get_categoria_por_nome(nome)

        if not categoria:
            self.__tela_categoria.mostra_mensagem("ATENÇÃO: Categoria não cadastrada.")
            return

        total_votos = Categoria.total_de_votos(categoria)

        return total_votos
         #ver quantos votos tem a cat, entrelaço com Indicacao e Voto?

    def quant_categoria_indicacao(self):
        nome = input("Digite o nome da categoria que deseja alterar: ")
        categoria = self.get_categoria_por_nome(nome)

        if not categoria:
            self.__tela_categoria.mostra_mensagem("ATENÇÃO: Categoria não cadastrada.")
            return

        total_ind = Categoria.total_de_indicacoes(categoria)

        return total_ind

    def listar(self):
        if not self.__categorias:
            self.__tela_categoria.mostra_mensagem("Nenhuma categoria cadastrada.")
            return

        for cat in self.__categorias:
            self.__tela_categoria.mostra_mensagem(f"Nome: {cat.nome}")


    def retornar(self):
        pass

    def abre_tela(self):
        pass




