"""Valida os datasets fotovoltaicos antes de usá-los no dimensionamento."""
import csv
import sys
from pathlib import Path

MINIMOS = {"modulos.csv": 10, "inversores.csv": 8, "baterias.csv": 6}
CAMPOS = {
    "modulos.csv": ["id", "fabricante", "modelo", "potencia_wp", "voc_v", "isc_a", "vmp_v", "imp_a",
                    "eficiencia_pct", "preco_brl", "fornecedor", "data_coleta", "url_fonte"],
    "inversores.csv": ["id", "fabricante", "modelo", "tipo", "potencia_nominal_w", "potencia_max_fv_w",
                       "tensao_max_entrada_v", "faixa_mppt_min_v", "faixa_mppt_max_v", "corrente_max_entrada_a",
                       "numero_mppt", "compativel_bateria", "tensao_bateria_min_v", "tensao_bateria_max_v",
                       "preco_brl", "fornecedor", "data_coleta", "url_fonte"],
    "baterias.csv": ["id", "fabricante", "modelo", "tecnologia", "tensao_nominal_v", "capacidade_ah",
                     "capacidade_kwh", "dod_pct", "ciclos", "preco_brl", "fornecedor", "data_coleta", "url_fonte"],
}
NUMERICOS = {
    "modulos.csv": ["potencia_wp", "voc_v", "isc_a", "vmp_v", "imp_a", "eficiencia_pct", "preco_brl"],
    "inversores.csv": ["potencia_nominal_w", "potencia_max_fv_w", "tensao_max_entrada_v", "faixa_mppt_min_v",
                       "faixa_mppt_max_v", "corrente_max_entrada_a", "numero_mppt", "tensao_bateria_min_v",
                       "tensao_bateria_max_v", "preco_brl"],
    "baterias.csv": ["tensao_nominal_v", "capacidade_ah", "capacidade_kwh", "dod_pct", "ciclos", "preco_brl"],
}
OPCIONAIS = {"obs"}
erros = []


def err(arq, id_, msg):
    erros.append(f"{arq} [{id_}]: {msg}")


def coerencia(arq, r):
    n = {c: float(r[c]) for c in NUMERICOS[arq]}
    ident = r["id"]
    if arq == "modulos.csv":
        if not n["vmp_v"] < n["voc_v"]:
            err(arq, ident, "Vmp deve ser < Voc")
        if not n["imp_a"] < n["isc_a"]:
            err(arq, ident, "Imp deve ser < Isc")
        if abs(n["vmp_v"] * n["imp_a"] - n["potencia_wp"]) / n["potencia_wp"] > 0.03:
            err(arq, ident, "Vmp × Imp difere de Pmax em mais de 3%")
    elif arq == "inversores.csv":
        if not n["faixa_mppt_min_v"] < n["faixa_mppt_max_v"] <= n["tensao_max_entrada_v"]:
            err(arq, ident, "faixa MPPT incoerente com tensão máxima")
        if r["tipo"].lower() == "híbrido" and r["compativel_bateria"].lower() != "sim":
            err(arq, ident, "híbrido deveria ter compativel_bateria = sim")
        if r["compativel_bateria"].lower() == "sim" and not 0 < n["tensao_bateria_min_v"] < n["tensao_bateria_max_v"]:
            err(arq, ident, "faixa de tensão da bateria inválida")
        if r["compativel_bateria"].lower() not in ("sim", "nao"):
            err(arq, ident, "compativel_bateria deve ser sim/nao")
        if n["numero_mppt"] != int(n["numero_mppt"]):
            err(arq, ident, "numero_mppt deve ser inteiro")
    else:
        kwh = n["tensao_nominal_v"] * n["capacidade_ah"] / 1000
        if abs(kwh - n["capacidade_kwh"]) / kwh > 0.05:
            err(arq, ident, f"capacidade_kwh difere de V × Ah / 1000 ({kwh:.2f}) em mais de 5%")
        if not 0 < n["dod_pct"] <= 100:
            err(arq, ident, "DoD fora de (0, 100]")


for arq, minimo in MINIMOS.items():
    caminho = Path(__file__).resolve().parent / arq
    try:
        with caminho.open(newline="", encoding="utf-8-sig") as f:
            leitor = csv.DictReader(f)
            linhas = list(leitor)
            faltando = [c for c in CAMPOS[arq] if c not in (leitor.fieldnames or [])]
            if faltando:
                err(arq, "-", "colunas ausentes: " + ", ".join(faltando))
                continue
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        err(arq, "-", f"não foi possível ler o arquivo: {exc}")
        continue

    if len(linhas) < minimo:
        err(arq, "-", f"{len(linhas)} itens; mínimo exigido {minimo}")
    ids = [l.get("id", "") for l in linhas]
    if len(ids) != len(set(ids)):
        err(arq, "-", "ids duplicados")
    for linha in linhas:
        ident = linha.get("id", "?")
        for campo in CAMPOS[arq]:
            valor = linha.get(campo)
            if valor is None or not valor.strip():
                err(arq, ident, f"campo obrigatório '{campo}' vazio")
        try:
            for campo in NUMERICOS[arq]:
                valor = float(linha[campo])
                permite_zero = arq == "inversores.csv" and campo in ("tensao_bateria_min_v", "tensao_bateria_max_v") and linha.get("compativel_bateria", "").lower() == "nao"
                if valor < 0 or (valor == 0 and not permite_zero):
                    err(arq, ident, f"campo '{campo}' deve ser {'>= 0' if permite_zero else '> 0'}")
                    raise ValueError
        except (ValueError, KeyError):
            err(arq, ident, "campo numérico inválido")
            continue
        coerencia(arq, linha)
    print(f"{arq}: {len(linhas)} itens (mínimo {minimo})")

if erros:
    print("\nERROS:")
    for erro in erros:
        print(" -", erro)
    sys.exit(1)
print("\nTodos os datasets atendem aos critérios de validação.")
