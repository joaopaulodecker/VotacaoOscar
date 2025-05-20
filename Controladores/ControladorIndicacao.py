# Controladores/ControladorIndicacao.py
from Limites.TelaIndicacao import TelaIndicacao
from Utils.validadores import le_num_inteiro


class ControladorIndicacao:

    def __init__(self, controlador_membros, controlador_categorias):  # Adicione estes parâmetros
        self.__tela = TelaIndicacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__indicacoes = []

    def iniciar_indicacao(self):
        membro_id = self.__tela.pegar_id_membro()
        if not self.__controlador_membros.existe_id(membro_id):
            print("❌ Membro não encontrado.")
            input("🔁 Pressione Enter para continuar...")
            return

        tipo = self.__tela.pegar_tipo_indicacao()
        categoria = self.__tela.pegar_categoria(self.__controlador_categorias.listar_categorias())

        if not categoria:
            print("⚠️ Indicação cancelada.")
            input("🔁 Pressione Enter para continuar...")
            return

        # Verificação de duplicidade
        for indicacao in self.__indicacoes:
            if (indicacao["membro_id"] == membro_id and
                    indicacao["tipo"] == tipo and
                    indicacao["categoria"]["nome"] == categoria["nome"]):
                print("⚠️ Você já indicou para essa categoria.")
                input("🔁 Pressione Enter para continuar...")
                return

        dados = self.__tela.pegar_dados_indicacao(tipo)
        if not dados:
            print("⚠️ Indicação cancelada.")
            input("🔁 Pressione Enter para continuar...")
            return

        self.__indicacoes.append({
            "tipo": tipo,
            "categoria": categoria,
            "dados": dados,
            "membro_id": membro_id
        })
        print("✅ Indicação registrada com sucesso!")
        input("🔁 Pressione Enter para continuar...")