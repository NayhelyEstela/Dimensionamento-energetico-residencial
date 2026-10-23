# IMPORTAÇÕES
# -----------------------------------------
import re  # validações
import matplotlib.pyplot as plt
import csv
import math
import os
import unicodedata
import hashlib
import secrets
import json
from datetime import datetime
import io
from contextlib import redirect_stdout

# DATASETS
# -----------------------------------------

# HSP -------------------------------------
CAMINHO_HSP = "hsp.csv"

COLUNAS_HSP_TEXTO = ["cidade", "estado"]
COLUNAS_HSP_NUM = ["hsp"]

# MODULOS ---------------------------------
CAMINHO_MODULOS = "modulos.csv"  # task 12

COLUNAS_MODULOS_TEXTO = ["id", "fabricante", "modelo", "fornecedor", "data_coleta", "url_fonte"]
COLUNAS_MODULOS_NUM = ["potencia_wp", "preco_brl", "voc_v", "isc_a", "vmp_v", "imp_a", "eficiencia_pct"]

# INVERSORES ------------------------------
CAMINHO_INVERSORES = "inversores.csv"  # task 12

COLUNAS_INVERSORES_TEXTO = ["id", "fabricante", "modelo", "tipo", "compativel_bateria", "fornecedor", "data_coleta",
                            "url_fonte"]
COLUNAS_INVERSORES_NUM = ["potencia_nominal_w", "potencia_max_fv_w", "tensao_max_entrada_v",
                          "faixa_mppt_min_v", "faixa_mppt_max_v", "corrente_max_entrada_a",
                          "numero_mppt", "tensao_bateria_min_v", "tensao_bateria_max_v", "preco_brl"]

# BATERIAS --------------------------------
CAMINHO_BATERIAS = "baterias.csv"
COLUNAS_BATERIAS_TEXTO = ["id", "fabricante", "modelo", "tecnologia", "fornecedor", "data_coleta", "url_fonte"]
COLUNAS_BATERIAS_NUM = ["tensao_nominal_v", "capacidade_ah", "capacidade_kwh", "dod_pct", "ciclos", "preco_brl"]

# PARÂMETROS (justificativas no README)
# -----------------------------------------
LIMITE_PERCENTUAL = 100  # US01: 0 < f <= 100
DIAS_GERACAO = 30  # D
EFICIENCIA_SISTEMA = 0.80  # PR (fator global de desempenho)
DIAS_MES_BATERIA = 30  # divisor de E_d
DOD_PADRAO = 0.80  # DoD usado em C_bat (US06)
EFICIENCIA_BATERIA = 0.90  # η_bat

JUSTIFICATIVA_PR = ("perdas típicas por temperatura, sujeira, cabeamento, inversor e "
                    "descasamento entre módulos (faixa usual de projeto: 0,75 a 0,85)")
RDC_AC_MIN = 0.8    # PB07: limites aceitos para a relação DC/AC
RDC_AC_MAX = 1.5
RDC_AC_IDEAL = 1.2  # usado só para ordenar as opções

NOTA_EFICIENCIA_INVERSOR = ("eficiência do inversor não consta no dataset; suas perdas "
                            "estão consideradas no PR adotado")

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
    return validar_decimal_positivo(valor)

def converter_numero(valor):
    return float(str(valor).strip().replace(",", "."))


def validar_decimal_positivo(valor):
    try:
        n = converter_numero(valor)
        return math.isfinite(n) and n > 0
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
                    permite_zero = (c in ("tensao_bateria_min_v", "tensao_bateria_max_v")
                                    and caminho.endswith("inversores.csv"))
                    if valor < 0 or (valor == 0 and not permite_zero):
                        motivo = f"campo '{c}' deve ser {'maior ou igual a zero' if permite_zero else 'maior que zero'}"
                        break
                    registro[c] = valor

            if c.endswith("_pct") and valor > 100:
                motivo = f"campo '{c}' não pode passar de 100"
                break

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
CAMINHO_PROPOSTAS = os.path.join(PASTA_DADOS, "propostas.csv")

CAMPOS_USUARIOS = ["id_usuario", "nome", "email", "senha_hash"]
CAMPOS_IMOVEIS = ["id_imovel", "id_usuario", "nome", "endereco", "cidade", "estado", "tipo"]
CAMPOS_EQUIPAMENTOS = ["id_equipamento", "id_imovel", "nome", "quantidade",
                       "potencia_watts", "horas_uso"]
