# Controladores/ControladorIndicacao.py
from Limites.TelaIndicacao import TelaIndicacao
from Utils.validadores import le_num_inteiro

class ControladorIndicacao:
    def __init__(self, controlador_membros, controlador_categorias):
        self.__tela = TelaIndicacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__indicacoes = []

    def iniciar_indicacao(self):
        membro_id = self.__tela.pegar_id_membro()
        if not self.__controlador_membros.existe_id(membro_id):
            print("❌ Membro não encontrado.")
            return

        tipo = self.__tela.pegar_tipo_indicacao()
        categoria = self.__tela.pegar_categoria(self.__controlador_categorias.listar_categorias())
        dados = self.__tela.pegar_dados_indicacao(tipo)

        self.__indicacoes.append({
            "tipo": tipo,
            "categoria": categoria,
            "dados": dados,
            "membro_id": membro_id
        })
        print("✅ Indicação registrada com sucesso!")