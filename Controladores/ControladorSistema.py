from Controladores.ControladorIndicacao import ControladorIndicacao
from Controladores.ControladorFilme import ControladorFilme
from Controladores.ControladorCategoria import Categoria, ControladorCategoria
from Controladores.ControladorMembroAcademia import ControladorMembroAcademia
from Controladores.ControladorVotacao import ControladorVotacao
from Entidades.MembroAcademia import MembroAcademia
from Limites.TelaSistema import TelaSistema


class ControladorSistema:
    def __init__(self):
        self.__categorias = {
            "ator": Categoria("ator"),
            "diretor": Categoria("diretor"),
            "filme": Categoria("filme")
        }
        self.__membro_logado = membro_logado
        self.__controlador_indicacao = controlador_indicacao
        self.controlador_categoria = ControladorCategoria(self.__controlador_indicacao, self.__categorias)
        self.__tela_sistema = TelaSistema

    def set_membro_logado(self, membro):
        self.__membro_logado = membro
        self.__controlador_indicacao = ControladorIndicacao(self.__categorias, self.__membro_logado)

    @property
    def controlador_indicacao(self):
        return self.__controlador_indicacao

    def listar_indicacoes(self):
        pass

    def retornar(self):
        pass

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {1: self.set_membro_logado(input("Digite seu nome como Membro da Academia:")), 2: self.listar_indicacoes(), 3: self.retornar(),
                        0: self.encerra_sistema}


        # while True:
        #     opcao_escolhida = self.__tela_sistema.listar opcoes
        #     funcao_escolhida = lista_opcoes[opcao_escolhida]
        #     funcao_escolhida()