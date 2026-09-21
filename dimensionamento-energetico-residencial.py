# IMPORTAÇÕES
# ----------------------------------------- 
import re       # validações
import matplotlib.pyplot as plt

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
        "tipo": tipo.lower(),
        "equipamentos": [],
        "historico": []
    }

    usuario["imoveis"].append(imovel)
    print("\tIMÓVEL CADASTRADO COM SUCESSO!")

def listar_imoveis(usuario):
    print(f"\n\tIMÓVEIS CADASTRADOS DE {usuario["nome"].upper()}")

    if not usuario["imoveis"]:
        print("Nenhum imóvel cadastrado.")
    else:
        for i, imovel in enumerate(usuario["imoveis"], start=1):
            print(f"{i} - {imovel['nome']} ({imovel['tipo']}) - {imovel['endereco']}")

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


def detalhes_imovel(usuario):
    print("\n\tDETALHES DO IMÓVEL")

    if not usuario["imoveis"]:
        print("Nenhum imóvel cadastrado.")
        return

    # lista os imóveis com índice
    for i, imovel in enumerate(usuario["imoveis"], start=1):
        print(f"{i} - {imovel['nome']} ({imovel['tipo']}) - {imovel['endereco']}")

    try:
        escolha = int(input("Digite o número do imóvel para ver detalhes: "))
        if escolha < 1 or escolha > len(usuario["imoveis"]):
            print("Opção inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    imovel = usuario["imoveis"][escolha - 1]

    # exibir dados cadastrais
    print("\n\tDados do Imóvel")
    print(f"Nome: {imovel['nome']}")
    print(f"Endereço: {imovel['endereco']}")
    print(f"Tipo: {imovel['tipo']}")

    # exibir equipamentos vinculados
    print("\n\tEquipamentos")
    if "equipamentos" not in imovel or not imovel["equipamentos"]:
        print("Nenhum equipamento cadastrado.")
    else:
        for eq in imovel["equipamentos"]:
            consumo_eq = calcular_consumo_equipamento(eq)
            print(f"- {eq['nome']} | Quantidade: {eq['quantidade']} | "
                  f"Potência: {eq['potencia_watts']}W | Uso diário: {eq['horas_uso']}h | "
                  f"Consumo: {consumo_eq:.2f} kWh/mês")

        consumo_total = calcular_consumo_mensal(imovel)
        print(f"\nConsumo total estimado: {consumo_total:.2f} kWh/mês")

    # navegação de volta
    input("\nPressione ENTER para voltar à lista de imóveis...")

# PB 07 - PB 12
# -----------------------------------------

def validar_inteiro_positivo(valor):
    return valor.isdigit() and int(valor) > 0


def validar_numero_positivo(valor):
    try:
        float(valor.replace(",", "."))
        return float(valor) > 0
    except ValueError:
        return False

def menu_equipamentos(imovel):
    while True:
        print(f"\n\tEQUIPAMENTOS - {imovel['nome'].upper()}")
        print("0 - Voltar")
        print("1 - Adicionar equipamento")
        print("2 - Listar equipamentos")
        print("3 - Editar equipamento")
        print("4 - Remover equipamento")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break
        elif opcao == "1":
            cadastrar_equipamento(imovel)
        elif opcao == "2":
            listar_equipamentos(imovel)
        elif opcao == "3":
            editar_equipamento(imovel)
        elif opcao == "4":
            remover_equipamento(imovel)
        else:
            print("Opção inválida, tente novamente.")

def cadastrar_equipamento(imovel):
    print(f"\n\tCADASTRO DE EQUIPAMENTO - {imovel['nome'].upper()}")

    nome = pedir_campo(
        "Digite o nome do equipamento: ",
        validar_string,
        "Nome é obrigatório!")

    quantidade = pedir_campo(
        "Digite a quantidade: ",
        validar_inteiro_positivo,
        "Quantidade deve ser um número inteiro maior que zero!")

    potencia = pedir_campo(
        "Digite a potência do equipamento (em watts): ",
        validar_numero_positivo,
        "Potência deve ser um número maior que zero!")

    horas_uso = pedir_campo(
        "Digite as horas de uso diário: ",
        validar_numero_positivo,
        "Horas de uso deve ser um número maior que zero!")

    equipamento = {
        "nome": nome,
        "quantidade": int(quantidade),
        "potencia_watts": float(potencia),
        "horas_uso": float(horas_uso)
    }

    imovel["equipamentos"].append(equipamento)
    print("\tEQUIPAMENTO CADASTRADO COM SUCESSO!")


def listar_equipamentos(imovel):
    print(f"\n\tEQUIPAMENTOS DE {imovel['nome'].upper()}")

    if not imovel["equipamentos"]:
        print("Nenhum equipamento cadastrado.")
    else:
        for i, equip in enumerate(imovel["equipamentos"], start=1):
            print(f"{i} - {equip['nome']} | Qtd: {equip['quantidade']} | "
                  f"Potência: {equip['potencia_watts']}W | Uso diário: {equip['horas_uso']}h")


def selecionar_equipamento(imovel):
    if not imovel["equipamentos"]:
        print("Nenhum equipamento cadastrado.")
        return None

    listar_equipamentos(imovel)

    try:
        escolha = int(input("Digite o número do equipamento: "))
        if escolha < 1 or escolha > len(imovel["equipamentos"]):
            print("Opção inválida.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None

    return imovel["equipamentos"][escolha - 1]


def editar_equipamento(imovel):
    print("\n\tEDITAR EQUIPAMENTO")

    equipamento = selecionar_equipamento(imovel)
    if equipamento is None:
        return

    nova_quantidade = pedir_campo(
        "Nova quantidade: ",
        validar_inteiro_positivo,
        "Quantidade deve ser um número inteiro maior que zero!")

    novas_horas = pedir_campo(
        "Novas horas de uso diário: ",
        validar_numero_positivo,
        "Horas de uso deve ser um número maior que zero!")

    equipamento["quantidade"] = int(nova_quantidade)
    equipamento["horas_uso"] = float(novas_horas)

    print("\tEQUIPAMENTO EDITADO COM SUCESSO!")


def remover_equipamento(imovel):
    print("\n\tREMOVER EQUIPAMENTO")

    equipamento = selecionar_equipamento(imovel)
    if equipamento is None:
        return

    confirmacao = input(f"Tem certeza que deseja remover '{equipamento['nome']}'? (s/n): ").lower()
    if confirmacao == "s":
        imovel["equipamentos"].remove(equipamento)
        print("\tEQUIPAMENTO REMOVIDO COM SUCESSO!")
    else:
        print("\tRemoção cancelada.")

DIAS_MES = 30

def calcular_consumo_equipamento(equipamento):
    # Fórmula: (potência em watts * quantidade * horas de uso diário) / 1000 = kWh/dia
    consumo_diario_kwh = (equipamento["potencia_watts"] * equipamento["quantidade"] * equipamento["horas_uso"]) / 1000
    return consumo_diario_kwh * DIAS_MES


def calcular_consumo_mensal(imovel):
    return sum(calcular_consumo_equipamento(equip) for equip in imovel["equipamentos"])


def exibir_consumo_imovel(imovel):
    print(f"\n\tCONSUMO MENSAL ESTIMADO - {imovel['nome'].upper()}")

    if not imovel["equipamentos"]:
        print("Nenhum equipamento cadastrado para calcular o consumo.")
        return

    for equip in imovel["equipamentos"]:
        consumo = calcular_consumo_equipamento(equip)
        print(f"- {equip['nome']}: {consumo:.2f} kWh/mês")

    total = calcular_consumo_mensal(imovel)
    print(f"\n\tCONSUMO TOTAL ESTIMADO: {total:.2f} kWh/mês")


def registrar_consumo_mensal(imovel):
    print(f"\n\tREGISTRAR CONSUMO MENSAL - {imovel['nome'].upper()}")

    if not imovel["equipamentos"]:
        print("Cadastre ao menos um equipamento antes de registrar o consumo.")
        return

    mes = pedir_campo(
        "Digite o mês/ano de referência (ex: Janeiro/2026): ",
        validar_string,
        "Mês/ano é obrigatório!")

    consumo = calcular_consumo_mensal(imovel)

    registro = {
        "mes": mes,
        "consumo_kwh": consumo
    }

    imovel["historico"].append(registro)
    print(f"\tCONSUMO DE {consumo:.2f} kWh REGISTRADO PARA {mes.upper()}!")


def exibir_historico(imovel):
    print(f"\n\tHISTÓRICO DE CONSUMO - {imovel['nome'].upper()}")

    if not imovel["historico"]:
        print("Nenhum histórico de consumo registrado.")
        return

    media = sum(registro["consumo_kwh"] for registro in imovel["historico"]) / len(imovel["historico"])

    for registro in imovel["historico"]:
        if registro["consumo_kwh"] > media:
            status = "ACIMA DA MÉDIA"
        elif registro["consumo_kwh"] < media:
            status = "ABAIXO DA MÉDIA"
        else:
            status = "NA MÉDIA"
        print(f"- {registro['mes']}: {registro['consumo_kwh']:.2f} kWh ({status})")

    print(f"\n\tMÉDIA MENSAL: {media:.2f} kWh")

def ranking_equipamentos(imovel):
    print(f"\n\tRANKING DE EQUIPAMENTOS - {imovel['nome'].upper()}")

    if not imovel["equipamentos"]:
        print("Nenhum equipamento cadastrado.")
        return

    ranking = sorted(imovel["equipamentos"], key=calcular_consumo_equipamento, reverse=True)

    for i, equip in enumerate(ranking, start=1):
        consumo = calcular_consumo_equipamento(equip)
        destaque = "  <-- MAIOR CONSUMO" if i == 1 else ""
        print(f"{i}º - {equip['nome']}: {consumo:.2f} kWh/mês{destaque}")


def relatorio_comparativo(usuario):
    print("\n\tRELATÓRIO COMPARATIVO ENTRE IMÓVEIS")

    if not usuario["imoveis"]:
        print("Nenhum imóvel cadastrado.")
        return

    consumos = [(imovel["nome"], calcular_consumo_mensal(imovel)) for imovel in usuario["imoveis"]]

    if len(consumos) < 2:
        print("Cadastre ao menos dois imóveis com equipamentos para gerar um comparativo.")
        return

    nomes = [nome for nome, _ in consumos]
    totais = [total for _, total in consumos]

    indice_maior = totais.index(max(totais))
    indice_menor = totais.index(min(totais))

    # Resumo em texto no terminal
    for nome, total in consumos:
        print(f"- {nome}: {total:.2f} kWh/mês")

    print(f"\n\tMAIOR CONSUMO: {nomes[indice_maior]} ({totais[indice_maior]:.2f} kWh/mês)")
    print(f"\tMENOR CONSUMO: {nomes[indice_menor]} ({totais[indice_menor]:.2f} kWh/mês)")

    # Gráfico comparativo com matplotlib
    cores = ["#4C72B0"] * len(nomes)
    cores[indice_maior] = "#C44E52"
    cores[indice_menor] = "#55A868"

    media = sum(totais) / len(totais)

    figura, eixo = plt.subplots(figsize=(8, 5))
    barras = eixo.bar(nomes, totais, color=cores)

    eixo.axhline(media, color="gray", linestyle="--", linewidth=1, label=f"Média ({media:.2f} kWh/mês)")

    for barra, total in zip(barras, totais):
        eixo.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height(),
            f"{total:.2f}",
            ha="center",
            va="bottom"
        )

    eixo.set_title("Comparativo de Consumo Mensal Estimado entre Imóveis")
    eixo.set_xlabel("Imóvel")
    eixo.set_ylabel("Consumo (kWh/mês)")
    eixo.legend()
    plt.xticks(rotation=15)
    plt.tight_layout()

    caminho_grafico = "comparativo_imoveis.png"
    plt.savefig(caminho_grafico)
    print(f"\n\tGráfico comparativo salvo em: {caminho_grafico}")

    plt.show()
    plt.close(figura)

def selecionar_imovel(usuario):
    if not usuario["imoveis"]:
        print("Nenhum imóvel cadastrado.")
        return None

    listar_imoveis(usuario)

    try:
        escolha = int(input("Digite o número do imóvel: "))
        if escolha < 1 or escolha > len(usuario["imoveis"]):
            print("Opção inválida.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None

    return usuario["imoveis"][escolha - 1]

def resumo_energetico_anual(usuario):
    print("\n\tRESUMO ENERGÉTICO ANUAL")

    imovel = selecionar_imovel(usuario)
    if imovel is None:
        return

    if not imovel["historico"]:
        print("Nenhum consumo mensal registrado para este imóvel.")
        return

    total_anual = sum(registro["consumo_kwh"] for registro in imovel["historico"])
    mes_maior = max(imovel["historico"], key=lambda r: r["consumo_kwh"])

    print(f"\n\tIMÓVEL: {imovel['nome'].upper()}")
    for registro in imovel["historico"]:
        destaque = "  <-- MAIOR CONSUMO DO ANO" if registro is mes_maior else ""
        print(f"- {registro['mes']}: {registro['consumo_kwh']:.2f} kWh{destaque}")

    print(f"\n\tCONSUMO TOTAL ANUAL: {total_anual:.2f} kWh")
    print(f"\tMÊS DE MAIOR CONSUMO: {mes_maior['mes']} ({mes_maior['consumo_kwh']:.2f} kWh)")


def menu(usuario):
    while True:
        print("\n\tMENU PRINCIPAL")
        print("0  - Sair")
        print("1  - Cadastrar imóvel")
        print("2  - Listar imóveis")
        print("3  - Editar imóvel")
        print("4  - Remover imóvel")
        print("5  - Detalhes do imóvel")
        print("6  - Gerenciar equipamentos de um imóvel")
        print("7  - Ver consumo mensal estimado de um imóvel")
        print("8  - Ver histórico de consumo de um imóvel")
        print("9  - Registrar consumo mensal de um imóvel")
        print("10 - Ver ranking de equipamentos de um imóvel")
        print("11 - Comparativo entre imóveis")
        print("12 - Resumo energético anual")

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
        elif opcao == "5":
            detalhes_imovel(usuario)
        elif opcao == "6":
            imovel = selecionar_imovel(usuario)
            if imovel is not None:
                menu_equipamentos(imovel)
        elif opcao == "7":
            imovel = selecionar_imovel(usuario)
            if imovel is not None:
                exibir_consumo_imovel(imovel)
        elif opcao == "8":
            imovel = selecionar_imovel(usuario)
            if imovel is not None:
                exibir_historico(imovel)
        elif opcao == "9":
            imovel = selecionar_imovel(usuario)
            if imovel is not None:
                registrar_consumo_mensal(imovel)
        elif opcao == "10":
            imovel = selecionar_imovel(usuario)
            if imovel is not None:
                ranking_equipamentos(imovel)
        elif opcao == "11":
            relatorio_comparativo(usuario)
        elif opcao == "12":
            resumo_energetico_anual(usuario)
        else:
            print("Opção inválida, tente novamente.")

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

