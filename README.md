# Dimensionamento Energético Residencial

## Sobre o projeto

O Dimensionamento Energético Residencial é uma aplicação de terminal desenvolvida em Python para auxiliar no acompanhamento do consumo de energia elétrica de imóveis residenciais e na elaboração de propostas de pré-dimensionamento fotovoltaico.

O sistema permite cadastrar usuários e imóveis, registrar equipamentos elétricos, acompanhar históricos de consumo, comparar imóveis e gerar relatórios energéticos. Também realiza estimativas preliminares de sistemas fotovoltaicos, considerando módulos, inversores e baterias opcionais, apresentando orçamento detalhado, estimativa de economia, payback simples e comparação entre cenários com e sem armazenamento.

Os dados são armazenados em arquivos CSV, permitindo preservar cadastros, informações de consumo e propostas entre diferentes execuções do programa. As propostas salvas podem ser consultadas novamente e exportadas para arquivo de texto.

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

- Seleção de um imóvel já cadastrado, reaproveitando seus equipamentos, localização e histórico, sem novo cadastro.
- Apresentação do consumo médio diário (kWh/dia), do consumo mensal (kWh/mês) e da potência instalada da residência (kW).
- Consulta da irradiação solar (HSP) conforme a cidade e o estado do imóvel, com registro da fonte utilizada.
- Adoção e justificativa do fator global de desempenho (PR).
- Cálculo automático da potência fotovoltaica necessária (kWp).
- Seleção de módulos solares a partir de um catálogo, com cálculo da quantidade e da potência efetivamente instalada.
- Seleção de inversores compatíveis, considerando limites elétricos, MPPT e relação DC/AC.
- Escolha entre sistema sem baterias ou com baterias, com atualização do dimensionamento e do orçamento.
- Cálculo da energia necessária, da capacidade nominal, da quantidade e da capacidade total instalada das baterias.
- Estimativa da geração diária e mensal, utilizando a potência efetivamente instalada.
- Comparação entre geração e consumo, com percentual de atendimento e distinção entre energia gerada e energia compensada.
- Orçamento detalhado por item (equipamento, fabricante/modelo, quantidade, preço unitário e subtotal), com rastreabilidade das fontes.
Estimativa de economia mensal e anual a partir da tarifa informada pelo usuário, com exibição das premissas.
- Cálculo do payback simples.
- Comparação lado a lado entre os cenários com e sem armazenamento.
- Resumo consolidado da proposta.
- Salvamento das propostas em arquivo CSV, consulta posterior e exportação para arquivo de texto.

## Tecnologias utilizadas

- **Python 3:** linguagem utilizada no desenvolvimento da aplicação.
- **CSV:** armazenamento de usuários, imóveis, equipamentos, históricos de consumo e catálogos.
- **JSON:** representação do conteúdo consolidado das propostas dentro do arquivo CSV.
- **Matplotlib:** geração do gráfico comparativo entre imóveis.
- **Bibliotecas padrão do Python:** manipulação de arquivos, cálculos matemáticos, validações, expressões regulares, identificadores e proteção de senhas.

## Pré-requisitos

- Python 3.12 ou superior, recomendado para executar o código atual.
- `pip`, para instalação das dependências.
- Arquivos de catálogo (hsp.csv, modulos.csv, inversores.csv e baterias.csv) presentes na pasta do projeto. O programa não cria dados de exemplo: se algum arquivo estiver ausente ou com colunas faltando, o dimensionamento é interrompido com uma mensagem explicativa.

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
 
Para realizar o dimensionamento fotovoltaico (opção 13 do menu), é necessário selecionar um imóvel com informações de localização e dados suficientes para estimar o consumo. O sistema utiliza o histórico de consumo, quando disponível, ou estima o consumo a partir dos equipamentos cadastrados.
 
O fluxo do dimensionamento segue estas etapas:
 
