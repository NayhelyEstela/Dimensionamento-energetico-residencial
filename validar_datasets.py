import csv, sys

MINIMOS = {"modulos.csv": 4, "inversores.csv": 7, "baterias.csv": 5}
OPCIONAIS = {"obs"}
NUMERICOS = {
 "modulos.csv": ["potencia_wp","voc_v","isc_a","vmp_v","imp_a","eficiencia_pct","preco_brl"],
 "inversores.csv": ["potencia_nominal_w","potencia_max_fv_w","tensao_max_entrada_v","faixa_mppt_min_v",
                    "faixa_mppt_max_v","corrente_max_entrada_a","numero_mppt","tensao_bateria_min_v",
                    "tensao_bateria_max_v","preco_brl"],
 "baterias.csv": ["tensao_nominal_v","capacidade_ah","capacidade_kwh","dod_pct","ciclos","preco_brl"],
}
erros = []

def err(arq, id_, msg): erros.append(f"{arq} [{id_}]: {msg}")

def coerencia(arq, r):
    n = {c: float(r[c]) for c in NUMERICOS[arq]}
    i = r["id"]
    if arq == "modulos.csv":
        if not n["vmp_v"] < n["voc_v"]: err(arq, i, "Vmp deve ser < Voc")
        if not n["imp_a"] < n["isc_a"]: err(arq, i, "Imp deve ser < Isc")
        if abs(n["vmp_v"]*n["imp_a"]-n["potencia_wp"])/n["potencia_wp"] > 0.03:
            err(arq, i, "Vmp x Imp difere de Pmax em mais de 3%")
    elif arq == "inversores.csv":
        if not n["faixa_mppt_min_v"] < n["faixa_mppt_max_v"] <= n["tensao_max_entrada_v"]:
            err(arq, i, "faixa MPPT incoerente com tensão máxima")
        if r["tipo"] == "híbrido" and r["compativel_bateria"] != "sim":
            err(arq, i, "híbrido deveria ser compativel_bateria = sim")
        if r["compativel_bateria"] == "sim" and not 0 < n["tensao_bateria_min_v"] < n["tensao_bateria_max_v"]:
            err(arq, i, "faixa de tensão da bateria inválida")
        if r["compativel_bateria"] not in ("sim", "nao"): err(arq, i, "compativel_bateria deve ser sim/nao")
    else:
        kwh = n["tensao_nominal_v"]*n["capacidade_ah"]/1000
        if abs(kwh-n["capacidade_kwh"])/kwh > 0.05: err(arq, i, f"kWh ({n['capacidade_kwh']}) difere de V x Ah/1000 ({kwh:.2f})")
        if not 0 < n["dod_pct"] <= 100: err(arq, i, "DoD fora de (0, 100]")

for arq, minimo in MINIMOS.items():
    with open(arq, newline="", encoding="utf-8-sig") as f:
        linhas = list(csv.DictReader(f))
    if len(linhas) < minimo: err(arq, "-", f"{len(linhas)} itens; mínimo {minimo}")
    ids = [l["id"] for l in linhas]
    if len(ids) != len(set(ids)): err(arq, "-", "ids duplicados")
    for l in linhas:
        for c, v in l.items():
            if c not in OPCIONAIS and (v is None or v.strip() == ""): err(arq, l["id"], f"campo '{c}' vazio")
        try:
            for c in NUMERICOS[arq]: float(l[c])
        except ValueError:
            err(arq, l["id"], "campo numérico inválido"); continue
        coerencia(arq, l)
    print(f"{arq}: {len(linhas)} itens")

if erros:
    print("\nERROS:"); [print(" -", e) for e in erros]; sys.exit(1)
print("\nTodos os datasets são válidos.")
