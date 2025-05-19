from Utils.validadores import le_num_inteiro, le_string_nao_vazia

class TelaIndicacao:
    def pegar_id_membro(self):
        return le_num_inteiro("Informe o ID do membro da academia: ")

    def pegar_tipo_indicacao(self):
        print("\nVocê quer indicar:")
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

    def pegar_dados_indicacao(self, tipo):
        if tipo == "filme":
            titulo = le_string_nao_vazia("Título do filme: ")
            return {"titulo": titulo}
        elif tipo == "ator":
            nome = le_string_nao_vazia("Nome do ator: ")
            return {"nome": nome}
        elif tipo == "diretor":
            nome = le_string_nao_vazia("Nome do diretor: ")
            return {"nome": nome}
        return {}