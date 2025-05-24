from Utils.validadores import le_num_inteiro, le_texto_alpha_espacos
from Excecoes.OpcaoInvalida import OpcaoInvalida
from datetime import date

class TelaCadastro:
    def __init__(self, tipo):
        self.__tipo = tipo

    def mostrar_menu(self):
        print(f"\n===== MENU {self.__tipo.upper()} =====")
        print("1 - Cadastrar")
        print("2 - Alterar")
        print("3 - Excluir")
        print("4 - Listar")
        print("0 - Voltar")

        opcao = le_num_inteiro("Escolha uma opção: ", min_val=0, max_val=4)
        if opcao is None:
            raise OpcaoInvalida("Entrada de opção inválida.")
        return opcao

    def pegar_dados(self, dados_atuais=None):
        if dados_atuais:
            print(f"\n--- Alteração de {self.__tipo.capitalize()} (ID: {dados_atuais.get('id', 'N/A')}) ---")
            print("Deixe o campo em branco para manter o valor atual (quando aplicável).")
        else:
            print(f"\n--- Cadastro de {self.__tipo.capitalize()} ---")
            print("(Deixe um campo obrigatório em branco para cancelar)")

        try:
            nome_prompt = "Nome"
            if dados_atuais and dados_atuais.get('nome') is not None:
                nome_prompt += f" (atual: {dados_atuais['nome']})"
            nome_prompt += ": "
            
            nome_input = le_texto_alpha_espacos(nome_prompt, permitir_vazio_cancela=True)
            nome_final = nome_input if nome_input is not None else dados_atuais.get('nome') if dados_atuais else None

            if nome_final is not None:
                nome_final = nome_final.title()

            if nome_final is None or not nome_final.strip():
                print("Nome é obrigatório e não pode ser vazio. Operação cancelada.")
                return None

            id_val = dados_atuais.get("id") if dados_atuais else None

            if self.__tipo == "categoria":
                retorno = {
                    "nome": nome_final
                }
                if id_val is not None:
                    retorno["id"] = id_val
                return retorno

            nacionalidade_prompt = "Nacionalidade"
            if dados_atuais and dados_atuais.get('nacionalidade') is not None:
                nacionalidade_prompt += f" (atual: {dados_atuais['nacionalidade']})"
            nacionalidade_prompt += ": "

            nacionalidade_input = le_texto_alpha_espacos(nacionalidade_prompt, permitir_vazio_cancela=True)
            nacionalidade_final = nacionalidade_input if nacionalidade_input is not None else dados_atuais.get(
                'nacionalidade') if dados_atuais else None

            if nacionalidade_final is not None:
                nacionalidade_final = nacionalidade_final.title()

            if nacionalidade_final is None or not nacionalidade_final.strip():
                print("Nacionalidade é obrigatória e não pode ser vazia. Operação cancelada.")
                return None

            if self.__tipo == "membro":
                ano_nascimento_final = None
                ano_nascimento_prompt = "Ano de Nascimento"
                min_ano_nasc = 1900
                max_ano_nasc = date.today().year

                if dados_atuais and dados_atuais.get('ano_nascimento') is not None:
                    ano_nascimento_prompt += f" (atual: {dados_atuais['ano_nascimento']})"
                ano_nascimento_prompt += ": "

                if dados_atuais:
                    ano_str_input = input(ano_nascimento_prompt).strip()
                    if not ano_str_input:
                        ano_nascimento_final = dados_atuais.get('ano_nascimento')
                    else:
                        try:
                            ano_val_input = int(ano_str_input)
                            if min_ano_nasc <= ano_val_input <= max_ano_nasc:
                                ano_nascimento_final = ano_val_input
                            else:
                                print(f"❌ Ano de nascimento fora do intervalo válido ({min_ano_nasc}-{max_ano_nasc}). Valor anterior mantido se existir.")
                                ano_nascimento_final = dados_atuais.get('ano_nascimento')
                        except ValueError:
                            print("❌ Ano de nascimento inválido. Deve ser um número. Valor anterior mantido se existir.")
                            ano_nascimento_final = dados_atuais.get('ano_nascimento')
                else:
                    ano_nascimento_final = le_num_inteiro(ano_nascimento_prompt, min_val=min_ano_nasc, max_val=max_ano_nasc)
                
                if ano_nascimento_final is None and not dados_atuais:
                    print("Ano de Nascimento é obrigatório para novo membro e deve ser válido. Operação cancelada.")
                    return None
                
                funcoes_permitidas = ["ator", "diretor", "jurado"]
                funcao_final = None

                print("\nFunção do membro:")
                for i, opt in enumerate(funcoes_permitidas):
                    print(f"  {i + 1} - {opt.capitalize()}")

                prompt_msg_funcao = f"Escolha o número da função (1-{len(funcoes_permitidas)})"
                current_funcao_display = ""
                if dados_atuais and dados_atuais.get('funcao'):
                    try:
                        current_funcao_lower = str(dados_atuais.get('funcao', '')).lower()
                        if current_funcao_lower in funcoes_permitidas:
                            current_funcao_index = funcoes_permitidas.index(current_funcao_lower)
                            current_funcao_display = f" (atual: {current_funcao_index + 1} - {str(dados_atuais.get('funcao')).capitalize()})"
                    except Exception:
                        pass
                prompt_msg_funcao += f"{current_funcao_display}: "

                while True:
                    escolha_str = input(prompt_msg_funcao).strip()
                    if dados_atuais and not escolha_str:
                        funcao_final = dados_atuais.get('funcao')
                        break
                    if not escolha_str and not dados_atuais:
                        funcao_final = None
                        break

                    if escolha_str.isdigit():
                        escolha_num = int(escolha_str)
                        if 1 <= escolha_num <= len(funcoes_permitidas):
                            funcao_final = funcoes_permitidas[escolha_num - 1]
                            break
                        else:
                            print(f"❌ Número fora do intervalo (1-{len(funcoes_permitidas)}). Tente novamente.")
                    else:
                        print("❌ Entrada inválida. Por favor, digite um número correspondente à opção.")

                if funcao_final is None or not funcao_final.strip():
                    print("Função é obrigatória e não pode ser vazia. Operação cancelada.")
                    return None

                retorno = {
                    "nome": nome_final,
                    "nacionalidade": nacionalidade_final,
                    "ano_nascimento": ano_nascimento_final,
                    "funcao": funcao_final
                }
                if id_val is not None:
                    retorno["id"] = id_val
                return retorno

            retorno = {
                "nome": nome_final,
                "nacionalidade": nacionalidade_final
            }
            if id_val is not None:
                retorno["id"] = id_val
            return retorno

        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            return None
        except Exception as e:
            print(f"\nOcorreu um erro inesperado ao coletar dados: {e}")
            return None

    def pegar_id(self, mensagem: str):
        return le_num_inteiro(mensagem)