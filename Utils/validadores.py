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