CAMPOS_HISTORICO = ["id_imovel", "mes", "consumo_kwh"]
CAMPOS_PROPOSTAS = ["id_proposta", "id_imovel", "data_geracao", "proposta_json"]


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
    propostas = []
    for imovel in imoveis:
        for proposta in imovel.get("propostas", []):
            propostas.append({"id_proposta": proposta["id_proposta"], "id_imovel": imovel["id"],
                              "data_geracao": proposta["data_geracao"],
                              "proposta_json": json.dumps(proposta["dados"], ensure_ascii=False)})
    escrever_csv(CAMINHO_PROPOSTAS, CAMPOS_PROPOSTAS, propostas)


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

    for r in ler_csv_dados(CAMINHO_PROPOSTAS):
        try:
            imovel = imoveis[r["id_imovel"]]
            imovel.setdefault("propostas", []).append({
                "id_proposta": int(r["id_proposta"]), "data_geracao": r["data_geracao"],
                "dados": json.loads(r["proposta_json"])})
        except (KeyError, ValueError, json.JSONDecodeError):
            print(f"\tAviso: linha inválida em '{CAMINHO_PROPOSTAS}' ignorada.")

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
        "potencia_watts": converter_numero(potencia),
        "horas_uso": converter_numero(horas_uso)
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
    equipamento["horas_uso"] = converter_numero(novas_horas)

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

def calcular_potencia_instalada_residencia(imovel):
    return sum(e["potencia_watts"] * e["quantidade"] for e in imovel["equipamentos"]) / 1000  # kW

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

    p_res_kw = calcular_potencia_instalada_residencia(imovel)
    print(f"Consumo de referência (C_m): {c_m:.2f} kWh/mês")
    print(f"Consumo médio diário (E_dia = C_m / {DIAS_MES}): {c_m / DIAS_MES:.2f} kWh/dia")
    print(f"Potência instalada da residência: {p_res_kw:.2f} kW")
    print(f"Origem do C_m: {origem}")

    f = converter_numero(pedir_campo(
        f"Percentual do consumo a atender com energia solar (0 < f <= {LIMITE_PERCENTUAL}): ",
        validar_percentual,
        f"Percentual inválido! Digite um número maior que 0 e no máximo {LIMITE_PERCENTUAL} "
        f"(pode usar vírgula)."))

    e_fv = c_m * (f / 100)
    print(f"\tENERGIA A GERAR (E_FV): {e_fv:.2f} kWh/mês")

    return {"c_m": c_m, "origem_c_m": origem, "percentual": f, "e_fv": e_fv,
            "e_dia": c_m / DIAS_MES, "p_residencia_kw": p_res_kw}


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
        return registro["hsp"], "hsp.csv"

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

    if not 0 < EFICIENCIA_SISTEMA <= 1:
        print("\tPR inválido: deve ser maior que 0 e no máximo 1. Ajuste EFICIENCIA_SISTEMA.")
        return None

    resultado = obter_hsp(imovel)
    if resultado is None:
        print("\tDimensionamento abortado: não há dado de irradiação (HSP) para o imóvel.")
        return None

    hsp, origem = resultado
    p_fv = e_fv / (hsp * DIAS_GERACAO * EFICIENCIA_SISTEMA)

    print(f"HSP utilizado: {hsp:.2f} kWh/m²/dia (fonte: {origem})")
    print(f"PR adotado: {EFICIENCIA_SISTEMA:.2f} — {JUSTIFICATIVA_PR}")
    print(f"Energia diária a gerar: {e_fv / DIAS_GERACAO:.2f} kWh/dia | D = {DIAS_GERACAO} dias")
    print(f"\tPOTÊNCIA NECESSÁRIA (P_FV): {p_fv:.2f} kWp")

    return {"hsp": hsp, "p_fv": p_fv, "pr": EFICIENCIA_SISTEMA}


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
    print(f"Geração estimada: {inst['geracao_estimada'] / DIAS_GERACAO:.2f} kWh/dia")
    print(f"\tGERAÇÃO ESTIMADA: {inst['geracao_estimada']:.2f} kWh/mês")


def selecionar_modulo(p_fv, hsp, modulos_excluidos=None):
    print("\n\t- SELEÇÃO DE MÓDULOS")

    resultado = ler_csv_validado(CAMINHO_MODULOS, COLUNAS_MODULOS_TEXTO, COLUNAS_MODULOS_NUM)
    if resultado is None:
        return None

    validos, invalidos = resultado
    for m in validos:
        m["preco"] = m.pop("preco_brl")
    for numero, motivo in invalidos:
        print(f"\tAviso: linha {numero} de '{CAMINHO_MODULOS}' ignorada ({motivo}).")

    if modulos_excluidos:
        validos = [m for m in validos if m["id"] not in modulos_excluidos]
    if not validos:
        print("\tLimitação: não há módulos válidos disponíveis para testar outra combinação.")
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
    # (a) Vmp da string também precisa respeitar o MPPT máximo
    max_serie = min(math.floor(inv["tensao_max_v"] / modulo["voc_v"]),
                    math.floor(inv["mppt_max_v"] / modulo["vmp_v"]))

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

        r_dc_ac = p_total_kw / inv["potencia_nominal_kw"]
        if not RDC_AC_MIN <= r_dc_ac <= RDC_AC_MAX:
            continue

        # menor nº de módulos extras; empate -> mais módulos em série (menos strings)
        if melhor is None or total < melhor["total"]:
            melhor = {
                "n_serie": n_serie, "n_strings": n_strings, "total": total,
                "strings_por_mppt": strings_por_mppt, "corrente_mppt": corrente_mppt,
                "p_total_kw": p_total_kw, "min_serie": min_serie, "max_serie": max_serie,
                "r_dc_ac": r_dc_ac,
            }
    return melhor


