# Dimensionamento Energético Residencial

## Sobre o projeto

O Dimensionamento Energético Residencial é uma aplicação de terminal desenvolvida em Python para auxiliar no acompanhamento do consumo de energia elétrica de imóveis residenciais e na elaboração de propostas de pré-dimensionamento fotovoltaico.

O sistema permite cadastrar usuários e imóveis, registrar equipamentos elétricos, acompanhar históricos de consumo, comparar imóveis e gerar relatórios energéticos. Também realiza estimativas preliminares de sistemas fotovoltaicos, considerando módulos, inversores e baterias opcionais, além de apresentar uma estimativa de orçamento.

Os dados são armazenados em arquivos CSV, permitindo preservar cadastros, informações de consumo e propostas entre diferentes execuções do programa.

O projeto possui finalidade acadêmica. Os resultados são estimativas preliminares e não substituem a avaliação de um profissional habilitado nem a elaboração de um projeto executivo.

## Informações acadêmicas

- **Instituição:** Faculdade de Informática e Administração Paulista - FIAP
- **Curso/Turma:** Ciência da Computação / 1CCPI
- **Disciplina/Projeto:** Soluções em Energias Renováveis e Sustentáveis
- **Integrantes:**
  - Nayhely Estela C. C. - 571416
  - Kauanne Paula de Oliveira - 574191
- **Professor(a) orientador(a):** Álvaro Alexandre Rezende Gonçalves

## Funcionalidades

### Usuários e imóveis

- Cadastro e autenticação de usuários.
- Validação do formato dos endereços de e-mail.
- Armazenamento de senhas com hash e salt.
- Cadastro, consulta, edição e remoção de imóveis.
- Registro de nome, endereço, cidade, estado e tipo de imóvel.
- Persistência das informações entre execuções.

### Equipamentos e consumo energético

- Cadastro, consulta, edição e remoção de equipamentos por imóvel.
- Registro de quantidade, potência elétrica e horas de uso diário.
- Estimativa do consumo diário e mensal de cada equipamento.
- Cálculo do consumo mensal estimado do imóvel.
- Registro e consulta do histórico mensal de consumo.
- Comparação do consumo registrado com a média histórica.
- Ranking dos equipamentos de acordo com o consumo estimado.
- Resumo energético anual, incluindo consumo total e mês de maior consumo.
- Comparação entre imóveis, com geração de gráfico de barras.

### Dimensionamento fotovoltaico

- Consulta da irradiação solar média diária conforme a cidade e o estado do imóvel.
- Estimativa da potência fotovoltaica necessária.
- Seleção de módulos solares a partir de um catálogo.
- Verificação preliminar da compatibilidade elétrica entre módulos e inversores.
- Seleção opcional de baterias para armazenamento de energia.
- Cálculo da capacidade de armazenamento e da quantidade estimada de baterias.
- Verificação da compatibilidade entre baterias e inversores híbridos.
- Estimativa da geração de energia do sistema.
- Cálculo do orçamento de equipamentos e de custos adicionais estimados.
- Exibição de um resumo consolidado da proposta.
- Salvamento das propostas em arquivo CSV.

## Tecnologias utilizadas

- **Python 3:** linguagem utilizada no desenvolvimento da aplicação.
- **CSV:** armazenamento de usuários, imóveis, equipamentos, históricos de consumo e catálogos.
- **JSON:** representação do conteúdo consolidado das propostas dentro do arquivo CSV.
- **Matplotlib:** geração do gráfico comparativo entre imóveis.
- **Bibliotecas padrão do Python:** manipulação de arquivos, cálculos matemáticos, validações, expressões regulares, identificadores e proteção de senhas.

## Pré-requisitos

- Python 3.12 ou superior, recomendado para executar o código atual.
- `pip`, para instalação das dependências.

