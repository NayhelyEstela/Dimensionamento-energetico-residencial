# PB 07

imovel = []

def cadastro_equipamento():
    nome_equipamento = input("Digite o nome do equipamento: ")
    qnt = int(input("Digite a quantidade do equipamentos que estarão em uso: "))
    if qnt > 1:
        tempo_uso_lista = []
        for i in range(qnt):
            tempo_uso = int(input(f"Digite o tempo de uso por dia do {i+1}º equipamento em minutos: "))
            tempo_uso_lista.append(tempo_uso)

        return nome_equipamento, qnt, tempo_uso_lista

    else:
        tempo_uso = int(input("Digite o tempo de uso do equipamento: "))

        return nome_equipamento, qnt, tempo_uso


nome_equipamento, qnt, tempo_uso = cadastro_equipamento()

print("==== Resumo do cadastro do equipamento ====\n")

print("Verifique se tudo esta correto, se não volte e cadastre novamente\n")
print(f"- Nome do equipamento: {nome_equipamento}")
print(f"- Quantidade de equipamentos: {qnt}")
for i in range(qnt):
    print(f"- Tempo de uso em minutos do {i+1}° equipamento: {tempo_uso[i]}")