def selecionar_inversor(inst, com_bateria, inversores_excluidos=None, automatico=False):
    print("\n\t- SELEÇÃO DE INVERSOR")

    resultado = ler_csv_validado(CAMINHO_INVERSORES, COLUNAS_INVERSORES_TEXTO,
                                 COLUNAS_INVERSORES_NUM)
    if resultado is None:
        return None

    validos, invalidos = resultado
    for inv in validos:
        inv["potencia_nominal_kw"] = inv.pop("potencia_nominal_w") / 1000
        inv["potencia_max_fv_kw"] = inv.pop("potencia_max_fv_w") / 1000

        inv["mppt_max_v"] = inv.pop("faixa_mppt_max_v")

        inv["mppt_min_v"] = inv.pop("faixa_mppt_min_v")
        inv["tensao_max_v"] = inv.pop("tensao_max_entrada_v")
        inv["preco"] = inv.pop("preco_brl")
        inv["numero_mppt"] = int(inv["numero_mppt"])

    for numero, motivo in invalidos:
        print(f"\tAviso: linha {numero} de '{CAMINHO_INVERSORES}' ignorada ({motivo}).")

    if com_bateria:  # 4.2
        validos = [i for i in validos if i["compativel_bateria"].lower() == "sim"]
    if inversores_excluidos:
        validos = [i for i in validos if i["id"] not in inversores_excluidos]

    modulo = inst["modulo"]
    compativeis = []
    for inv in validos:
        config = configurar_strings(inv, modulo, inst["n_modulos"])
        if config is not None:
            compativeis.append((inv, config))  # incompatíveis descartados antes do preço

    if not compativeis:
        print("\tNenhum inversor do dataset é compatível com a configuração escolhida.")
        return None

    compativeis.sort(key=lambda x: (abs(x[1]["r_dc_ac"] - RDC_AC_IDEAL), x[0]["preco"]))

    print(f"Inversores compatíveis: {len(compativeis)} de {len(validos)} analisados")
    print("Ordenados por R_DC/AC mais próximo do ideal e, em empate, menor preço (o 1 é a sugestão):")
    for i, (cand, cfg) in enumerate(compativeis, start=1):
        print(f"{i} - {cand['fabricante']} {cand['modelo']} | {cand['potencia_nominal_kw']:.2f} kW | "
              f"R_DC/AC {cfg['r_dc_ac']:.2f} | R$ {cand['preco']:,.2f}")

    while True:
        escolha = "" if automatico else input("Digite o número do inversor ou ENTER para aceitar a sugestão: ").strip()
        if escolha == "":
            inv, config = compativeis[0]
            break
        if escolha.isdigit() and 1 <= int(escolha) <= len(compativeis):
            inv, config = compativeis[int(escolha) - 1]
            break
        print("\tOpção inválida.")

    print(f"Inversor selecionado: {inv['fabricante']} {inv['modelo']} [id {inv['id']}]")
    print("Parâmetros comparados:")
    print(f"  - Módulos por string: {config['n_serie']} "
          f"(faixa permitida {config['min_serie']} a {config['max_serie']})")
    print(f"  - Tensão Voc da string: {config['n_serie'] * modulo['voc_v']:.1f} V "
          f"(máx. {inv['tensao_max_v']:.0f} V)")
    print(f"  - Tensão Vmp da string: {config['n_serie'] * modulo['vmp_v']:.1f} V "
          f"(faixa MPPT {inv['mppt_min_v']:.0f} a {inv['mppt_max_v']:.0f} V)")
    print(f"  - Relação DC/AC: {config['r_dc_ac']:.2f} "
          f"({config['p_total_kw']:.2f} kWp / {inv['potencia_nominal_kw']:.2f} kW)")
    print(f"  - Eficiência: {NOTA_EFICIENCIA_INVERSOR}")
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
def selecionar_bateria(c_bat, inversor, automatico=False):
    """US07: escolhe a bateria compatível de menor custo por kWh útil."""
    print("\n\t- SELEÇÃO DE BATERIAS")
    resultado = ler_csv_validado(CAMINHO_BATERIAS, COLUNAS_BATERIAS_TEXTO, COLUNAS_BATERIAS_NUM)
    if resultado is None:
        return None
    validos, invalidos = resultado
    for numero, motivo in invalidos:
        print(f"\tAviso: linha {numero} de '{CAMINHO_BATERIAS}' ignorada ({motivo}).")

    inv = inversor["inversor"]
    candidatos = []
    for bat in validos:
        bat["preco"] = bat.pop("preco_brl")
        bat["capacidade_util_kwh"] = bat["capacidade_kwh"] * bat["dod_pct"] / 100
        # A compatibilidade é limitada pela faixa de tensão declarada pelo inversor.
        if not (inv["tensao_bateria_min_v"] <= bat["tensao_nominal_v"] <= inv["tensao_bateria_max_v"]):
            continue
        bat["n_baterias"] = math.ceil(c_bat / bat["capacidade_kwh"])
        bat["capacidade_instalada_kwh"] = bat["n_baterias"] * bat["capacidade_kwh"]
        bat["capacidade_util_instalada_kwh"] = bat["n_baterias"] * bat["capacidade_util_kwh"]
        bat["custo_total"] = bat["n_baterias"] * bat["preco"]
        bat["custo_por_kwh_util"] = bat["preco"] / bat["capacidade_util_kwh"]
        candidatos.append(bat)

    if not candidatos:
        print("Nenhuma bateria do dataset é compatível com a tensão do inversor selecionado.")
        print(f"Conflito: tensão nominal da bateria deve estar entre "
              f"{inv['tensao_bateria_min_v']:.1f} V e {inv['tensao_bateria_max_v']:.1f} V; "
              "as baterias disponíveis ficaram fora desse limite.")
        for bat in validos:
            if not (inv["tensao_bateria_min_v"] <= bat["tensao_nominal_v"] <= inv["tensao_bateria_max_v"]):
                print(f"  - {bat['id']} {bat['fabricante']} {bat['modelo']}: "
                      f"{bat['tensao_nominal_v']:.1f} V (fora da faixa)")
        return None

    candidatos.sort(key=lambda b: (b["custo_por_kwh_util"], b["custo_total"]))
    print("Baterias compatíveis (ordenadas pelo menor custo por kWh útil):")
    for idx, bat in enumerate(candidatos, 1):
        print(f"{idx} - {bat['fabricante']} {bat['modelo']} | {bat['tensao_nominal_v']:.1f} V | "
              f"útil/unidade {bat['capacidade_util_kwh']:.2f} kWh | "
              f"R$ {bat['custo_por_kwh_util']:.2f}/kWh útil | {bat['n_baterias']} un. | "
              f"total R$ {bat['custo_total']:.2f}")
    while True:
        escolha = "" if automatico else input("Escolha uma bateria ou ENTER para aceitar a sugestão: ").strip()
        if not escolha:
            selecionada = candidatos[0]
            break
        if escolha.isdigit() and 1 <= int(escolha) <= len(candidatos):
            selecionada = candidatos[int(escolha) - 1]
            break
        print("\tOpção inválida.")
    print(f"Selecionada: {selecionada['fabricante']} {selecionada['modelo']} — "
          f"{selecionada['n_baterias']} unidade(s), "
          f"{selecionada['capacidade_instalada_kwh']:.2f} kWh nominais / "
          f"{selecionada['capacidade_util_instalada_kwh']:.2f} kWh úteis.")
    return selecionada

