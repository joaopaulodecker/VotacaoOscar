from Limites.TelaCadastro import TelaCadastro
from Excecoes.OpcaoInvalida import OpcaoInvalida
from datetime import date

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
                opcao = self.__tela.mostra_menu()
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
                self.__tela.mostra_mensagem(f"❌ {e}")
                self.__tela.espera_input()

    def cadastrar(self):
        dados = self.__tela.pegar_dados()
        if dados:
            dados["id"] = self._gerar_proximo_id()
            self.__entidades.append(dados)
            self.__tela.mostra_mensagem(
                f"✅ {self.__tipo_entidade.capitalize()} '{dados['nome']}' cadastrado(a) com sucesso! "
                f"(ID: {dados['id']})"
            )
        else:
            self.__tela.mostra_mensagem(f"ℹ️ Cadastro de {self.__tipo_entidade} cancelado.")
        self.__tela.espera_input()

    def alterar(self):
        self.listar()
        if not self.__entidades:
            return

        id_alvo = self.__tela.pegar_id(
            mensagem=f"Digite o ID do(a) {self.__tipo_entidade} que deseja alterar: "
        )
        if id_alvo is None:
            self.__tela.mostra_mensagem("ℹ️ Alteração cancelada.")
            self.__tela.espera_input()
            return

        entidade_encontrada = self.buscar_por_id(id_alvo)
        if entidade_encontrada:
            self.__tela.mostra_cabecalho_operacao("Alteração")
            novos_dados = self.__tela.pegar_dados(dados_atuais=entidade_encontrada)
            
            if novos_dados:
                entidade_encontrada.update(novos_dados)
                self.__tela.mostra_mensagem("✅ Alteração realizada com sucesso!")
            else:
                self.__tela.mostra_mensagem("ℹ️ Nenhuma alteração realizada.")
        else:
            self.__tela.mostra_mensagem(
                f"❌ {self.__tipo_entidade.capitalize()} com ID {id_alvo} não encontrado."
            )
        self.__tela.espera_input()

    def excluir(self):
        self.listar()
        if not self.__entidades:
            return
            
        id_alvo = self.__tela.pegar_id(
            mensagem=f"Digite o ID do(a) {self.__tipo_entidade} que deseja excluir: "
        )
        if id_alvo is None:
            self.__tela.mostra_mensagem("ℹ️ Exclusão cancelada.")
            self.__tela.espera_input()
            return

        entidade_para_excluir = self.buscar_por_id(id_alvo)
        
        if entidade_para_excluir:
            self.__entidades.remove(entidade_para_excluir)
            self.__tela.mostra_mensagem("🗑️ Registro excluído com sucesso!")
        else:
            self.__tela.mostra_mensagem(
                f"❌ {self.__tipo_entidade.capitalize()} com ID {id_alvo} não encontrado."
            )
        self.__tela.espera_input()
    
    def _preparar_dados_para_tela(self, entidade: dict) -> dict:
        info_str = f"ID: {entidade.get('id')} | Nome: {entidade.get('nome')}"

        if self.__tipo_entidade == "membro":
            if entidade.get('funcao'):
                info_str += f" | Função: {entidade['funcao'].capitalize()}"
            
            ano_nasc = entidade.get('ano_nascimento')
            if ano_nasc:
                try:
                    idade = date.today().year - int(ano_nasc)
                    info_str += f" | Idade: {idade} anos"
                except (ValueError, TypeError):
                    pass
        
        return {"info_str": info_str}

    def listar(self, mostrar_msg_voltar=False):
        if not self.__entidades:
            self.__tela.mostra_lista_entidades([])
        else:
            lista_para_tela = [self._preparar_dados_para_tela(ent) for ent in self.__entidades]
            self.__tela.mostra_lista_entidades(lista_para_tela)
        
        if mostrar_msg_voltar:
            self.__tela.espera_input()
        
        return bool(self.__entidades)

    def buscar_por_id(self, id_busca):
        for entidade in self.__entidades:
            if entidade.get("id") == id_busca:
                return entidade
        return None

    def buscar_por_funcao(self, funcao_busca):
        return [ent for ent in self.__entidades if ent.get("funcao") == funcao_busca]