1. Seleção do imóvel e definição do percentual do consumo a ser atendido por energia solar.
2. Consulta da HSP pela localização (ou informe manual, se não houver registro).
3. Cálculo da potência fotovoltaica necessária.
4. Seleção do módulo e cálculo da quantidade.
5. Escolha entre sistema com ou sem baterias.
6. Seleção do inversor compatível e ajuste da configuração de strings.
7. Dimensionamento e seleção das baterias, quando aplicável.
8. Informe da tarifa de energia elétrica.
9. Exibição do resumo da proposta, com orçamento, economia e payback.
10. Opção de gerar o cenário alternativo (com ou sem bateria) para comparação.
11. Opção de exportar a proposta para arquivo de texto.
As propostas geradas são salvas automaticamente e podem ser consultadas depois pela opção 14 do menu ("Ver propostas salvas").
 
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
 
O consumo mensal estimado do imóvel corresponde à soma dos consumos mensais de seus equipamentos. A potência instalada da residência é a soma de potência × quantidade de todos os equipamentos, expressa em kW.
 
Quando há histórico de consumo, o sistema utiliza a média dos registros como referência para o dimensionamento. Caso contrário, utiliza a estimativa calculada a partir dos equipamentos. Se não houver dados suficientes para nenhuma dessas alternativas, a proposta não é dimensionada.
 
O consumo médio diário de referência é obtido por:
 
\[
E_{\text{dia}} = \frac{E_{\text{mês}}}{30}
\]
 
## Parâmetros e premissas adotados
 
| Parâmetro | Valor | Observação |
|---|---|---|
| Dias do mês (\(D\)) | 30 | Usado em consumo, geração e baterias |
| Fator global de desempenho (PR) | 0,80 | Ver justificativa abaixo |
| DoD usado no dimensionamento das baterias | 0,80 | Parâmetro padrão do cálculo de \(C_{\text{bat}}\) |
| Eficiência das baterias (\(\eta_{\text{bat}}\)) | 0,90 | Perdas de carga e descarga |
| Relação DC/AC aceita | 0,8 a 1,5 | Valores fora da faixa descartam o inversor |
| Relação DC/AC de referência | 1,2 | Usada apenas para ordenar as opções |
| Custos adicionais (estrutura, cabos, proteções e instalação) | 20% do custo dos equipamentos | Premissa acadêmica simplificada |
 
**Justificativa do PR:** o PR de 0,80 representa as perdas típicas por temperatura, sujeira, cabeamento, inversor e descasamento entre módulos. A faixa usual de projeto situa-se entre 0,75 e 0,85. O valor é exibido e justificado no momento do dimensionamento e no resumo da proposta.
 
## Dimensionamento fotovoltaico
 
### Irradiação solar
 
O sistema utiliza o arquivo `hsp.csv`, que relaciona cidades e estados brasileiros a valores de Horas de Sol Pleno (HSP), expressos em kWh/m²/dia.
 
A base identifica como referência o Atlas Brasileiro de Energia Solar, segunda edição, publicado pelo INPE/LABREN em 2017. O valor consultado é utilizado como parâmetro para estimar a potência necessária do sistema fotovoltaico. Quando não há registro para a cidade e o estado informados, o usuário pode digitar a HSP manualmente, e a fonte "manual" fica registrada na proposta.
 
A HSP representa uma medida equivalente da energia solar recebida diariamente por unidade de área, expressa em horas à irradiância de referência de 1 kW/m².
 
