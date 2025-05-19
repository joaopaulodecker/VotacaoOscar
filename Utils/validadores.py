def le_num_inteiro(msg):
    while True:
        entrada = input(msg)
        if entrada.isdigit():
            return int(entrada)
        print("Entrada inválida. Digite um número inteiro.")

def le_string_nao_vazia(mensagem="Digite um texto: "):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("❌ O valor não pode ser vazio.")