## Instalação e execução

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/NayhelyEstela/Dimensionamento-energetico-residencial.git
cd Dimensionamento-energetico-residencial
```

Instale a dependência externa:

```bash
pip install matplotlib
```

Execute a aplicação:

```bash
python dimensionamento-energetico-residencial.py
```

Para validar os catálogos de equipamentos, execute:

```bash
python validar_datasets.py
```

Para verificar erros de sintaxe nos scripts:

```bash
python -m py_compile dimensionamento-energetico-residencial.py validar_datasets.py
```

## Funcionamento do sistema

O programa apresenta um menu interativo no terminal. O usuário realiza o cadastro e o login e, em seguida, acessa as funcionalidades disponíveis para gerenciar imóveis, equipamentos e consumo energético.

Para realizar o dimensionamento fotovoltaico, é necessário selecionar um imóvel com informações de localização e dados suficientes para estimar o consumo. O sistema utiliza o histórico de consumo, quando disponível, ou estima o consumo a partir dos equipamentos cadastrados.

A localização é utilizada para consultar a base de irradiação solar. Caso não exista um registro correspondente à cidade e ao estado informados, o programa pode solicitar um valor manual de HSP. Se não houver um valor válido disponível, o dimensionamento é interrompido.

Ao final do processo, o programa apresenta a configuração estimada do sistema e seus custos. A proposta é armazenada para consulta posterior.

## Cálculo do consumo energético

O consumo diário estimado de um equipamento é calculado por:

\[
C_{\text{diário}} =
\frac{P \times Q \times H}{1000}
\]

Em que:

- \(P\): potência do equipamento, em watts.
- \(Q\): quantidade de unidades.
- \(H\): horas de uso diário.
- \(C_{\text{diário}}\): consumo estimado, em kWh/dia.

Considerando um mês padrão de 30 dias:

\[
C_{\text{mensal}} = C_{\text{diário}} \times 30
\]

O consumo mensal estimado do imóvel corresponde à soma dos consumos mensais de seus equipamentos.

Quando há histórico de consumo, o sistema pode utilizar a média dos registros como referência para o dimensionamento. Caso contrário, utiliza a estimativa calculada a partir dos equipamentos. Se não houver dados suficientes para nenhuma dessas alternativas, a proposta não é dimensionada.

## Dimensionamento fotovoltaico

### Irradiação solar

O sistema utiliza o arquivo `hsp.csv`, que relaciona cidades e estados brasileiros a valores de Horas de Sol Pleno (HSP), expressos em kWh/m²/dia.

A base identifica como referência o Atlas Brasileiro de Energia Solar, segunda edição, publicado pelo INPE/LABREN em 2017. O valor consultado é utilizado como parâmetro para estimar a potência necessária do sistema fotovoltaico.

A HSP representa uma medida equivalente da energia solar recebida diariamente por unidade de área, expressa em horas à irradiância de referência de 1 kW/m².

Fonte: [Atlas Brasileiro de Energia Solar — INPE/LABREN](https://labren.ccst.inpe.br/atlas_2017.html).

### Potência necessária

A potência fotovoltaica necessária é estimada considerando o consumo mensal de referência, a HSP local, o número de dias adotado no cálculo e um fator global de desempenho.

De forma geral, o cálculo considera:

\[
P_{\text{FV}} =
\frac{C_m}{D \times HSP \times \eta}
\]

Em que:

- \(P_{\text{FV}}\): potência fotovoltaica necessária, em kW.
- \(C_m\): consumo mensal de referência, em kWh/mês.
- \(D\): quantidade de dias considerada no mês.
- \(HSP\): horas de sol pleno médias por dia.
- \(\eta\): fator global de desempenho adotado no sistema.

Os parâmetros utilizados devem ser interpretados como premissas de estimativa, e não como garantias de geração real. O resultado depende da qualidade dos dados de entrada e das simplificações adotadas.

### Seleção de módulos e inversores

Os módulos são selecionados a partir de `modulos.csv`, considerando suas características elétricas, potência e preço.

A análise preliminar de compatibilidade com o inversor considera os limites de tensão, a faixa de operação MPPT, a corrente de entrada, o número de MPPTs e a potência fotovoltaica máxima admitida.

A quantidade de módulos e a configuração das strings devem respeitar os limites elétricos verificados pelo sistema. Inversores que não atendam aos critérios de compatibilidade são descartados antes da escolha final.

O preço é utilizado como critério econômico entre alternativas tecnicamente compatíveis. A opção de menor custo não deve ser interpretada como uma garantia de melhor desempenho global.

### Dimensionamento das baterias

A utilização de baterias é opcional. Quando selecionado o armazenamento, o sistema estima a capacidade necessária de acordo com o consumo de referência e a autonomia informada.

A capacidade útil de uma bateria é calculada por:

\[
C_{\text{útil}} =
C_{\text{nominal}} \times \frac{DoD}{100}
\]

Em que \(DoD\) representa a profundidade de descarga percentual informada no catálogo.

A quantidade estimada de baterias é calculada pelo arredondamento para cima da razão entre a capacidade necessária e a capacidade útil de uma unidade:

\[
N_{\text{baterias}} =
\left\lceil
\frac{C_{\text{necessária}}}{C_{\text{útil}}}
\right\rceil
\]

A seleção considera a compatibilidade da tensão nominal da bateria com a faixa aceita pelo inversor híbrido. Entre as opções compatíveis, o sistema pode recomendar a alternativa de menor custo por kWh útil.

Se não houver uma combinação válida de equipamentos, a proposta não deve ser apresentada como compatível.

### Estimativa de geração

A geração fotovoltaica é estimada a partir da potência instalada, da HSP e do fator de desempenho adotado. Trata-se de uma aproximação da produção energética, sujeita à variação da irradiação, às condições de instalação, à temperatura, às sombras e às perdas reais do sistema.

O percentual de atendimento representa uma comparação estimada entre a energia produzida pelo sistema e o consumo de referência do imóvel. Ele não garante autonomia energética nem substitui uma análise detalhada do perfil de consumo.

## Estimativa de orçamento

O orçamento considera os preços unitários registrados nos catálogos e as quantidades selecionadas na proposta.

Os custos são organizados da seguinte forma:

- **Custo dos módulos:** preço unitário multiplicado pela quantidade de módulos.
- **Custo do inversor:** preço do inversor selecionado.
- **Custo das baterias:** preço unitário multiplicado pela quantidade de baterias; quando não há baterias, o custo é zero.
- **Custo dos equipamentos:** soma dos custos de módulos, inversor e baterias.
- **Demais custos estimados:** percentual adicional aplicado ao custo dos equipamentos, destinado a representar itens como estrutura, cabeamento, proteções e instalação.
- **Custo total estimado:** soma dos custos dos equipamentos e dos demais custos estimados.

No modelo acadêmico atual, os demais custos correspondem a 20% do custo dos equipamentos. Esse percentual é uma premissa simplificada, não uma cotação comercial.

Os dados de preço devem ser interpretados conforme o fornecedor, a data de coleta e a fonte registrada no catálogo. Os valores podem sofrer alterações e não representam necessariamente preços vigentes no momento da consulta.

## Estrutura dos arquivos

O projeto utiliza a seguinte organização:

```text
Dimensionamento-energetico-residencial/
├── dimensionamento-energetico-residencial.py
├── validar_datasets.py
├── README.md
├── LICENSE
├── .gitignore
├── hsp.csv
├── modulos.csv
├── inversores.csv
├── baterias.csv
└── dados/
    ├── usuarios.csv
    ├── imoveis.csv
    ├── equipamentos.csv
    ├── historico_consumo.csv
    └── propostas.csv