def pedir_tarifa():
    return converter_numero(pedir_campo(
        "Para posterior análise, insira, por favor, a tarifa de energia elétrica (R$/kWh, ex: 0,95): ",
        validar_decimal_positivo,
        "Tarifa inválida! Digite um número maior que zero."))

def calcular_economia(energia, instalacao, tarifa):
    """PB09/PB15: atendimento real, energia compensada e economia."""
    geracao = instalacao["geracao_estimada"]
    consumo = energia["c_m"]  # sempre > 0 aqui (obter_consumo_referencia garante)
    compensada = min(geracao, consumo)
    economia_mensal = compensada * tarifa
    return {
        "tarifa": tarifa,
        "consumo_mensal": consumo,
        "geracao_mensal": geracao,
        "atendimento_pct": geracao / consumo * 100,
        "compensada": compensada,
        "excedente": max(geracao - consumo, 0),
        "economia_mensal": economia_mensal,
        "economia_anual": economia_mensal * 12,
    }

def exibir_resumo_proposta(imovel, proposta):
    """US09/US10: custos rastreáveis e resumo consolidado."""
    energia, potencia = proposta["energia"], proposta["potencia"]
    inst, inv = proposta["instalacao"], proposta["inversor"]["inversor"]
    modulo = inst["modulo"]
    bateria = proposta.get("bateria")
    c_modulos = modulo["preco"] * inst["n_modulos"]
    c_inversor = inv["preco"]
    c_baterias = bateria["custo_total"] if bateria else 0.0
    c_equipamentos = c_modulos + c_inversor + c_baterias
    # Estimativa acadêmica: 20% para BOS/instalação, explicitamente separada.
    percentual_demais = 0.20
    c_demais = c_equipamentos * percentual_demais
    c_total = c_equipamentos + c_demais
    proposta["custos"] = {
        "modulos": c_modulos, "inversor": c_inversor, "baterias": c_baterias,
        "equipamentos": c_equipamentos, "percentual_demais": percentual_demais,
        "demais": c_demais, "total": c_total,
        "itens": [
                     {"id": modulo["id"], "tipo": "módulo", "fabricante": modulo["fabricante"],
                      "modelo": modulo["modelo"], "quantidade": inst["n_modulos"],
                      "preco_unitario_brl": modulo["preco"], "fornecedor": modulo.get("fornecedor", ""),
                      "data_coleta": modulo.get("data_coleta", ""), "url_fonte": modulo.get("url_fonte", "")},
                     {"id": inv["id"], "tipo": "inversor", "fabricante": inv["fabricante"],
                      "modelo": inv["modelo"], "quantidade": 1, "preco_unitario_brl": c_inversor,
                      "fornecedor": inv.get("fornecedor", ""), "data_coleta": inv.get("data_coleta", ""),
                      "url_fonte": inv.get("url_fonte", "")}
                 ] + ([{"id": bateria["id"], "tipo": "bateria", "fabricante": bateria["fabricante"],
                        "modelo": bateria["modelo"], "quantidade": bateria["n_baterias"],
                        "preco_unitario_brl": bateria["preco"], "fornecedor": bateria.get("fornecedor", ""),
                        "data_coleta": bateria.get("data_coleta", ""),
                        "url_fonte": bateria.get("url_fonte", "")}] if bateria else [])
    }
    print("\n" + "=" * 58)
    print("RESUMO DA PROPOSTA FOTOVOLTAICA")
    print("=" * 58)
    print(f"Imóvel: {imovel['nome']} ({imovel.get('cidade', '')}/{imovel.get('estado', '')})")
    print(f"Consumo de referência: {energia['c_m']:.2f} kWh/mês — {energia['origem_c_m']}")
    print(f"Consumo médio diário: {energia.get('e_dia', energia['c_m'] / DIAS_MES):.2f} kWh/dia")
    if energia.get("p_residencia_kw") is not None:
        print(f"Potência instalada da residência: {energia['p_residencia_kw']:.2f} kW")
    print(f"Atendimento desejado: {energia['percentual']:.1f}% | Energia FV: {energia['e_fv']:.2f} kWh/mês")
    print(f"HSP: {potencia['hsp']:.3f} kWh/m²/dia (origem: {potencia.get('origem_hsp', 'dataset hsp.csv')})")
    print(f"PR adotado: {potencia.get('pr', EFICIENCIA_SISTEMA):.2f} — {JUSTIFICATIVA_PR}")
    print(f"Potência necessária: {potencia['p_fv']:.2f} kWp | instalada: {inst['p_instalada']:.2f} kWp")
    print(f"Módulos: {inst['n_modulos']} × {modulo['fabricante']} {modulo['modelo']}")
    print(f"Inversor: {inv['fabricante']} {inv['modelo']} (id {inv['id']})")
    rdc = proposta["inversor"]["configuracao"].get("r_dc_ac")
    if rdc is not None:
        print(f"Relação DC/AC: {rdc:.2f} | {NOTA_EFICIENCIA_INVERSOR}")
    print(f"Geração estimada: {inst['geracao_estimada'] / DIAS_GERACAO:.2f} kWh/dia | "
          f"{inst['geracao_estimada']:.2f} kWh/mês")
    if bateria:
        print(f"Armazenamento: com bateria | autonomia {proposta['armazenamento']['autonomia_h']:.1f} h")
        print(f"Energia necessária para a autonomia: {proposta['capacidade_bateria']['e_autonomia']:.2f} kWh")
        print(f"Capacidade necessária: {proposta['capacidade_bateria']['c_bat']:.2f} kWh | "
              f"capacidade instalada: {bateria['capacidade_instalada_kwh']:.2f} kWh nominais "
              f"({bateria['capacidade_util_instalada_kwh']:.2f} kWh úteis)")
    else:
        print("Armazenamento: sem bateria")
    print("\nORÇAMENTO"
          "\n(item | fabricante/modelo | qtd | preço unit. | subtotal)")
    for item in proposta["custos"]["itens"]:
        subtotal = item["quantidade"] * item["preco_unitario_brl"]
        print(f"- {item['tipo']} | {item['fabricante']} {item['modelo']} | {item['quantidade']} | "
              f"R$ {item['preco_unitario_brl']:,.2f} | R$ {subtotal:,.2f}")
    print(f"Custo dos equipamentos: R$ {c_equipamentos:,.2f}")
    print(f"Demais custos estimados (estrutura, cabos, proteções e instalação; 20%): R$ {c_demais:,.2f}")
    print(f"CUSTO TOTAL ESTIMADO: R$ {c_total:,.2f}")
    print("\nRastreabilidade dos itens:")
    for item in proposta["custos"]["itens"]:
        print(f"- {item['tipo']}: id {item['id']} | fornecedor {item['fornecedor']} | "
              f"coleta {item['data_coleta']} | R$ {item['preco_unitario_brl']:,.2f}/un.")
        print(f"  Fonte: {item['url_fonte']}")

    eco = proposta.get("economia")
    if eco:
        print("\nGERAÇÃO × CONSUMO")
        print(f"Consumo mensal: {eco['consumo_mensal']:.2f} kWh | "
              f"Geração mensal: {eco['geracao_mensal']:.2f} kWh")
        print(f"ATENDIMENTO: {eco['atendimento_pct']:.1f}%")
        if eco["excedente"] > 0:
            print(f"A geração supera o consumo: {eco['compensada']:.2f} kWh efetivamente "
                  f"consumidos/compensados e {eco['excedente']:.2f} kWh de excedente gerado.")

        print("\nESTIMATIVA DE ECONOMIA")
        print(f"Tarifa utilizada: R$ {eco['tarifa']:.2f}/kWh")
        print(f"Energia compensada: {eco['compensada']:.2f} kWh/mês")
        print(f"Economia mensal: R$ {eco['economia_mensal']:,.2f}")
        print(f"Economia anual: R$ {eco['economia_anual']:,.2f}")
        print("Premissas: tarifa constante (sem reajuste), compensação limitada ao consumo, "
              "sem taxa de disponibilidade, sem degradação dos módulos.")
        if eco["economia_anual"] > 0:
            eco["payback_anos"] = c_total / eco["economia_anual"]
            print(f"PAYBACK SIMPLES: {eco['payback_anos']:.1f} anos "
                  f"({eco['payback_anos'] * 12:.0f} meses) — estimativa simples, "
                  "não é previsão financeira exata.")
        else:
            print("Payback simples não calculável: a economia anual estimada é zero.")
    print("\nAVISO: pré-dimensionamento acadêmico. Não substitui projeto executivo, "
          "ART, vistoria, análise de sombreamento ou validação por profissional habilitado.")
    print("=" * 58)

