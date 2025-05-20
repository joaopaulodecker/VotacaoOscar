from Utils.validadores import le_num_inteiro

class TelaVotacao:
    def pegar_id_membro(self):
        return le_num_inteiro("Informe o ID do membro da academia: ")

    def pegar_tipo_voto(self):
        print("\nVocê quer votar em:")
        print("1 - Filme")
        print("2 - Ator")
        print("3 - Diretor")
        opcao = le_num_inteiro("Escolha uma opção: ")
        if opcao == 1:
            return "filme"
        elif opcao == 2:
            return "ator"
        elif opcao == 3:
            return "diretor"
        else:
            print("❌ Tipo inválido. Padrão: Filme")
            return "filme"

    def pegar_categoria(self, categorias):
        if not categorias:
            print("⚠️ Nenhuma categoria disponível.")
            return None

        print("\nCategorias disponíveis:")
        for i, cat in enumerate(categorias):
            print(f"{i + 1} - {cat['nome']}")
        idx = le_num_inteiro("Escolha a categoria (número): ")
        if 1 <= idx <= len(categorias):
            return categorias[idx - 1]
        print("❌ Categoria inválida. Selecionando a primeira por padrão.")
        return categorias[0]

    def selecionar_indicado(self, indicados):
        print("\n🎬 INDICADOS DISPONÍVEIS:")
        print("-" * 40)
        for i, indicado in enumerate(indicados, start=1):
            print(f"{i}. {indicado['nome']}")
        print("-" * 40)

        idx = le_num_inteiro("🎯 Escolha seu voto (número): ")
        if 1 <= idx <= len(indicados):
            return indicados[idx - 1]

        print("❌ Voto inválido. Selecionando o primeiro por padrão.")
        return indicados[0]

    def exibir_resultados(self, resultados):
        print("\n🏆 RESULTADOS DA VOTAÇÃO 🏆")
        print("=" * 40)

        for i, resultado in enumerate(resultados, start=1):
            nome = resultado["nome"]
            votos = resultado["votos"]
            barra = "█" * votos  # Barrinha proporcional aos votos
            print(f"{i}. {nome:<25} | {votos:>2} voto(s) {barra}")

        print("=" * 40)
