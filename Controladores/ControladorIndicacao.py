from Entidades.Categoria import Categoria
from Entidades.IndAtor import IndAtor
from Entidades.IndDiretor import IndDiretor
from Entidades.IndFilme import IndFilme
from Limites.TelaIndicacao import TelaIndicacao
from DAOs.IndicacaoDao import IndicacaoDAO

class ControladorIndicacao:

    def __init__(self, controlador_sistema, controlador_membros,
                 controlador_categorias, controlador_filmes):
        self.__controlador_sistema = controlador_sistema
        self.__tela_indicacao = TelaIndicacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__controlador_filmes = controlador_filmes
        self.__dao = IndicacaoDAO()

    @staticmethod
    def _criar_objeto_indicacao(id_ind, cat_obj, item_obj_final):
        """Cria a instância correta da classe de indicação a partir dos dados da tela."""
        tipo_original = item_obj_final.get('tipo_original_indicado')
        objeto_completo = item_obj_final.get('objeto_completo')

        if tipo_original == 'filme':
            return IndFilme(id_indicacao=id_ind, categoria=cat_obj, filme_indicado=objeto_completo)
        elif tipo_original == 'ator':
            return IndAtor(id_indicacao=id_ind, categoria=cat_obj, ator_indicado=objeto_completo)
        elif tipo_original == 'diretor':
            return IndDiretor(id_indicacao=id_ind, categoria=cat_obj, diretor_indicado=objeto_completo)
        return None

    def abrir_menu_indicacoes(self):
        """Abre e gerencia a janela principal de indicações."""
        self.__tela_indicacao.init_components(self.__dao.get_all())

        while True:
            event, values = self.__tela_indicacao.open()

            if event in (None, '-VOLTAR-'):
                break

            if event == '-ADICIONAR-':
                self.iniciar_processo_indicacao()

            elif values.get('-TABELA-'):  # .get() é mais seguro
                index_selecionado = values['-TABELA-'][0]
                indicacao_selecionada = self.__dao.get_all()[index_selecionado]

                if event == '-EXCLUIR-':
                    self.excluir_indicacao(indicacao_selecionada)

            elif event == '-EXCLUIR-':
                TelaIndicacao.show_message("Aviso", "Por favor, selecione uma indicação na tabela primeiro.")

        self.__tela_indicacao.close()

    def iniciar_processo_indicacao(self):
        """Conduz o fluxo de registrar uma nova indicação com a tela gráfica."""
        if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_INDICACOES_ABERTAS:
            TelaIndicacao.show_message("Aviso", "O período de indicações já foi encerrado.")
            return

        #1: Pedir a categoria para a tela
        categorias = self.__controlador_categorias.entidades
        dados_da_tela = self.__tela_indicacao.pega_dados_indicacao(categorias)

        if dados_da_tela is None or dados_da_tela.get("acao") != "BUSCAR_FINALISTAS":
            return

        categoria_obj = dados_da_tela.get("categoria_obj")

        #2: Buscar finalistas e chamar a segunda parte da tela
        finalistas = self.get_finalistas_para_indicacao(categoria_obj)
        if not finalistas:
            TelaIndicacao.show_message("Aviso",
                                       f"Não há {categoria_obj.tipo_indicacao}(s) cadastrados para indicar nesta categoria.")
            return

        dados_finais = self.__tela_indicacao.preenche_lista_finalistas(finalistas, categoria_obj)

        if dados_finais and dados_finais.get("acao") == "SALVAR_INDICACAO":
            item_obj_final = dados_finais.get("indicado_obj")

            all_ids = [ind.id_indicacao for ind in self.__dao.get_all()]
            proximo_id = max(all_ids) + 1 if all_ids else 1

            nova_indicacao = self._criar_objeto_indicacao(proximo_id, categoria_obj, item_obj_final)

            if nova_indicacao:
                self.__dao.add(proximo_id, nova_indicacao)
                TelaIndicacao.show_message("Sucesso", "✅ Indicação registrada com sucesso!")
                self.__tela_indicacao.refresh_table(self.__dao.get_all())
            else:
                TelaIndicacao.show_message("Erro", "Falha ao criar o objeto de indicação.")

    def get_finalistas_para_indicacao(self, categoria_obj: Categoria) -> list:
        """Busca a lista de filmes ou membros e formata para a tela de seleção."""
        tipo_item = categoria_obj.tipo_indicacao
        lista_formatada = []
        lista_crua = []

        if tipo_item == "filme":
            lista_crua = self.__controlador_filmes.filmes
        elif tipo_item == "ator":
            genero_alvo = "Atriz" if "atriz" in categoria_obj.nome.lower() else "Ator"
            lista_crua = self.__controlador_membros.buscar_por_funcao_e_genero("ator", genero_alvo)
        elif tipo_item == "diretor":
            lista_crua = self.__controlador_membros.buscar_por_funcao_e_genero("diretor")

        for item in lista_crua:
            nome = item.titulo if tipo_item == 'filme' else item.nome
            lista_formatada.append({
                "nome_display": nome,
                "objeto_completo": item,
                "tipo_original_indicado": tipo_item
            })
        return lista_formatada

    def excluir_indicacao(self, indicacao_alvo):
        """Exclui uma indicação que foi selecionada na tabela."""
        if self.__controlador_sistema.fase_atual_premiacao != self.__controlador_sistema.FASE_INDICACOES_ABERTAS:
            TelaIndicacao.show_message("Aviso", "Não é possível excluir indicações após o início da votação.")
            return

        if indicacao_alvo:
            info = indicacao_alvo.obter_detalhes_item_indicado()
            confirmado = TelaIndicacao.show_confirm_message(
                "Confirmar Exclusão",
                f"Tem certeza que deseja excluir a indicação para '{info}'?"
            )
            if confirmado == 'Yes':
                self.__dao.remove(indicacao_alvo.id_indicacao)
                TelaIndicacao.show_message("Sucesso", "🗑️ Indicação removida com sucesso!")
                self.__tela_indicacao.refresh_table(self.__dao.get_all())
