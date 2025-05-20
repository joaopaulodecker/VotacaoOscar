from Limites.TelaVotacao import TelaVotacao
from Utils.validadores import le_num_inteiro
from collections import Counter

class ControladorVotacao:
    def __init__(self, controlador_membros, controlador_categorias):  # Adicione estes parâmetros
        self.__tela = TelaVotacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__votos = []

    def iniciar_votacao(self):
        membro_id = self.__tela.pegar_id_membro()
        if not self.__controlador_membros.existe_id(membro_id):
            print("❌ Membro não encontrado.")
            input("🔁 Pressione Enter para continuar...")
            return

        tipo = self.__tela.pegar_tipo_voto()
        categoria = self.__tela.pegar_categoria(self.__controlador_categorias.listar_categorias())

        if not categoria:
            print("⚠️ Votação cancelada.")
            input("🔁 Pressione Enter para continuar...")
            return

        # Verificação de voto duplicado
        for voto in self.__votos:
            if voto["membro_id"] == membro_id and voto["categoria"] == categoria["nome"]:
                print("⚠️ Este membro já votou nesta categoria.")
                input("🔁 Pressione Enter para continuar...")
                return

        indicados = self.__listar_indicados_fake(tipo, categoria)
        escolhido = self.__tela.selecionar_indicado(indicados)

        if not escolhido:
            print("⚠️ Votação cancelada.")
            input("🔁 Pressione Enter para continuar...")
            return

        self.__votos.append({
            "membro_id": membro_id,
            "categoria": categoria["nome"],
            "tipo": tipo,
            "escolhido": escolhido["nome"]
        })
        print("✅ Voto registrado com sucesso!")
        input("🔁 Pressione Enter para continuar...")

    def mostrar_resultados(self):
        if not self.__votos:
            print("📭 Nenhum voto registrado.")
        else:
            contagem = Counter(v["escolhido"] for v in self.__votos)
            resultados = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
            print("\n🏆 Resultados:")
            for nome, votos in resultados:
                print(f"{nome}: {votos} voto(s)")
        input("🔁 Pressione Enter para voltar ao menu...")