```

### Catálogo de módulos — `modulos.csv`

Contém os dados técnicos e comerciais dos módulos fotovoltaicos.

Principais campos:

- `id`: identificador do módulo.
- `fabricante` e `modelo`: identificação do equipamento.
- `potencia_wp`: potência nominal em watts-pico.
- `voc_v` e `isc_a`: tensão de circuito aberto e corrente de curto-circuito.
- `vmp_v` e `imp_a`: tensão e corrente no ponto de máxima potência.
- `eficiencia_pct`: eficiência percentual.
- `preco_brl`: preço em reais.
- `fornecedor`, `data_coleta` e `url_fonte`: informações de rastreabilidade.
- `obs`: observações adicionais.

### Catálogo de inversores — `inversores.csv`

Contém as características elétricas e comerciais dos inversores.

Principais campos:

- `id`, `fabricante`, `modelo` e `tipo`.
- `potencia_nominal_w` e `potencia_max_fv_w`.
- `tensao_max_entrada_v`.
- `faixa_mppt_min_v` e `faixa_mppt_max_v`.
- `corrente_max_entrada_a` e `numero_mppt`.
- `compativel_bateria`.
- `tensao_bateria_min_v` e `tensao_bateria_max_v`.
- `preco_brl`, `fornecedor`, `data_coleta`, `url_fonte` e `obs`.

### Catálogo de baterias — `baterias.csv`

Contém as características de capacidade, tecnologia e preço das baterias.

Principais campos:

- `id`, `fabricante`, `modelo` e `tecnologia`.
- `tensao_nominal_v`.
- `capacidade_ah` e `capacidade_kwh`.
- `dod_pct`: profundidade de descarga percentual.
- `ciclos`: quantidade de ciclos informada.
- `preco_brl`, `fornecedor`, `data_coleta`, `url_fonte` e `obs`.

### Base de irradiação solar — `hsp.csv`

Relaciona cidade, estado, valor de HSP, fonte, endereço eletrônico da fonte e data de coleta.

O arquivo é utilizado para obter o parâmetro de irradiação solar correspondente à localização cadastrada no imóvel.

### Arquivos de persistência — pasta `dados/`

- `usuarios.csv`: informações dos usuários e credenciais protegidas.
- `imoveis.csv`: imóveis cadastrados e suas informações de localização.
- `equipamentos.csv`: equipamentos vinculados aos imóveis.
- `historico_consumo.csv`: registros mensais de consumo.
- `propostas.csv`: propostas de dimensionamento e seus respectivos dados consolidados.

Os identificadores permitem relacionar os registros entre os arquivos. A remoção de um imóvel deve considerar os registros dependentes associados a ele.

As propostas são armazenadas com seus identificadores, a data e o conteúdo consolidado da configuração selecionada.

## Persistência e tratamento de erros

O sistema carrega os dados armazenados ao iniciar e salva as alterações realizadas durante a execução.

As senhas são armazenadas utilizando hash PBKDF2-HMAC-SHA256 com salt, em vez de texto puro.

O programa prevê o tratamento de arquivos ausentes, registros inválidos e arquivos que não possam ser lidos. Dependendo da situação, os dados inválidos são ignorados com aviso, ou o arquivo ilegível é isolado para evitar que seja utilizado como uma base válida.

Os arquivos CSV devem manter os cabeçalhos esperados, o formato de separação e os tipos de dados definidos para cada campo. Alterações manuais nos arquivos podem comprometer a leitura ou a integridade dos relacionamentos.

## Validação dos datasets

O script `validar_datasets.py` verifica os catálogos de módulos, inversores e baterias.

A validação contempla, entre outros pontos:

- Presença das colunas obrigatórias.
- Preenchimento dos campos essenciais.
- Unicidade dos identificadores.
- Validade dos valores numéricos.
- Coerência básica das características técnicas.
- Quantidade mínima de registros prevista para os catálogos.

Para executar a validação:

```bash
python validar_datasets.py
```

Os catálogos devem manter informações de origem e rastreabilidade sempre que disponíveis. Dados técnicos inferidos, ajustados ou que necessitem de confirmação adicional devem ser identificados nas observações.

## Saídas geradas

O relatório comparativo entre imóveis gera um gráfico de barras salvo no diretório do projeto, com o nome:

```text
comparativo_imoveis.png
```

A proposta fotovoltaica é apresentada no terminal e registrada em `dados/propostas.csv`, permitindo recuperar os dados consolidados posteriormente.

## Limitações do projeto

O dimensionamento fotovoltaico é uma estimativa acadêmica e possui simplificações importantes:

- Os resultados dependem da qualidade do histórico de consumo ou das estimativas baseadas nos equipamentos cadastrados.
- A HSP representa um parâmetro médio e não prevê exatamente a geração em cada dia ou mês.
- Os cálculos elétricos utilizam parâmetros de catálogo e não representam todas as condições de operação em campo.
- A verificação de compatibilidade não substitui a análise completa de projeto, incluindo condições de temperatura, corrente de curto-circuito, limites específicos de entradas e strings, proteções e normas aplicáveis.
- O orçamento não equivale a uma proposta comercial. Os preços podem variar, e o percentual de custos adicionais é uma estimativa simplificada.
- A seleção de baterias depende dos dados disponíveis no catálogo e das premissas de capacidade e autonomia adotadas.
- O percentual de atendimento energético estimado não garante independência da rede elétrica nem autonomia em caso de interrupção do fornecimento.

Antes de uma instalação real, é necessário confirmar as especificações nos documentos oficiais dos fabricantes, avaliar as condições do local e elaborar o projeto com um profissional habilitado.

## Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).
