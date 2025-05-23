from datetime import date, datetime

def le_num_inteiro(mensagem_prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    while True:
        entrada_str = input(mensagem_prompt).strip()
        if entrada_str.isdigit() or (entrada_str.startswith('-') and entrada_str[1:].isdigit()):
            try:
                numero = int(entrada_str)
                
                valido = True
                if min_val is not None and numero < min_val:
                    valido = False
                    print(f"❌ Valor inválido. O número deve ser maior ou igual a {min_val}.")
                if max_val is not None and numero > max_val:
                    valido = False
                    print(f"❌ Valor inválido. O número deve ser menor ou igual a {max_val}.")
                
                if valido:
                    return numero

            except ValueError:
                print("❌ Entrada inválida. Ocorreu um erro ao converter para número.")
        else:
            print("❌ Entrada inválida. Por favor, digite um número inteiro.")

def le_string_nao_vazia(mensagem_prompt: str = "Digite um texto: ") -> str:
    while True:
        valor = input(mensagem_prompt).strip()
        if valor:
            return valor
        print("❌ O valor não pode ser vazio. Por favor, digite algum texto.")

def le_string_permitindo_vazio(mensagem_prompt: str = "Digite um texto (ou deixe em branco): ") -> str:
    valor = input(mensagem_prompt).strip()
    return valor

def le_data(mensagem_prompt: str, permitir_vazio: bool = False) -> date | None:
    while True:
        data_str = input(f"{mensagem_prompt} (formato DD/MM/AAAA): ").strip()
        if not data_str and permitir_vazio:
            return None
        if not data_str and not permitir_vazio:
            print("❌ A data não pode ser vazia.")
            continue
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
            return data_obj
        except ValueError:
            print("❌ Data inválida. Use o formato DD/MM/AAAA.")

def le_opcao_sim_nao(mensagem_prompt: str) -> bool:
    while True:
        resposta = input(f"{mensagem_prompt} (S/N): ").strip().upper()
        if resposta == 'S':
            return True
        elif resposta == 'N':
            return False
        print("❌ Resposta inválida. Por favor, digite S para Sim ou N para Não.")

def le_ano_valido(mensagem_prompt: str, min_ano: int | None = 1888, max_ano: int | None = None) -> int | None:
    if max_ano is None:
        max_ano = datetime.now().year + 5 

    while True:
        try:
            ano_str = input(mensagem_prompt).strip()
            if not ano_str: 
                return None
            ano = int(ano_str)
            if (min_ano is not None and ano < min_ano) or (max_ano is not None and ano > max_ano):
                print(f"❌ Ano inválido. Deve estar entre {min_ano or 'qualquer'} e {max_ano or 'qualquer'}.")
            else:
                return ano
        except ValueError:
            print("❌ Entrada inválida. Por favor, digite um ano válido (número).")

def le_float_positivo(mensagem_prompt: str, permitir_zero: bool = False) -> float | None:
    while True:
        entrada_str = input(mensagem_prompt).strip()
        if not entrada_str: # Permite cancelar com Enter
            return None
        try:
            numero = float(entrada_str.replace(',', '.'))
            if permitir_zero and numero >= 0:
                return numero
            elif not permitir_zero and numero > 0:
                return numero
            elif permitir_zero:
                print("❌ O número deve ser maior ou igual a zero.")
            else:
                print("❌ O número deve ser maior que zero.")
        except ValueError:
            print("❌ Entrada inválida. Por favor, digite um número válido.")

def le_escolha_de_lista(mensagem_prompt: str, opcoes: list[str], permitir_cancelar: bool = True) -> str | None:

    if not opcoes:
        print("⚠️ Nenhuma opção disponível para escolha.")
        return None

    print(f"\n{mensagem_prompt}")
    for i, opcao_texto in enumerate(opcoes):
        print(f"{i + 1}. {opcao_texto}")
    
    prompt_final = f"Escolha o número da opção (1-{len(opcoes)})"
    if permitir_cancelar:
        prompt_final += " ou 0 para cancelar: "
    else:
        prompt_final += ": "

    while True:
        try:
            escolha_str = input(prompt_final).strip()
            if not escolha_str and permitir_cancelar:
                print("Seleção cancelada.")
                return None
            escolha_num = int(escolha_str)
            if permitir_cancelar and escolha_num == 0:
                print("Seleção cancelada.")
                return None
            if 1 <= escolha_num <= len(opcoes):
                return opcoes[escolha_num - 1]
            else:
                print(f"❌ Número inválido. Escolha entre 1 e {len(opcoes)}" + (" ou 0." if permitir_cancelar else "."))
        except ValueError:
            print("❌ Entrada inválida. Por favor, digite um número.")

def le_texto_alpha_espacos(prompt_msg: str, permitir_vazio_cancela: bool = True) -> str | None:
    while True:
        texto = input(prompt_msg).strip()
        if permitir_vazio_cancela and not texto:
            return None  # Usuário cancelou

        if not texto:
            print("❌ Entrada não pode ser vazia. Tente novamente.")
            continue

        if any(char.isdigit() for char in texto):
            print("❌ Entrada não deve conter números. Tente novamente.")
            continue

        if not any(char.isalpha() for char in texto): # garante pelo menos uma letra
            print("❌ Entrada deve conter pelo menos uma letra. Tente novamente.")
            continue
            
        return texto

def le_opcao_de_lista(prompt_msg: str, lista_opcoes: list[str], permitir_vazio_cancela: bool = True, mensagem_erro_personalizada: str | None = None) -> str | None:
    opcoes_lower = [opt.lower() for opt in lista_opcoes]
    while True:
        escolha = input(prompt_msg).strip()
        if permitir_vazio_cancela and not escolha:
            return None # Usuário cancelou

        if not escolha and not permitir_vazio_cancela:
            print("❌ Opção não pode ser vazia. Tente novamente.")
            continue
        
        escolha_lower = escolha.lower()

        if escolha_lower in opcoes_lower:
            for i, opt_l in enumerate(opcoes_lower):
                if opt_l == escolha_lower:
                    return lista_opcoes[i]
        
        erro_msg = mensagem_erro_personalizada if mensagem_erro_personalizada else "Opção inválida."
        print(f"❌ {erro_msg} As opções válidas são: {', '.join(lista_opcoes)}. Tente novamente.")