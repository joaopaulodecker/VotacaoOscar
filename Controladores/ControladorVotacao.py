from Limites.TelaVotacao import TelaVotacao
from Utils.validadores import le_num_inteiro
from collections import Counter

class ControladorVotacao:
    def __init__(self, controlador_membros, controlador_categorias):
        self.__tela = TelaVotacao()
        self.__controlador_membros = controlador_membros
        self.__controlador_categorias = controlador_categorias
        self.__votos = []

    def iniciar_votacao(self):
        membro_id = self.__tela.pegar_id_membro()
        if not self.__controlador_membros.existe_id(membro_id):
            print("❌ Membro não encontrado.")
            return

        tipo = self.__tela.pegar_tipo_voto()
        categoria = self.__tela.pegar_categoria(self.__controlador_categorias.listar_categorias())

        if not categoria:
            print("⚠️ Votação cancelada: nenhuma categoria disponível.")
            return

        indicados = self.__listar_indicados_fake(tipo, categoria)
        escolhido = self.__tela.selecionar_indicado(indicados)

        self.__votos.append({
            "membro_id": membro_id,
            "categoria": categoria["nome"],
            "tipo": tipo,
            "escolhido": escolhido["nome"]
        })
        print("✅ Voto registrado com sucesso!")

    def __listar_indicados_fake(self, tipo, categoria):
        # Simulação de indicados por tipo e categoria
        return [
            {"id": 1, "nome": f"{tipo.title()} Exemplo 1"},
            {"id": 2, "nome": f"{tipo.title()} Exemplo 2"},
            {"id": 3, "nome": f"{tipo.title()} Exemplo 3"}
        ]

    def mostrar_resultados(self):
        if not self.__votos:
            print("📭 Nenhum voto registrado.")
            return

        contagem = Counter(v["escolhido"] for v in self.__votos)
        resultados = [{"nome": nome, "votos": qtd} for nome, qtd in contagem.items()]
        resultados.sort(key=lambda x: x["votos"], reverse=True)
        self.__tela.exibir_resultados(resultados)