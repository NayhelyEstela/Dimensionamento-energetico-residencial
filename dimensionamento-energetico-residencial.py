# IMPORTAÇÕES
# ----------------------------------------- 
import re       # validações


# FUNÇÕES 
# ----------------------------------------- 
def validar_nome(n):
    return n.strip() != ""

def validar_email(e):
    # usa o regex 
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(padrao, e) is not None

def validar_senha(s):
    return s.isdigit()

# *********
def pedir_campo(mensagem, funcao_validacao, erro):
    while True:
        valor = input(mensagem)

        if funcao_validacao(valor):
            return valor

        print(f"\t{erro}")


print("\n\t\tDIMENSIONAMENTO ENERGÉTICO RESIDENCIAL")
print("-" * 65)

# Nome ----
nome = pedir_campo(
    "Digite seu nome: ", 
    validar_nome, 
    "Nome é obrigatório!")

# E-mail ----
email = pedir_campo(
    "Digite seu e-mail: ",
    validar_email,
    "E-mail inválido!")

# Senha ----
senha = pedir_campo(
    "Digite sua senha (apenas numeros): ",
    validar_senha,
    "A senha deve conter apenas números!")

print("\n\tCADASTRO REALIZADO COM SUCESSO!")


