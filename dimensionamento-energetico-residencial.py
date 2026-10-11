# IMPORTAÇÕES
# -----------------------------------------
import re       # validações
import matplotlib.pyplot as plt
import csv
import math
import os
import unicodedata
import hashlib
import secrets


# DATASETS
# -----------------------------------------


# HSP -------------------------------------
CAMINHO_HSP = "hsp.csv"

COLUNAS_HSP_TEXTO = ["cidade", "estado"]
COLUNAS_HSP_NUM = ["hsp"]


# MODULOS ---------------------------------
CAMINHO_MODULOS = "modulos.csv"          # task 12

COLUNAS_MODULOS_TEXTO = ["id", "fabricante", "modelo"]
COLUNAS_MODULOS_NUM = ["potencia_wp", "preco", "voc_v", "vmp_v", "imp_a"]


# INVERSORES ------------------------------
CAMINHO_INVERSORES = "inversores.csv"    # task 12

COLUNAS_INVERSORES_TEXTO = ["id", "fabricante", "modelo", "compativel_bateria"]
COLUNAS_INVERSORES_NUM = ["potencia_nominal_kw", "potencia_max_fv_kw", "mppt_min_v",
                          "tensao_max_v", "corrente_max_entrada_a", "numero_mppt", "preco"]


# PARÂMETROS (justificativas no README)
# -----------------------------------------
LIMITE_PERCENTUAL = 100  # US01: 0 < f <= 100
DIAS_GERACAO = 30  # D
EFICIENCIA_SISTEMA = 0.80  # η
DIAS_MES_BATERIA = 30  # divisor de E_d
DOD_PADRAO = 0.80  # DoD usado em C_bat (US06)
EFICIENCIA_BATERIA = 0.90  # η_bat


# FUNÇÕES UTILITÁRIOS
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

def validar_inteiro_positivo(valor):
    return valor.isdigit() and int(valor) > 0


def validar_numero_positivo(valor):
    try:
        float(valor.replace(",", "."))
        return float(valor) > 0
    except ValueError:
        return False


def converter_numero(valor):
    return float(str(valor).strip().replace(",", "."))


def validar_decimal_positivo(valor):
    try:
        return converter_numero(valor) > 0
    except ValueError:
        return False


def validar_percentual(valor):
    try:
        return 0 < converter_numero(valor) <= LIMITE_PERCENTUAL
    except ValueError:
        return False


def validar_com_sem(valor):
    return valor.strip().lower() in ["com", "sem"]


def validar_estado(valor):
    return len(valor.strip()) == 2 and valor.strip().isalpha()


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode()
    return " ".join(sem_acento.lower().split())


def ler_csv_validado(caminho, colunas_texto, colunas_num):
    if not os.path.exists(caminho):
        print(f"\tArquivo '{caminho}' não encontrado.")
        return None

    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        primeira = arquivo.readline()
        arquivo.seek(0)
        delimitador = ";" if ";" in primeira else ","
        leitor = csv.DictReader(arquivo, delimiter=delimitador)

        faltando = [c for c in colunas_texto + colunas_num if c not in (leitor.fieldnames or [])]
        if faltando:
            print(f"\tColunas ausentes em '{caminho}': {', '.join(faltando)}")
            return None

        validos, invalidos = [], []
        for numero, linha in enumerate(leitor, start=2):  # linha 1 = cabeçalho
            registro, motivo = {}, None

            for c in colunas_texto:
                valor = (linha.get(c) or "").strip()
                if not valor:
                    motivo = f"campo '{c}' vazio"
                    break
                registro[c] = valor

            if motivo is None:
                for c in colunas_num:
                    try:
                        valor = converter_numero(linha.get(c) or "")
                    except ValueError:
                        motivo = f"campo '{c}' não numérico"
                        break
                    if valor <= 0:
                        motivo = f"campo '{c}' deve ser maior que zero"
                        break
                    registro[c] = valor

            if motivo is None:
                validos.append(registro)
            else:
                invalidos.append((numero, motivo))

    return validos, invalidos