Fonte: [Atlas Brasileiro de Energia Solar — INPE/LABREN](https://labren.ccst.inpe.br/atlas_2017.html).
 
### Potência necessária
 
A potência fotovoltaica necessária é estimada a partir do consumo diário a ser atendido, da HSP local e do PR:
 
\[
P_{\text{FV}} =
\frac{E_{\text{dia}}}{HSP \times PR}
\]
 
Em que:
 
- \(P_{\text{FV}}\): potência fotovoltaica necessária, em kWp.
- \(E_{\text{dia}}\): energia diária a ser gerada, em kWh/dia (consumo mensal de referência × percentual de atendimento desejado ÷ 30).
- \(HSP\): horas de sol pleno médias por dia.
- \(PR\): fator global de desempenho adotado no sistema.
Os parâmetros utilizados devem ser interpretados como premissas de estimativa, e não como garantias de geração real. O resultado depende da qualidade dos dados de entrada e das simplificações adotadas.
 
### Seleção e dimensionamento dos módulos
 
Os módulos são recuperados de `modulos.csv` (nenhum valor de equipamento é fixado no código). Eles são listados por custo por Wp, com a opção de menor custo como sugestão, e o usuário pode aceitá-la ou escolher outro módulo.
 
A quantidade de módulos e a potência efetivamente instalada são:
 
\[
N_{\text{mod}} = \left\lceil \frac{P_{\text{FV}} \times 1000}{P_{\text{mod}}} \right\rceil
\qquad
P_{\text{inst}} = \frac{N_{\text{mod}} \times P_{\text{mod}}}{1000}
\]
 
### Seleção de inversores
 
O inversor é recuperado de `inversores.csv`. A análise de compatibilidade considera:
 
- tensão máxima de entrada (a tensão Voc da string não pode ultrapassá-la);
- faixa de operação MPPT, mínima e máxima (a tensão Vmp da string deve ficar dentro dela);
- corrente máxima de entrada por MPPT e número de MPPTs;
- potência fotovoltaica máxima admitida;
- relação DC/AC entre 0,8 e 1,5;
- compatibilidade com baterias, quando o sistema é com armazenamento.
A relação DC/AC é calculada por:
 
\[
R_{DC/AC} = \frac{P_{\text{FV,instalada}}}{P_{\text{inversor}}}
\]
 
Os inversores incompatíveis são descartados. Os compatíveis são ordenados pela proximidade da relação DC/AC de referência (1,2) e, em caso de empate, pelo menor preço. O usuário pode aceitar a sugestão ou escolher outro inversor, de modo que o preço não é o único critério de seleção.
 
Quando a configuração de strings exige mais módulos do que o dimensionamento inicial, a quantidade é ajustada e a potência instalada e a geração são recalculadas.
 
O dataset de inversores não traz a eficiência do equipamento. As perdas do inversor estão consideradas no PR adotado, e essa premissa é informada na tela de seleção e no resumo da proposta.
 
### Dimensionamento das baterias
 
A utilização de baterias é opcional. Quando selecionado o armazenamento, o usuário informa a autonomia desejada (em horas) e o sistema calcula:
 
\[
E_{\text{aut}} = \frac{E_{\text{mês}}}{30} \times \frac{\text{autonomia (h)}}{24}
\]
 
\[
C_{\text{bat}} = \frac{E_{\text{aut}}}{DoD \times \eta_{\text{bat}}}
\]
 
\[
N_{\text{bat}} = \left\lceil \frac{C_{\text{bat}}}{C_{\text{unidade}}} \right\rceil
\]
 
Em que:
 
- \(E_{\text{aut}}\): energia necessária para a autonomia desejada, em kWh.
- \(C_{\text{bat}}\): capacidade nominal necessária, em kWh. Já considera o DoD e a eficiência das baterias.
- \(C_{\text{unidade}}\): capacidade nominal de uma bateria do catálogo, em kWh.
- \(N_{\text{bat}}\): quantidade de baterias.
A capacidade útil de cada bateria, usada para comparar o custo entre opções, é:
 
\[
C_{\text{útil}} = C_{\text{nominal}} \times \frac{DoD_{\text{catálogo}}}{100}
\]
 
A seleção considera a compatibilidade da tensão nominal da bateria com a faixa aceita pelo inversor híbrido. Entre as opções compatíveis, a de menor custo por kWh útil é a sugestão, e o usuário pode escolher outra. O resumo apresenta a autonomia considerada, a energia necessária, a capacidade necessária, o modelo, a quantidade e a capacidade total instalada (nominal e útil).
 
Se não houver uma combinação válida de inversor e bateria, o sistema tenta outras combinações e, não havendo nenhuma, a proposta não é apresentada como compatível.
 
### Estimativa de geração
 
A geração fotovoltaica é estimada a partir da potência efetivamente instalada, da HSP e do PR:
 
\[
E_{\text{gerada,dia}} = P_{\text{inst}} \times HSP \times PR
\qquad
E_{\text{gerada,mês}} = E_{\text{gerada,dia}} \times 30
\]
 
Trata-se de uma aproximação da produção energética, sujeita à variação da irradiação, às condições de instalação, à temperatura, às sombras e às perdas reais do sistema.
 
### Comparação entre geração e consumo
 
O percentual de atendimento é calculado por:
 
\[
\text{Atendimento (\%)} = \frac{E_{\text{gerada,mês}}}{E_{\text{consumida,mês}}} \times 100
\]
 
Quando a geração supera o consumo, o resumo distingue a energia gerada da energia efetivamente consumida/compensada (limitada ao consumo) e apresenta o excedente. O atendimento não garante autonomia energética nem substitui uma análise detalhada do perfil de consumo.
 
## Estimativa de orçamento
 
O orçamento considera os preços unitários registrados nos catálogos e as quantidades selecionadas na proposta. Cada item é apresentado com equipamento, fabricante/modelo, quantidade, preço unitário e subtotal:
 
\[
\text{Custo}_{\text{item}} = \text{quantidade} \times \text{preço unitário}
\qquad
\text{Custo}_{\text{total}} = \sum \text{Custo}_{\text{item}}
\]
 
Os custos são organizados da seguinte forma:
 
- **Custo dos módulos:** preço unitário multiplicado pela quantidade de módulos.
- **Custo do inversor:** preço do inversor selecionado.
- **Custo das baterias:** preço unitário multiplicado pela quantidade de baterias; quando não há baterias, o custo é zero.
- **Custo dos equipamentos:** soma dos custos de módulos, inversor e baterias.
- **Demais custos estimados:** percentual adicional aplicado ao custo dos equipamentos, destinado a representar itens como estrutura, cabeamento, proteções e instalação.
- **Custo total estimado:** soma dos custos dos equipamentos e dos demais custos estimados.
No modelo acadêmico atual, os demais custos correspondem a 20% do custo dos equipamentos. Esse percentual é uma premissa simplificada, não uma cotação comercial.
 
Os dados de preço devem ser interpretados conforme o fornecedor, a data de coleta e a fonte registrada no catálogo. O resumo apresenta uma seção de rastreabilidade com o identificador, o fornecedor, a data de coleta e a fonte de cada item. Os valores podem sofrer alterações e não representam necessariamente preços vigentes no momento da consulta.
 
## Estimativa de economia e payback
 
O usuário informa a tarifa de energia elétrica (R$/kWh) no momento do dimensionamento. A economia é estimada por:
 
\[
\text{Economia}_{\text{mensal}} = E_{\text{compensada}} \times \text{tarifa}
\qquad
\text{Economia}_{\text{anual}} = \text{Economia}_{\text{mensal}} \times 12
\]
 
Em que \(E_{\text{compensada}}\) é o menor valor entre a geração mensal e o consumo mensal de referência.
 
O payback simples é calculado por:
 
\[
\text{Payback} = \frac{\text{Investimento total}}{\text{Economia}_{\text{anual}}}
\]
 
O resumo apresenta a tarifa utilizada, a energia compensada, a economia mensal e anual e o payback, sempre identificado como **payback simples**. Os valores são estimativas, e não previsão financeira exata.
 
**Premissas da economia:** tarifa constante (sem reajuste), compensação limitada ao consumo, sem taxa de disponibilidade e sem degradação dos módulos. Se a economia anual estimada for zero, o payback não é calculado.
 
## Comparação entre cenários
 
Após gerar uma proposta, o usuário pode solicitar o cenário alternativo (se a primeira foi sem bateria, gera-se o cenário com bateria, e vice-versa). Neste cenário o módulo escolhido é mantido, e o inversor e a bateria são definidos automaticamente pela primeira sugestão de cada lista.
 
O sistema apresenta os dois cenários lado a lado, comparando:
 
- potência fotovoltaica necessária e instalada;
- módulos e inversor;
- geração mensal e atendimento;
- armazenamento, capacidade instalada e autonomia;
- investimento total, economia anual e payback simples;
- custo adicional do armazenamento.
Cada cenário é salvo como uma proposta própria.
 
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
- `propostas.csv`: propostas de dimensionamento e seus respectivos dados consolidados (configuração fotovoltaica, baterias, orçamento e resultados econômicos).
Os identificadores permitem relacionar os registros entre os arquivos. A remoção de um imóvel deve considerar os registros dependentes associados a ele.
 
## Persistência e tratamento de erros
 
O sistema carrega os dados armazenados ao iniciar e salva as alterações realizadas durante a execução. As propostas são gravadas em `dados/propostas.csv` após o dimensionamento e podem ser recuperadas pela opção 14 do menu, que exibe novamente o resumo completo.
 
As senhas são armazenadas utilizando hash PBKDF2-HMAC-SHA256 com salt, em vez de texto puro.
 
O programa prevê o tratamento de arquivos ausentes, registros inválidos e arquivos que não possam ser lidos. Dependendo da situação, os dados inválidos são ignorados com aviso, ou o arquivo ilegível é isolado para evitar que seja utilizado como uma base válida.
 
Os principais casos de validação tratados, com mensagens compreensíveis ao usuário, são:
 
- campos obrigatórios vazios;
- quantidades que não sejam inteiros positivos;
- valores numéricos inválidos, nulos, negativos ou infinitos (vírgula decimal aceita);
- HSP menor ou igual a zero (no arquivo ou digitada manualmente);
- PR fora do intervalo entre 0 e 1;
- consumo de referência indisponível, que impede o dimensionamento;
- linhas inválidas nos catálogos, ignoradas com aviso;
- ausência de inversor ou bateria compatível com a configuração, com indicação do conflito;
- economia nula, que impede o cálculo do payback.
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
 
- **Gráfico comparativo entre imóveis:** gráfico de barras salvo no diretório do projeto como `comparativo_imoveis.png`.
- **Proposta fotovoltaica:** apresentada no terminal e registrada em `dados/propostas.csv`.
- **Proposta exportada:** arquivo de texto com o resumo completo (e a comparação dos cenários, quando houver), gerado no diretório do projeto com o nome `proposta_<nome_do_imovel>_<data>_<hora>.txt`. A exportação pode ser feita ao final do dimensionamento ou a partir da opção 14 do menu.
## Limitações do projeto
 
O dimensionamento fotovoltaico é uma estimativa acadêmica e possui simplificações importantes:
 
- Os resultados dependem da qualidade do histórico de consumo ou das estimativas baseadas nos equipamentos cadastrados.
- A HSP representa um parâmetro médio e não prevê exatamente a geração em cada dia ou mês.
- O PR é uma constante adotada para todo o sistema; as perdas reais variam conforme a instalação.
- O dataset de inversores não informa a eficiência; as perdas do inversor são consideradas apenas dentro do PR.
- Os cálculos elétricos utilizam parâmetros de catálogo e não representam todas as condições de operação em campo.
- A verificação de compatibilidade não substitui a análise completa de projeto, incluindo condições de temperatura, corrente de curto-circuito, limites específicos de entradas e strings, proteções e normas aplicáveis.
- O orçamento não equivale a uma proposta comercial. Os preços podem variar, e o percentual de custos adicionais é uma estimativa simplificada.
- A economia usa tarifa constante e considera apenas a energia solar compensada; não inclui taxa de disponibilidade, regras de compensação, reajustes tarifários, degradação dos módulos nem economia adicional pelo uso de baterias.
- O payback calculado é simples, sem juros, inflação ou custos de manutenção, e não deve ser tomado como previsão financeira exata.
- No cenário alternativo, o inversor e a bateria são escolhidos automaticamente pela primeira sugestão, o que pode diferir da escolha manual do cenário principal.
- A seleção de baterias depende dos dados disponíveis no catálogo e das premissas de capacidade e autonomia adotadas.
- O percentual de atendimento energético estimado não garante independência da rede elétrica nem autonomia em caso de interrupção do fornecimento.
Antes de uma instalação real, é necessário confirmar as especificações nos documentos oficiais dos fabricantes, avaliar as condições do local e elaborar o projeto com um profissional habilitado.
 
## Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).
