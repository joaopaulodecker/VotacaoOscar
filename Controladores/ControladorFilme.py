from Limites.TelaFilme import TelaFilme
from Entidades.Filme import Filme

class ControladorFilme:

  def __init__(self, controlador_sistema):
    self.__filmes = []
    self.__tela_filme = TelaFilme()
    self.__controlador_sistema = controlador_sistema

  def pega_filme_por_titulo(self, titulo: str):
    for filme in self.__filmes:
      if filme.titulo == titulo:
        return filme
    return None

  def incluir_filme(self):
    dados = self.__tela_filme.pega_dados_filme()
    filme_existente = self.pega_filme_por_titulo(dados["titulo"])
    if filme_existente:
      self.__tela_filme.mostra_mensagem("ATENÇÃO: Filme já cadastrado.")
      return
    filme = Filme(dados["titulo"], dados["ano"], dados["diretor"], dados["nacionalidade"])
    self.__filmes.append(filme)
    self.__tela_filme.mostra_mensagem("Filme cadastrado com sucesso!")

  def alterar_filme(self):
    self.lista_filmes()
    titulo = self.__tela_filme.seleciona_filme()
    filme = self.pega_filme_por_titulo(titulo)
    if filme:
      novos_dados = self.__tela_filme.pega_dados_filme()
      filme.titulo = novos_dados["titulo"]
      filme.ano = novos_dados["ano"]
      filme.diretor = novos_dados["diretor"]
      filme.nacionalidade = novos_dados["nacionalidade"]
      self.__tela_filme.mostra_mensagem("Filme alterado com sucesso!")
    else:
      self.__tela_filme.mostra_mensagem("ATENÇÃO: Filme não encontrado.")

  def excluir_filme(self):
    self.lista_filmes()
    titulo = self.__tela_filme.seleciona_filme()
    filme = self.pega_filme_por_titulo(titulo)
    if filme:
      self.__filmes.remove(filme)
      self.__tela_filme.mostra_mensagem("Filme removido com sucesso!")
    else:
      self.__tela_filme.mostra_mensagem("ATENÇÃO: Filme não encontrado.")

  def lista_filmes(self):
      if not self.__filmes:
          self.__tela_filme.mostra_mensagem("Nenhum filme cadastrado.")
          return
      for filme in self.__filmes:
          self.__tela_filme.mostra_filme({
              "titulo": filme.titulo,
              "ano": filme.ano,
              "diretor": filme.diretor,
              "nacionalidade": filme.nacionalidade
          })

  def retornar(self):
      self.__controlador_sistema.abre_tela()

  def abre_tela(self):
      opcoes = {
          1: self.incluir_filme,
          2: self.alterar_filme,
          3: self.lista_filmes,
          4: self.excluir_filme,
          0: self.retornar
      }

      while True:
          escolha = self.__tela_filme.tela_opcoes()
          funcao_escolhida = opcoes.get(escolha)
          if funcao_escolhida:
              funcao_escolhida()
          else:
              self.__tela_filme.mostra_mensagem("Opção inválida.")
      # Loop principal do menu da tela: exibe opções, executa a função escolhida ou mostra erro