def completar_proposta(energia, potencia, instalacao, armazenamento, inversor, tarifa, automatico=False):
    """Do ajuste de strings até o dicionário da proposta (usada nos dois cenários)."""
    inversores_excluidos = set()
    total = inversor["configuracao"]["total"]
    if total != instalacao["n_modulos"]:
        print(f"\n\tAjuste de strings: arranjo exige {total} módulos "
              f"(dimensionamento inicial: {instalacao['n_modulos']}).")
        instalacao = montar_instalacao(instalacao["modulo"], total, potencia["hsp"])
        exibir_instalacao(instalacao)
    capacidade_bateria = None
    bateria = None
    if armazenamento["com_bateria"]:
        capacidade_bateria = calcular_capacidade_bateria(energia["c_m"], armazenamento["autonomia_h"])
        while True:
            bateria = selecionar_bateria(capacidade_bateria["c_bat"], inversor, automatico)
            if bateria is not None:
                break
            inversores_excluidos.add(inversor["inversor"]["id"])
            print("Tentando outra combinação de inversor e bateria (US08)...")
            inversor = selecionar_inversor(instalacao, True, inversores_excluidos, automatico)
            if inversor is None:
                print("Proposta não gerada: não existe combinação válida de inversor e bateria. "
                      "Revise os datasets ou escolha sem bateria.")
                return None
            total = inversor["configuracao"]["total"]
            if total != instalacao["n_modulos"]:
                instalacao = montar_instalacao(instalacao["modulo"], total, potencia["hsp"])
                exibir_instalacao(instalacao)
        armazenamento["custo_baterias"] = bateria["custo_total"]
    return {
        "energia": energia, "potencia": potencia, "instalacao": instalacao,
        "armazenamento": armazenamento, "inversor": inversor, "bateria": bateria,
        "capacidade_bateria": capacidade_bateria,
        "economia": calcular_economia(energia, instalacao, tarifa),
        "data_geracao": datetime.now().isoformat(timespec="seconds")
    }