# PERSISTÊNCIA
# -----------------------------------------
PASTA_DADOS = "dados"
CAMINHO_USUARIOS = os.path.join(PASTA_DADOS, "usuarios.csv")
CAMINHO_IMOVEIS = os.path.join(PASTA_DADOS, "imoveis.csv")
CAMINHO_EQUIPAMENTOS = os.path.join(PASTA_DADOS, "equipamentos.csv")
CAMINHO_HISTORICO = os.path.join(PASTA_DADOS, "historico_consumo.csv")

CAMPOS_USUARIOS = ["id_usuario", "nome", "email", "senha_hash"]
CAMPOS_IMOVEIS = ["id_imovel", "id_usuario", "nome", "endereco", "cidade", "estado", "tipo"]
CAMPOS_EQUIPAMENTOS = ["id_equipamento", "id_imovel", "nome", "quantidade",
                       "potencia_watts", "horas_uso"]
CAMPOS_HISTORICO = ["id_imovel", "mes", "consumo_kwh"]


def gerar_hash_senha(senha, salt=None):
    salt = salt or secrets.token_hex(8)
    h = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt.encode(), 100_000).hex()
    return f"{salt}${h}"


def conferir_senha(senha, senha_hash):
    salt = senha_hash.split("$")[0]
    return secrets.compare_digest(gerar_hash_senha(senha, salt), senha_hash)


def atribuir_ids(itens):
    """Dá id aos itens novos (sem 'id'); os já salvos mantêm o seu."""
    maior = max((i.get("id", 0) for i in itens), default=0)
    for item in itens:
        if "id" not in item:
            maior += 1
            item["id"] = maior


