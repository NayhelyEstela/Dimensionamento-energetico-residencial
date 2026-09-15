# IMPORTAÇÕES
# ----------------------------------------- 
import re       # validações


# FUNÇÕES 
# ----------------------------------------- 
def validar_string(valor):
    return valor.strip() != ""

def validar_email(email_cadastro):
    # usa o regex 
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(padrao, email_cadastro) is not None

def validar_senha(senha_cadastro):
    return senha_cadastro.isdigit()

def pedir_campo(mensagem, funcao_validacao, erro):
    while True:
        valor = input(mensagem)

        if funcao_validacao(valor):
            return valor

        print(f"\t{erro}")

def cadastro_usuario():
    print("\tCADASTRO DE PERFIL")

    nome = pedir_campo(
        "Digite seu nome: ",
        validar_string,
        "Nome é obrigatório!")

    email = pedir_campo(
        "Digite seu e-mail: ",
        validar_email,
        "E-mail inválido!")

    senha = pedir_campo(
        "Digite sua senha (apenas numeros): ",
        validar_senha,
        "A senha deve conter apenas números!")

    print("\tCADASTRO REALIZADO COM SUCESSO!")

    usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "imoveis": []
    }

    return usuario

def verificar_login(email_cadastro, senha_cadastro):
    print("\n\tLOGIN")

    while True:
        email_login = pedir_campo(
            "Digite seu e-mail: ",
            validar_email,
            "E-mail inválido!"
        )

        if email_login != email_cadastro:
            print("\tE-mail incorreto!")
            continue
        break

    while True:
        senha_login = pedir_campo(
            "Digite sua senha (apenas numeros): ",
            validar_senha,
            "A senha deve conter apenas números!"
        )

        if senha_login != senha_cadastro:
            print("\tSenha incorreta!")
            continue

        print("\tLOGIN REALIZADO COM SUCESSO!")
        break

def menu(usuario):
    while True:
        print("\n\tMENU PRINCIPAL")
        print("0 - Sair")
        print("1 - Cadastrar imóvel")
        print("2 - Listar imóveis")
        print("3 - Editar imóvel")
        print("4 - Remover imóvel")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("Saindo do sistema...")
            break
        elif opcao == "1":
            cadastro_imovel(usuario)
        elif opcao == "2":
            listar_imoveis(usuario)
        elif opcao == "3":
            editar_imovel(usuario)
        elif opcao == "4":
            remover_imovel(usuario)
        else:
            print("Opção inválida, tente novamente.")

def validar_tipo(tipo):
    return tipo.lower() in ["casa", "apartamento"]

def cadastro_imovel(usuario):
    print("\n\tCADASTRO DE IMÓVEL")

    nome_imovel = pedir_campo(
        "Digite o nome/apelido do imóvel: ",
        validar_string,
        "Nome/apelido é obrigatório!")

    endereco = pedir_campo(
        "Digite o endereço do imóvel: ",
        validar_string,
        "Endereço é obrigatório!")

    tipo = pedir_campo(
        "Digite o tipo (casa/apartamento): ",
        validar_tipo,
        "Tipo inválido! Digite 'casa' ou 'apartamento'.")

    imovel = {
        "nome": nome_imovel,
        "endereco": endereco,
        "tipo": tipo.lower()
    }

    usuario["imoveis"].append(imovel)
    print("\tIMÓVEL CADASTRADO COM SUCESSO!")

def listar_imoveis(usuario):
    print(f"\n\tIMÓVEIS CADASTRADOS DE {usuario["nome"].upper()}")

    if not usuario["imoveis"]:
        print("Nenhum imóvel cadastrado.")
    else:
        for imovel in usuario["imoveis"]:
            print(f"- {imovel['nome']} ({imovel['tipo']}) - {imovel['endereco']}")

def editar_imovel(usuario):
    print("\n\tEDITAR IMÓVEL")

    if not usuario["imoveis"]:
        print("Nenhum imóvel cadastrado para editar.")
        return

    for i, imovel in enumerate(usuario["imoveis"], start=1):
        print(f"{i} - {imovel['nome']} ({imovel['tipo']}) - {imovel['endereco']}")

    try:
        escolha = int(input("Digite o número do imóvel que deseja editar: "))
        if escolha < 1 or escolha > len(usuario["imoveis"]):
            print("Opção inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    imovel = usuario["imoveis"][escolha - 1]

    novo_nome = pedir_campo(
        "Novo nome/apelido: ",
        validar_string,
        "Nome é obrigatório!")

    novo_endereco = pedir_campo(
        "Novo endereço: ",
        validar_string,
        "Endereço é obrigatório!")

    novo_tipo = pedir_campo(
        "Novo tipo (casa/apartamento): ",
        validar_tipo,
        "Tipo inválido!")

    imovel["nome"] = novo_nome
    imovel["endereco"] = novo_endereco
    imovel["tipo"] = novo_tipo.lower()

    print("\tIMÓVEL EDITADO COM SUCESSO!")

def remover_imovel(usuario):
    print("\n\tREMOVER IMÓVEL")

    if not usuario["imoveis"]:
        print("Nenhum imóvel cadastrado para remover.")
        return

    for i, imovel in enumerate(usuario["imoveis"], start=1):
        print(f"{i} - {imovel['nome']} ({imovel['tipo']}) - {imovel['endereco']}")

    try:
        escolha = int(input("Digite o número do imóvel que deseja remover: "))
        if escolha < 1 or escolha > len(usuario["imoveis"]):
            print("Opção inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    imovel = usuario["imoveis"][escolha - 1]

    confirmacao = input(f"Tem certeza que deseja remover '{imovel['nome']}'? (s/n): ").lower()
    if confirmacao == "s":
        usuario["imoveis"].pop(escolha - 1)  # remove pelo índice
        print("\tIMÓVEL REMOVIDO COM SUCESSO!")
    else:
        print("\tRemoção cancelada.")


# PROGRAMA PRINCIPAL
# -----------------------------------------
print("\n\t\tDIMENSIONAMENTO ENERGÉTICO RESIDENCIAL")
print("=" * 65)

# === CADASTRO ===
usuario = cadastro_usuario()

# === LOGIN ===
verificar_login(usuario["email"], usuario["senha"])

# === MENU ===
menu(usuario)