def gerar_cenario_alternativo(proposta_base, tarifa):
    """PB14: refaz o dimensionamento com a escolha oposta (com/sem bateria)."""
    energia, potencia = proposta_base["energia"], proposta_base["potencia"]
    com_bateria = not proposta_base["armazenamento"]["com_bateria"]
    print(f"\n\tCENÁRIO ALTERNATIVO: {'COM' if com_bateria else 'SEM'} BATERIA")
    if com_bateria:
        autonomia = converter_numero(pedir_campo(
            "Autonomia desejada (em horas): ", validar_decimal_positivo,
            "Autonomia inválida! Digite um número maior que zero."))
        armazenamento = {"com_bateria": True, "autonomia_h": autonomia, "custo_baterias": None}
    else:
        armazenamento = {"com_bateria": False, "autonomia_h": 0, "custo_baterias": 0.0}
    modulo = proposta_base["instalacao"]["modulo"]
    n = math.ceil((potencia["p_fv"] * 1000) / modulo["potencia_wp"])
    instalacao = montar_instalacao(modulo, n, potencia["hsp"])
    inversor = selecionar_inversor(instalacao, com_bateria, automatico=True)
    if inversor is None:
        print("Cenário alternativo não gerado: nenhum inversor compatível com o módulo escolhido.")
        return None
    return completar_proposta(energia, potencia, instalacao, armazenamento, inversor, tarifa, automatico=True)


