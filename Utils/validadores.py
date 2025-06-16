from datetime import date, datetime

def le_num_inteiro(
    mensagem_prompt: str,
    min_val: int | None = None,
    max_val: int | None = None,
    permitir_vazio: bool = False 
) -> int | None:

    while True:
        entrada_str = input(mensagem_prompt).strip()
        
        if permitir_vazio and not entrada_str:
            return None
            
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
    """Lê uma string do usuário, garantindo que não seja vazia."""
    while True:
        valor = input(mensagem_prompt).strip()
        if valor:
            return valor
        print("❌ O valor não pode ser vazio. Por favor, digite algum texto.")

def le_string_permitindo_vazio(mensagem_prompt: str = "Digite um texto (ou deixe em branco): ") -> str:
    """Lê uma string do usuário, permitindo que ela seja vazia."""
    valor = input(mensagem_prompt).strip()
    return valor

def le_texto_alpha_espacos(prompt_msg: str, permitir_vazio_cancela: bool = True) -> str | None:
    """Lê uma string contendo apenas letras e espaços."""
    while True:
        texto = input(prompt_msg).strip()
        if permitir_vazio_cancela and not texto:
            return None

        if not texto:
            print("❌ Entrada não pode ser vazia. Tente novamente.")
            continue

        if any(char.isdigit() for char in texto):
            print("❌ Entrada não deve conter números. Tente novamente.")
            continue

        if not any(char.isalpha() for char in texto):
            print("❌ Entrada deve conter pelo menos uma letra. Tente novamente.")
            continue
            
        return texto

def le_data(mensagem_prompt: str, permitir_vazio: bool = False) -> date | None:
    """Lê uma data no formato DD/MM/AAAA e a valida."""
    while True:
        data_str = input(mensagem_prompt).strip()
        if permitir_vazio and not data_str:
            return None
        
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
            return data_obj
        except ValueError:
            print("❌ Data inválida. Por favor, use o formato DD/MM/AAAA.")