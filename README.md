# Dimensionamento Energético Residencial

Sistema de terminal (CLI) em Python para cadastro de imóveis, controle de equipamentos elétricos e estimativa do consumo de energia residencial. Permite comparar o consumo entre diferentes imóveis e gerar um gráfico comparativo com `matplotlib`.

## Informações acadêmicas

- **Instituição:** Faculdade de Informática e Administração Paulista - FIAP
- **Curso/Turma:** Ciência da Computação / 1CCPI
- **Disciplina/Projeto:** Soluções em Energias Renováveis e Sustentáveis
- **Integrantes:**
  - Nayhely Estela C. C. - 571416
  - Kauanne Paula de Oliveira - 574191
- **Professor(a) orientador(a):** Álvaro Alexandre Rezende Gonçalves

## Funcionalidades

- **Cadastro e login de usuário** (nome, e-mail e senha numérica)
- **Gestão de imóveis**: cadastrar, listar, editar, remover e ver detalhes
- **Gestão de equipamentos** por imóvel: adicionar, listar, editar e remover
- **Cálculo de consumo mensal estimado** por equipamento e por imóvel (kWh/mês)
- **Registro e histórico de consumo mensal**, com indicação de meses acima/abaixo da média
- **Ranking de equipamentos** por consumo dentro de um imóvel
- **Relatório comparativo entre imóveis**, com geração de gráfico de barras (`comparativo_imoveis.png`)
- **Resumo energético anual** por imóvel, com total do ano e mês de maior consumo

## Tecnologias

- Python 3
- [matplotlib](https://matplotlib.org/) - geração do gráfico comparativo
- `re` - validação de e-mail (biblioteca padrão)

## Pré-requisitos

- Python 3.10 ou superior (o código usa f-strings com aspas duplas aninhadas, suportado a partir do Python 3.12; recomenda-se usar a versão mais recente)
- pip

## Instalação

```bash
git clone <url-do-repositorio>
cd dimensionamento-energetico-residencial
pip install matplotlib
```

## Como usar

Execute o script principal:

```bash
python dimensionamento-energetico-residencial.py
```

O fluxo do programa é:

1. **Cadastro de usuário** - informe nome, e-mail e senha (apenas números)
2. **Login** - confirme o e-mail e a senha cadastrados
3. **Menu principal** - navegue pelas opções numeradas para gerenciar imóveis, equipamentos e consumo

### Fórmula de cálculo de consumo

```
consumo_diario (kWh) = (potência_watts × quantidade × horas_uso) / 1000
consumo_mensal (kWh) = consumo_diario × 30
```

## Estrutura de dados

O sistema mantém os dados em memória durante a execução, na seguinte estrutura:

```
usuario
├── nome, email, senha
└── imoveis []
    ├── nome, endereco, tipo (casa/apartamento)
    ├── equipamentos []
    │   └── nome, quantidade, potencia_watts, horas_uso
    └── historico []
        └── mes, consumo_kwh
```

> **Observação:** os dados não são persistidos em arquivo ou banco de dados - ao encerrar o programa, as informações são perdidas.

## Saída gerada

Ao executar o relatório comparativo entre imóveis (opção 11), um gráfico de barras é salvo no diretório do projeto como `comparativo_imoveis.png`.

## Dados de teste

Como o programa não tem persistência, é preciso recadastrar tudo a cada execução. Use os valores abaixo como um roteiro rápido para testar o sistema sem precisar inventar dados na hora.

**1. Cadastro de usuário / Login**

| Campo | Valor sugerido |
|---|---|
| Nome | Usuário Teste |
| E-mail | teste@teste.com |
| Senha | 1234 |

Repita e-mail e senha na etapa de login.

**2. Imóvel 1**

| Campo | Valor sugerido |
|---|---|
| Nome/apelido | Casa Principal |
| Endereço | Rua das Flores, 100 |
| Tipo | casa |

Equipamentos do Imóvel 1 (opção 6 -> 1):

| Nome | Quantidade | Potência (W) | Horas de uso/dia |
|---|---|---|---|
| Geladeira | 1 | 150 | 24 |
| Chuveiro elétrico | 1 | 5500 | 0.5 |
| Ar-condicionado | 1 | 1200 | 6 |
| Lâmpada LED | 6 | 9 | 5 |

**3. Imóvel 2**

| Campo | Valor sugerido |
|---|---|
| Nome/apelido | Apartamento Centro |
| Endereço | Av. Central, 500, Apto 12 |
| Tipo | apartamento |

Equipamentos do Imóvel 2:

| Nome | Quantidade | Potência (W) | Horas de uso/dia |
|---|---|---|---|
| Geladeira | 1 | 120 | 24 |
| Micro-ondas | 1 | 1100 | 0.3 |
| TV | 1 | 100 | 4 |

Com os dois imóveis e equipamentos cadastrados, já é possível testar as opções 7 a 12 do menu (consumo mensal, histórico, ranking, comparativo entre imóveis e resumo anual). Para o histórico (opção 9), registre o consumo em dois ou mais meses (ex.: `Janeiro/2026`, `Fevereiro/2026`) para visualizar a comparação com a média.

## Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).