def registrar_proposta(usuario, imovel, proposta):
    imovel.setdefault("propostas", [])
    novo_id = max((p.get("id_proposta", 0) for i in usuario["imoveis"]
                   for p in i.get("propostas", [])), default=0) + 1
    imovel["propostas"].append({"id_proposta": novo_id, "data_geracao": proposta["data_geracao"],
                                "dados": proposta})
    print(f"\nProposta #{novo_id} salva em '{CAMINHO_PROPOSTAS}'.")
    return novo_id


def exibir_comparativo(a, b):
    """PB14: os dois cenários lado a lado (exige exibir_resumo_proposta já chamado em ambos)."""
    sem, com = (b, a) if a["armazenamento"]["com_bateria"] else (a, b)

    def linhas(p):
        inst, inv = p["instalacao"], p["inversor"]["inversor"]
        bat, eco = p.get("bateria"), p["economia"]
        payback = eco.get("payback_anos")
        return [
            ("Potência FV necessária", f"{p['potencia']['p_fv']:.2f} kWp"),
            ("Potência FV instalada", f"{inst['p_instalada']:.2f} kWp"),
            ("Módulos", f"{inst['n_modulos']} × {inst['modulo']['modelo']}"),
            ("Inversor", f"{inv['fabricante']} {inv['modelo']}"),
            ("Geração mensal", f"{inst['geracao_estimada']:.2f} kWh"),
            ("Atendimento", f"{eco['atendimento_pct']:.1f}%"),
            ("Armazenamento", f"{bat['n_baterias']} × {bat['modelo']}" if bat else "sem bateria"),
            ("Capacidade instalada", f"{bat['capacidade_instalada_kwh']:.2f} kWh" if bat else "—"),
            ("Autonomia", f"{p['armazenamento']['autonomia_h']:.1f} h" if bat else "—"),
            ("Investimento total", f"R$ {p['custos']['total']:,.2f}"),
            ("Economia anual", f"R$ {eco['economia_anual']:,.2f}"),
            ("Payback simples", f"{payback:.1f} anos" if payback else "—"),
        ]

    print("\n" + "=" * 80)
    print("COMPARAÇÃO DOS CENÁRIOS")
    print("=" * 80)
    print(f"{'':<24}{'SEM BATERIA':<28}{'COM BATERIA':<28}")
    for (rotulo, v_sem), (_, v_com) in zip(linhas(sem), linhas(com)):
        print(f"{rotulo:<24}{v_sem[:27]:<28}{v_com[:27]:<28}")
    print(f"\nCusto adicional do armazenamento: R$ {com['custos']['total'] - sem['custos']['total']:,.2f}")
    print("Obs.: a economia considera só a energia solar compensada; a bateria não gera "
          "economia adicional neste modelo.")
    print("=" * 80)

