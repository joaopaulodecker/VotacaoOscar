from Excecoes.OpcaoInvalida import OpcaoInvalida
from Utils.validadores import le_num_inteiro
from Entidades.Nacionalidade import Nacionalidade

class TelaFilmes:
    def mostra_opcoes(self):
        print("\n----- FILMES -----")
        print("1 - Cadastrar Filme")
        print("2 - Alterar Filme")
        print("3 - Excluir Filme")
        print("4 - Listar Filmes")
        print("0 - Voltar")

        while True:
            opcao_str = input("Escolha a opção: ").strip()
            if opcao_str.isdigit():
                valor = int(opcao_str)
                if 0 <= valor <= 4:
                    return valor
            raise OpcaoInvalida("Opção de menu de filmes inválida. Escolha entre 0 e 4.")

    def le_dados_filme(self, dados_atuais=None, diretores_disponiveis=None):
        print("\n--- Dados do Filme ---")
        dados_coletados = {}

        if dados_atuais:
            print(f"(Deixe em branco para manter o valor atual: '{dados_atuais.get('titulo', '')}')")
            titulo_input = input("Novo Título do filme: ").strip()
            dados_coletados["titulo"] = titulo_input if titulo_input else dados_atuais.get("titulo")
        else:
            dados_coletados["titulo"] = input("Título do filme: ").strip()

        if dados_coletados.get("titulo") is not None and isinstance(dados_coletados.get("titulo"), str):
            dados_coletados["titulo"] = dados_coletados["titulo"].title()

        if not dados_coletados.get("titulo"):
            print("❌ Título não pode ser vazio.")
            return None

        ano_str = ""
        if dados_atuais:
            print(f"(Deixe em branco para manter o valor atual: '{dados_atuais.get('ano', '')}')")
            ano_input = input("Novo Ano de lançamento: ").strip()
            ano_str = ano_input if ano_input else str(dados_atuais.get("ano", ""))
        else:
            ano_str = input("Ano de lançamento: ").strip()

        if not ano_str:
            print("❌ Ano não pode ser vazio.")
            return None

        try:
            ano = int(ano_str)
            if ano <= 0:
                print("❌ Ano deve ser um número positivo.")
                return None
            dados_coletados["ano"] = ano
        except ValueError:
            print("❌ Ano inválido. Deve ser um número inteiro.")
            return None

        nacionalidade_obj_final = None
        nacionalidade_prompt = "Nacionalidade do Filme (país)"
        current_nacionalidade_pais = ""

        if dados_atuais and dados_atuais.get('nacionalidade') is not None:
            if isinstance(dados_atuais.get('nacionalidade'), Nacionalidade):
                current_nacionalidade_pais = dados_atuais.get('nacionalidade').pais
                nacionalidade_prompt += f" (atual: {current_nacionalidade_pais})"
        nacionalidade_prompt += ": "

        if dados_atuais:
            pais_input_str = input(nacionalidade_prompt).strip()
            if not pais_input_str:
                nacionalidade_obj_final = dados_atuais.get('nacionalidade')
            else:
                if not pais_input_str.replace(" ", "").isalpha():
                    print("❌ Nacionalidade (país) deve conter apenas letras e espaços. Mantendo anterior se houver.")
                    nacionalidade_obj_final = dados_atuais.get('nacionalidade')
                else:
                    nacionalidade_obj_final = Nacionalidade(pais_input_str.title())
        else:
            pais_input_str = ""
            while True:
                pais_input_str = input(nacionalidade_prompt).strip()
                if not pais_input_str:
                    print("❌ Nacionalidade (país) é obrigatória. Tente novamente.")
                elif not pais_input_str.replace(" ", "").isalpha():
                    print("❌ Nacionalidade (país) deve conter apenas letras e espaços. Tente novamente.")
                else:
                    break 
            nacionalidade_obj_final = Nacionalidade(pais_input_str.title())
        
        dados_coletados["nacionalidade_obj"] = nacionalidade_obj_final
        if dados_coletados.get("nacionalidade_obj") is None and not dados_atuais:
             print("❌ Nacionalidade deve ser fornecida para o novo filme.")
             return None

        selected_diretor_id = None
        if diretores_disponiveis and len(diretores_disponiveis) > 0:
            print("\n--- Diretor do Filme ---")
            for i, diretor_dict in enumerate(diretores_disponiveis):
                print(f"  {i+1} - {diretor_dict.get('nome', 'Nome Indisponível')} (ID: {diretor_dict.get('id', 'N/A')})")
            
            prompt_diretor_base = f"Escolha o número do diretor (1-{len(diretores_disponiveis)})"
            
            if dados_atuais:
                current_diretor_info = ""
                if dados_atuais.get('diretor_id') is not None:
                    current_dir_id = dados_atuais.get('diretor_id')
                    diretor_encontrado_na_lista = False
                    for i, d_dict in enumerate(diretores_disponiveis):
                        if d_dict.get('id') == current_dir_id:
                            current_diretor_info = f" (atual: {i+1} - {d_dict.get('nome', 'N/A')})"
                            diretor_encontrado_na_lista = True
                            break
                    if not diretor_encontrado_na_lista:
                         current_diretor_info = f" (ID Diretor atual: {current_dir_id} - não está na lista)"
                
                prompt_diretor_final = prompt_diretor_base + current_diretor_info
                print(prompt_diretor_final)
                escolha_str = input("Digite o novo número ou deixe em branco para manter: ").strip()

                if not escolha_str:
                    selected_diretor_id = dados_atuais.get('diretor_id')
                else:
                    if escolha_str.isdigit():
                        escolha_num = int(escolha_str)
                        if 1 <= escolha_num <= len(diretores_disponiveis):
                            selected_diretor_id = diretores_disponiveis[escolha_num - 1].get('id')
                        else:
                            print(f"❌ Número fora do intervalo. Mantendo diretor original se houver (ID: {dados_atuais.get('diretor_id')}).")
                            selected_diretor_id = dados_atuais.get('diretor_id')
                    else:
                        print("❌ Entrada inválida para número do diretor. Mantendo diretor original se houver.")
                        selected_diretor_id = dados_atuais.get('diretor_id')
            else: 
                prompt_diretor_final = prompt_diretor_base + ": "
                escolha_num_diretor = le_num_inteiro(prompt_diretor_final, 
                                                     min_val=1, 
                                                     max_val=len(diretores_disponiveis))
                if escolha_num_diretor is not None:
                    selected_diretor_id = diretores_disponiveis[escolha_num_diretor - 1].get('id')
                else:
                    print("❌ Seleção de diretor obrigatória falhou ou foi cancelada.")
                    return None
        elif not dados_atuais: 
            print("❌ Não há diretores cadastrados para selecionar. Cadastre diretores primeiro.")
            return None 
        elif dados_atuais: 
            selected_diretor_id = dados_atuais.get('diretor_id')
        
        dados_coletados["diretor_id"] = selected_diretor_id
        
        if dados_coletados.get("diretor_id") is None and not dados_atuais :
             print("❌ Um diretor deve ser selecionado para o novo filme.")
             return None

        return dados_coletados

    def seleciona_filme_por_id(self, mensagem="Digite o ID do filme: "):
        while True:
            id_str = input(mensagem).strip()
            if not id_str:
                return None
            if id_str.isdigit():
                return int(id_str)
            print("❌ ID inválido. Por favor, digite um número.")

    def confirma_exclusao(self, titulo_filme):
        while True:
            confirmacao = input(f"Tem certeza que deseja excluir o filme '{titulo_filme}'? (S/N): ").strip().upper()
            if confirmacao == 'S':
                return True
            elif confirmacao == 'N':
                return False
            print("❌ Opção inválida. Digite S para Sim ou N para Não.")

    def mostra_detalhes_filme(self, filme, nome_diretor: str | None = None):
        print(f"   ID: {filme.id_filme}")
        print(f"   Título: {filme.titulo}")
        print(f"   Ano: {filme.ano}")
        
        nacionalidade_str = "Não especificada"
        if filme.nacionalidade and hasattr(filme.nacionalidade, 'pais'):
            nacionalidade_str = filme.nacionalidade.pais
        print(f"   Nacionalidade: {nacionalidade_str}")
        if nome_diretor:
            print(f"   Diretor: {nome_diretor}")
        elif filme.diretor_id is not None:
            print(f"   Diretor ID: {filme.diretor_id}")
        else:
            print("   Diretor: Não especificado")