def escrever_csv(caminho, campos, linhas):
    temporario = caminho + ".tmp"
    with open(temporario, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(linhas)
    os.replace(temporario, caminho)  # troca atômica: nunca deixa arquivo pela metade


def salvar_dados(usuarios):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    imoveis = [i for u in usuarios for i in u["imoveis"]]
    equipamentos = [e for i in imoveis for e in i["equipamentos"]]
    for itens in (usuarios, imoveis, equipamentos):
        atribuir_ids(itens)

    escrever_csv(CAMINHO_USUARIOS, CAMPOS_USUARIOS, [
        {"id_usuario": u["id"], "nome": u["nome"], "email": u["email"],
         "senha_hash": u["senha_hash"]} for u in usuarios])
    escrever_csv(CAMINHO_IMOVEIS, CAMPOS_IMOVEIS, [
        {"id_imovel": i["id"], "id_usuario": u["id"], "nome": i["nome"],
         "endereco": i["endereco"], "cidade": i.get("cidade", ""),
         "estado": i.get("estado", ""), "tipo": i["tipo"]}
        for u in usuarios for i in u["imoveis"]])
    escrever_csv(CAMINHO_EQUIPAMENTOS, CAMPOS_EQUIPAMENTOS, [
        {"id_equipamento": e["id"], "id_imovel": i["id"], "nome": e["nome"],
         "quantidade": e["quantidade"], "potencia_watts": e["potencia_watts"],
         "horas_uso": e["horas_uso"]}
        for i in imoveis for e in i["equipamentos"]])
    escrever_csv(CAMINHO_HISTORICO, CAMPOS_HISTORICO, [
        {"id_imovel": i["id"], "mes": r["mes"], "consumo_kwh": r["consumo_kwh"]}
        for i in imoveis for r in i["historico"]])


def ler_csv_dados(caminho):
    if not os.path.exists(caminho):
        return []
    try:
        with open(caminho, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except (OSError, UnicodeDecodeError, csv.Error):
        os.replace(caminho, caminho + ".corrompido")
        print(f"\tAviso: '{caminho}' estava ilegível e foi movido para '{caminho}.corrompido'.")
        return []


def carregar_dados():
    usuarios, imoveis = {}, {}

    for r in ler_csv_dados(CAMINHO_USUARIOS):
        try:
            usuarios[r["id_usuario"]] = {
                "id": int(r["id_usuario"]), "nome": r["nome"], "email": r["email"],
                "senha_hash": r["senha_hash"], "imoveis": []}
        except (KeyError, ValueError):
            print(f"\tAviso: linha inválida em '{CAMINHO_USUARIOS}' ignorada.")

    for r in ler_csv_dados(CAMINHO_IMOVEIS):
        try:
            imovel = {
                "id": int(r["id_imovel"]), "nome": r["nome"], "endereco": r["endereco"],
                "cidade": r["cidade"], "estado": r["estado"], "tipo": r["tipo"],
                "equipamentos": [], "historico": []}
            usuarios[r["id_usuario"]]["imoveis"].append(imovel)
            imoveis[r["id_imovel"]] = imovel
        except (KeyError, ValueError):
            print(f"\tAviso: linha inválida em '{CAMINHO_IMOVEIS}' ignorada.")

    for r in ler_csv_dados(CAMINHO_EQUIPAMENTOS):
        try:
            imoveis[r["id_imovel"]]["equipamentos"].append({
                "id": int(r["id_equipamento"]), "nome": r["nome"],
                "quantidade": int(r["quantidade"]),
                "potencia_watts": float(r["potencia_watts"]),
                "horas_uso": float(r["horas_uso"])})
        except (KeyError, ValueError):
            print(f"\tAviso: linha inválida em '{CAMINHO_EQUIPAMENTOS}' ignorada.")

    for r in ler_csv_dados(CAMINHO_HISTORICO):
        try:
            imoveis[r["id_imovel"]]["historico"].append(
                {"mes": r["mes"], "consumo_kwh": float(r["consumo_kwh"])})
        except (KeyError, ValueError):
            print(f"\tAviso: linha inválida em '{CAMINHO_HISTORICO}' ignorada.")

    return list(usuarios.values())


# FUNÇÕES REFERENTES A CP 1
# -----------------------------------------
def cadastro_usuario(usuarios):
    print("\n\tCADASTRO DE PERFIL")

    nome = pedir_campo(
        "Digite seu nome: ",
        validar_string,
        "Nome é obrigatório!")

    while True:
        email = pedir_campo(
            "Digite seu e-mail: ",
            validar_email,
            "E-mail inválido!")

        if any(u["email"].lower() == email.lower() for u in usuarios):
            print("\tE-mail já cadastrado!")
            continue
        break

    senha = pedir_campo(
        "Digite sua senha (apenas numeros): ",
        validar_senha,
        "A senha deve conter apenas números!")

    usuario = {
        "nome": nome,
        "email": email,
        "senha_hash": gerar_hash_senha(senha),
        "imoveis": []
    }

    usuarios.append(usuario)
    print("\tCADASTRO REALIZADO COM SUCESSO!")
    return usuario

def login(usuarios):
    print("\n\tLOGIN")

    email = pedir_campo(
        "Digite seu e-mail: ",
        validar_email,
        "E-mail inválido!")

    senha = pedir_campo(
        "Digite sua senha (apenas numeros): ",
        validar_senha,
        "A senha deve conter apenas números!")

    for usuario in usuarios:
        if usuario["email"].lower() == email.lower() and conferir_senha(senha, usuario["senha_hash"]):
            print("\tLOGIN REALIZADO COM SUCESSO!")
            return usuario

    print("\tE-mail ou senha incorretos!")
    return None

def tela_inicial(usuarios):
    while True:
        print("\n\tBEM-VINDO")
        print("0 - Sair")
        print("1 - Login")
        print("2 - Cadastrar novo perfil")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            return None
        elif opcao == "1":
            usuario = login(usuarios)
            if usuario is not None:
                return usuario
        elif opcao == "2":
            cadastro_usuario(usuarios)
            salvar_dados(usuarios)
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

    cidade, estado = pedir_localizacao()

    imovel = {
        "nome": nome_imovel,
        "endereco": endereco,
        "cidade": cidade,
        "estado": estado,
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

    imovel["cidade"], imovel["estado"] = pedir_localizacao("Nova ")

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


# FUNÇÕES REFERENTES A CP 2
# -----------------------------------------
def pedir_localizacao(prefixo=""):
    cidade = pedir_campo(
        f"{prefixo}Cidade do imóvel: ", validar_string, "Cidade é obrigatória!").strip()
    estado = pedir_campo(
        f"{prefixo}Estado (UF, ex: SP): ", validar_estado,
        "Estado deve ter 2 letras (ex: SP)!").strip().upper()
    return cidade, estado

def garantir_localizacao(imovel):
    """2.5: imóveis antigos sem cidade/estado têm o preenchimento solicitado."""
    if not imovel.get("cidade") or not imovel.get("estado"):
        print("\tEste imóvel ainda não possui localização cadastrada.")
        imovel["cidade"], imovel["estado"] = pedir_localizacao()

def obter_consumo_referencia(imovel):
    if imovel["historico"]:
        media = sum(r["consumo_kwh"] for r in imovel["historico"]) / len(imovel["historico"])
        if media > 0:
            return media, f"média de {len(imovel['historico'])} mês(es) do histórico registrado"

    estimado = calcular_consumo_mensal(imovel)
    if estimado > 0:
        return estimado, "consumo estimado dos equipamentos (sem histórico registrado)"

    return None, None

def definir_energia_mensal(imovel):
    print("\n\t- ENERGIA MENSAL DESEJADA")

    c_m, origem = obter_consumo_referencia(imovel)
    if c_m is None:
        print("\tImóvel sem dados de consumo. Cadastre equipamentos ou registre o consumo mensal.")
        return None

    print(f"Consumo de referência (C_m): {c_m:.2f} kWh/mês")
    print(f"Origem do C_m: {origem}")

    f = converter_numero(pedir_campo(
        f"Percentual do consumo a atender com energia solar (0 < f <= {LIMITE_PERCENTUAL}): ",
        validar_percentual,
        f"Percentual inválido! Digite um número maior que 0 e no máximo {LIMITE_PERCENTUAL} "
        f"(pode usar vírgula)."))

    e_fv = c_m * (f / 100)
    print(f"\tENERGIA A GERAR (E_FV): {e_fv:.2f} kWh/mês")

    return {"c_m": c_m, "origem_c_m": origem, "percentual": f, "e_fv": e_fv}

def buscar_hsp(cidade, estado):
    resultado = ler_csv_validado(CAMINHO_HSP, COLUNAS_HSP_TEXTO, COLUNAS_HSP_NUM)
    if resultado is None:
        return None

    validos, _ = resultado
    for registro in validos:
        if (normalizar(registro["cidade"]) == normalizar(cidade)
                and normalizar(registro["estado"]) == normalizar(estado)):
            return registro
    return None

def obter_hsp(imovel):
    registro = buscar_hsp(imovel["cidade"], imovel["estado"])

    if registro is not None:
        return registro["hsp"]

    print(f"\tSem dado solar para {imovel['cidade']}/{imovel['estado']}.")
    while True:
        manual = input("Digite o HSP manualmente (kWh/m²/dia) ou ENTER para abortar: ").strip()
        if manual == "":
            return None
        if validar_decimal_positivo(manual):
            return converter_numero(manual), "manual"
        print("\tHSP inválido! Digite um número maior que zero.")

def calcular_potencia_fv(imovel, e_fv):
    print("\n\t- POTÊNCIA FOTOVOLTAICA NECESSÁRIA")

    garantir_localizacao(imovel)

    resultado = obter_hsp(imovel)
    if resultado is None:
        print("\tDimensionamento abortado: não há dado de irradiação (HSP) para o imóvel.")
        return None

    hsp, origem = resultado
    p_fv = e_fv / (hsp * DIAS_GERACAO * EFICIENCIA_SISTEMA)

    print(f"HSP utilizado: {hsp:.2f} kWh/m²/dia")
    print(f"Parâmetros: D = {DIAS_GERACAO} dias | η = {EFICIENCIA_SISTEMA}")
    print(f"\tPOTÊNCIA NECESSÁRIA (P_FV): {p_fv:.2f} kWp")

    return {"hsp": hsp, "p_fv": p_fv}

def calcular_geracao_estimada(p_instalada, hsp):
    return p_instalada * hsp * DIAS_GERACAO * EFICIENCIA_SISTEMA

def montar_instalacao(modulo, n, hsp):
    p_instalada = (n * modulo["potencia_wp"]) / 1000
    return {
        "modulo": modulo,
        "n_modulos": n,
        "p_instalada": p_instalada,
        "geracao_estimada": calcular_geracao_estimada(p_instalada, hsp),
    }

def exibir_instalacao(inst):
    m = inst["modulo"]
    print(f"Módulo: {m['fabricante']} {m['modelo']} ({m['potencia_wp']:.0f} Wp) [id {m['id']}]")
    print(f"Quantidade (N): {inst['n_modulos']}")
    print(f"Potência instalada: {inst['p_instalada']:.2f} kWp")
    print(f"\tGERAÇÃO ESTIMADA: {inst['geracao_estimada']:.2f} kWh/mês")

def selecionar_modulo(p_fv, hsp):
    print("\n\t- SELEÇÃO DE MÓDULOS")

    resultado = ler_csv_validado(CAMINHO_MODULOS, COLUNAS_MODULOS_TEXTO, COLUNAS_MODULOS_NUM)
    if resultado is None:
        return None

    validos, invalidos = resultado
    for numero, motivo in invalidos:
        print(f"\tAviso: linha {numero} de '{CAMINHO_MODULOS}' ignorada ({motivo}).")

    if not validos:
        print("\tLimitação: nenhum módulo válido no dataset. Não é possível dimensionar.")
        return None

    validos.sort(key=lambda m: m["preco"] / m["potencia_wp"])

    print("Módulos válidos (ordenados por custo por Wp; o 1 é a sugestão):")
    for i, m in enumerate(validos, start=1):
        n = math.ceil((p_fv * 1000) / m["potencia_wp"])
        print(f"{i} - {m['fabricante']} {m['modelo']} | {m['potencia_wp']:.0f} Wp | "
              f"R$ {m['preco'] / m['potencia_wp']:.2f}/Wp | N = {n}")

    while True:
        escolha = input("Digite o número do módulo ou ENTER para aceitar a sugestão: ").strip()
        if escolha == "":
            modulo = validos[0]
            break
        if escolha.isdigit() and 1 <= int(escolha) <= len(validos):
            modulo = validos[int(escolha) - 1]
            break
        print("\tOpção inválida.")

    n = math.ceil((p_fv * 1000) / modulo["potencia_wp"])
    inst = montar_instalacao(modulo, n, hsp)
    exibir_instalacao(inst)
    return inst

def escolher_armazenamento():
    print("\n\t- ARMAZENAMENTO POR BATERIAS")

    opcao = pedir_campo(
        "O sistema terá baterias? (com/sem): ",
        validar_com_sem,
        "Opção inválida! Digite 'com' ou 'sem'.").strip().lower()

    if opcao == "sem":
        print("\tSISTEMA SEM BATERIA (custo de baterias = 0; etapas de bateria puladas)")
        return {"com_bateria": False, "autonomia_h": 0, "custo_baterias": 0.0}

    autonomia = converter_numero(pedir_campo(
        "Autonomia desejada (em horas): ",
        validar_decimal_positivo,
        "Autonomia inválida! Digite um número maior que zero."))

    return {"com_bateria": True, "autonomia_h": autonomia, "custo_baterias": None}

def configurar_strings(inv, modulo, n):
    min_serie = math.ceil(inv["mppt_min_v"] / modulo["vmp_v"])
    max_serie = math.floor(inv["tensao_max_v"] / modulo["voc_v"])

    if max_serie < 1 or min_serie > max_serie:
        return None

    melhor = None
    for n_serie in range(max_serie, min_serie - 1, -1):
        n_strings = math.ceil(n / n_serie)
        total = n_strings * n_serie
        strings_por_mppt = math.ceil(n_strings / inv["numero_mppt"])
        # Corrente de operação (Imp) comparada à corrente máxima de entrada do inversor
        corrente_mppt = strings_por_mppt * modulo["imp_a"]
        p_total_kw = total * modulo["potencia_wp"] / 1000

        if corrente_mppt > inv["corrente_max_entrada_a"]:
            continue
        if p_total_kw > inv["potencia_max_fv_kw"]:
            continue

        # menor nº de módulos extras; empate -> mais módulos em série (menos strings)
        if melhor is None or total < melhor["total"]:
            melhor = {
                "n_serie": n_serie, "n_strings": n_strings, "total": total,
                "strings_por_mppt": strings_por_mppt, "corrente_mppt": corrente_mppt,
                "p_total_kw": p_total_kw, "min_serie": min_serie, "max_serie": max_serie,
            }
    return melhor

def selecionar_inversor(inst, com_bateria):
    print("\n\t- SELEÇÃO DE INVERSOR")

    resultado = ler_csv_validado(CAMINHO_INVERSORES, COLUNAS_INVERSORES_TEXTO,
                                 COLUNAS_INVERSORES_NUM)
    if resultado is None:
        return None

    validos, invalidos = resultado
    for numero, motivo in invalidos:
        print(f"\tAviso: linha {numero} de '{CAMINHO_INVERSORES}' ignorada ({motivo}).")

    if com_bateria:  # 4.2
        validos = [i for i in validos if i["compativel_bateria"].lower() == "sim"]

    modulo = inst["modulo"]
    compativeis = []
    for inv in validos:
        config = configurar_strings(inv, modulo, inst["n_modulos"])
        if config is not None:
            compativeis.append((inv, config))  # incompatíveis descartados antes do preço

    if not compativeis:
        print("\tNenhum inversor do dataset é compatível com a configuração escolhida.")
        return None

    inv, config = min(compativeis, key=lambda x: x[0]["preco"])  # critério: menor preço

    print(f"Inversores compatíveis: {len(compativeis)} de {len(validos)} analisados")
    print(f"Inversor selecionado: {inv['fabricante']} {inv['modelo']} [id {inv['id']}]")
    print("Parâmetros comparados:")
    print(f"  - Módulos por string: {config['n_serie']} "
          f"(faixa permitida {config['min_serie']} a {config['max_serie']})")
    print(f"  - Tensão Voc da string: {config['n_serie'] * modulo['voc_v']:.1f} V "
          f"(máx. {inv['tensao_max_v']:.0f} V)")
    print(f"  - Tensão Vmp da string: {config['n_serie'] * modulo['vmp_v']:.1f} V "
          f"(MPPT mín. {inv['mppt_min_v']:.0f} V)")
    print(f"  - Strings: {config['n_strings']} em {int(inv['numero_mppt'])} MPPT(s) "
          f"-> {config['corrente_mppt']:.1f} A por MPPT "
          f"(máx. {inv['corrente_max_entrada_a']:.1f} A)")
    print(f"  - Potência FV: {config['p_total_kw']:.2f} kWp "
          f"(máx. {inv['potencia_max_fv_kw']:.2f} kW)")

    return {"inversor": inv, "configuracao": config}

def calcular_capacidade_bateria(c_m, autonomia_h):
    print("\n\t- CAPACIDADE DE ARMAZENAMENTO")

    e_d = c_m / DIAS_MES_BATERIA
    e_autonomia = e_d * (autonomia_h / 24)
    c_bat = e_autonomia / (DOD_PADRAO * EFICIENCIA_BATERIA)

    print(f"Energia diária (E_d): {e_d:.2f} kWh")
    print(f"Autonomia utilizada: {autonomia_h:.1f} h -> E_autonomia: {e_autonomia:.2f} kWh")
    print(f"Parâmetros: DoD = {DOD_PADRAO} | η_bat = {EFICIENCIA_BATERIA}")
    print(f"\tCAPACIDADE NECESSÁRIA (C_bat): {c_bat:.2f} kWh")

    return {"e_d": e_d, "e_autonomia": e_autonomia, "c_bat": c_bat,
            "dod": DOD_PADRAO, "eta_bat": EFICIENCIA_BATERIA}


# ORQUESTRAÇÃO
# -----------------------------------------
def dimensionar_fotovoltaico(usuario):
    print("\n\tDIMENSIONAMENTO FOTOVOLTAICO")

    imovel = selecionar_imovel(usuario)  # 1.2
    if imovel is None:
        return

    energia = definir_energia_mensal(imovel)  # US01
    if energia is None:
        return

    potencia = calcular_potencia_fv(imovel, energia["e_fv"])  # US02
    if potencia is None:
        return

    instalacao = selecionar_modulo(potencia["p_fv"], potencia["hsp"])  # US03
    if instalacao is None:
        return

    armazenamento = escolher_armazenamento()

    inversor = selecionar_inversor(instalacao, armazenamento["com_bateria"])  # US04
    if inversor is None:
        return

    # Se o arranjo de strings exigiu módulos extras, atualiza a instalação
    total = inversor["configuracao"]["total"]
    if total != instalacao["n_modulos"]:
        print(f"\n\tAjuste: o arranjo de strings exige {total} módulos "
              f"(dimensionado: {instalacao['n_modulos']}).")
        instalacao = montar_instalacao(instalacao["modulo"], total, potencia["hsp"])
        exibir_instalacao(instalacao)

    bateria = None
    if armazenamento["com_bateria"]:
        bateria = calcular_capacidade_bateria(energia["c_m"], armazenamento["autonomia_h"])

    imovel["proposta"] = {
        "energia": energia,
        "potencia": potencia,
        "instalacao": instalacao,
        "armazenamento": armazenamento,
        "inversor": inversor,
        "bateria": bateria,
    }

    print("\n\tDIMENSIONAMENTO CONCLUÍDO E SALVO NO IMÓVEL!")

OPCOES_QUE_ALTERAM_DADOS = ["1", "3", "4", "6", "9", "13"]

def menu(usuario, usuarios):
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
        print("13 - Dimensionamento fotovoltaico")

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
        elif opcao == "13":
            dimensionar_fotovoltaico(usuario)
        else:
            print("Opção inválida, tente novamente.")

        if opcao in OPCOES_QUE_ALTERAM_DADOS:
            salvar_dados(usuarios)


# APENAS PARA TESTE
# -----------------------------------------
def criar_csvs_exemplo():

    if not os.path.exists(CAMINHO_MODULOS):
        with open(CAMINHO_MODULOS, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "fabricante", "modelo", "potencia_wp", "preco",
                        "voc_v", "vmp_v", "imp_a"])
            w.writerow(["M01", "FabricanteA", "Mod550", 550, 650, 49.5, 41.5, 13.25])
            w.writerow(["M02", "FabricanteB", "Mod600", 600, 780, 51.0, 43.0, 13.95])

    if not os.path.exists(CAMINHO_INVERSORES):
        with open(CAMINHO_INVERSORES, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "fabricante", "modelo", "potencia_nominal_kw", "potencia_max_fv_kw",
                        "mppt_min_v", "tensao_max_v", "corrente_max_entrada_a",
                        "numero_mppt", "preco", "compativel_bateria"])
            w.writerow(["I01", "FabricanteX", "Inv5k", 5, 7.5, 80, 600, 16, 2, 3800, "nao"])
            w.writerow(["I02", "FabricanteY", "Inv10k", 10, 15, 200, 1000, 20, 2, 6500, "sim"])


# PROGRAMA PRINCIPAL
# -----------------------------------------
print("\n\t\tDIMENSIONAMENTO ENERGÉTICO E FOTOVOLTAICO RESIDENCIAL")
print("=" * 65)

# === DADOS SALVOS ===
usuarios = carregar_dados()

# === CADASTRO / LOGIN ===
usuario = tela_inicial(usuarios)

# === TESTE ===
criar_csvs_exemplo()

# === MENU ===
if usuario is not None:
    menu(usuario, usuarios)