def exportar_propostas(imovel, propostas):
    """PB21: grava o(s) resumo(s) e o comparativo em um arquivo de texto."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):  # reaproveita o que já é impresso na tela
        for p in propostas:
            exibir_resumo_proposta(imovel, p)
        if len(propostas) == 2:
            exibir_comparativo(propostas[0], propostas[1])
    nome = re.sub(r"\W+", "_", normalizar(imovel["nome"])).strip("_")
    caminho = f"proposta_{nome}_{datetime.now():%Y%m%d_%H%M%S}.txt"
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(buffer.getvalue())
    print(f"\tProposta exportada em: {caminho}")

def dimensionar_fotovoltaico(usuario):
    print("\n\tDIMENSIONAMENTO FOTOVOLTAICO")
    imovel = selecionar_imovel(usuario)
    if imovel is None:
        return
    energia = definir_energia_mensal(imovel)
    if energia is None:
        return
    potencia = calcular_potencia_fv(imovel, energia["e_fv"])
    if potencia is None:
        return
    # Mantém a origem do HSP no estado da proposta.
    reg_hsp = buscar_hsp(imovel["cidade"], imovel["estado"])
    potencia["origem_hsp"] = "hsp.csv (normais climatológicas municipais)" if reg_hsp else "manual"
    instalacao = selecionar_modulo(potencia["p_fv"], potencia["hsp"])
    if instalacao is None:
        return
    armazenamento = escolher_armazenamento()
    inversores_excluidos = set()
    modulos_excluidos = set()
    inversor = selecionar_inversor(instalacao, armazenamento["com_bateria"])
    while inversor is None:
        modulos_excluidos.add(instalacao["modulo"]["id"])
        print("Tentando outra combinação com um módulo diferente (US08)...")
        nova_instalacao = selecionar_modulo(potencia["p_fv"], potencia["hsp"], modulos_excluidos)
        if nova_instalacao is None:
            print("Proposta não gerada: nenhum conjunto módulo/inversor compatível foi encontrado.")
            return
        instalacao = nova_instalacao
        inversores_excluidos.clear()
        inversor = selecionar_inversor(instalacao, armazenamento["com_bateria"])
    tarifa = pedir_tarifa()
    proposta = completar_proposta(energia, potencia, instalacao, armazenamento, inversor, tarifa)
    if proposta is None:
        return
    exibir_resumo_proposta(imovel, proposta)
    registrar_proposta(usuario, imovel, proposta)
    propostas = [proposta]

    if input("\nGerar o cenário alternativo (com/sem bateria) para comparação? (s/n): ").strip().lower() == "s":
        alternativa = gerar_cenario_alternativo(proposta, tarifa)
        if alternativa is not None:
            exibir_resumo_proposta(imovel, alternativa)
            registrar_proposta(usuario, imovel, alternativa)
            exibir_comparativo(proposta, alternativa)
            propostas.append(alternativa)

    if input("\nExportar a proposta para arquivo de texto? (s/n): ").strip().lower() == "s":
        exportar_propostas(imovel, propostas)
    input("Pressione ENTER para voltar ao menu principal...")

OPCOES_QUE_ALTERAM_DADOS = ["1", "3", "4", "6", "9", "13"]

def ver_propostas_salvas(usuario):
    print("\n\tPROPOSTAS SALVAS")
    imovel = selecionar_imovel(usuario)
    if imovel is None:
        return
    propostas = imovel.get("propostas", [])
    if not propostas:
        print("Nenhuma proposta salva para este imóvel.")
        return
    for p in propostas:
        tipo = "com bateria" if p["dados"]["armazenamento"]["com_bateria"] else "sem bateria"
        print(f"#{p['id_proposta']} - {p['data_geracao']} - {tipo}")
    escolha = input("Digite o número da proposta (sem o #) ou ENTER para voltar: ").strip()
    if not escolha:
        return
    selecionada = next((p for p in propostas if str(p["id_proposta"]) == escolha), None)
    if selecionada is None:
        print("\tProposta não encontrada.")
        return
    exibir_resumo_proposta(imovel, selecionada["dados"])
    if input("Exportar esta proposta para arquivo de texto? (s/n): ").strip().lower() == "s":
        exportar_propostas(imovel, [selecionada["dados"]])

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
        print("14 - Ver propostas salvas")

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
        elif opcao == "14":
            ver_propostas_salvas(usuario)
        else:
            print("Opção inválida, tente novamente.")

        if opcao in OPCOES_QUE_ALTERAM_DADOS:
            salvar_dados(usuarios)

# PROGRAMA PRINCIPAL
# -----------------------------------------
print("\n\t\tDIMENSIONAMENTO ENERGÉTICO E FOTOVOLTAICO RESIDENCIAL")
print("=" * 65)

# === DADOS SALVOS ===
usuarios = carregar_dados()

# === CADASTRO / LOGIN ===
usuario = tela_inicial(usuarios)

# === MENU ===
if usuario is not None:
    menu(usuario, usuarios)
