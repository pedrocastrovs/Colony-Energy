# Colony Energy

**Sistema Integrado de Gerenciamento Energético de uma Colônia (simulação didática)**

Projeto acadêmico em Python que une estruturas de dados, lógica de decisão, regressão linear simples e análise de energia solar/eólica com armazenamento. Usa somente a biblioteca padrão do Python.

## Requisitos

- Python 3.9 ou superior.
- Nenhuma dependência externa e nenhum banco de dados.

## Como executar

No terminal, dentro da pasta do projeto:

```bash
python main.py
```

Para visualizar todos os cinco cenários sem digitar nada:

```bash
python main.py --demo
```

Para executar um cenário específico:

```bash
python main.py --cenario critico
```

Para testar as regras:

```bash
python -m unittest discover -s tests -v
```

> No Windows, se necessário, use `py` no lugar de `python`.

## Organização dos arquivos

| Arquivo | Responsabilidade |
|---|---|
| `dados.py` | Dicionários hierárquicos, listas históricas e cenários |
| `previsao.py` | Regressão linear pelo método dos mínimos quadrados |
| `energia.py` | Comparação entre geração, consumo e bateria |
| `decisoes.py` | Regras de operação, prioridades e alertas |
| `main.py` | Menu do programa e execução integrada |
| `tests/test_sistema.py` | Testes automáticos de cálculo e regras |

## Fluxo do sistema

1. Os dados da colônia são representados por dicionários de fontes, consumo e bateria, e listas históricas de vento e produção eólica.
2. A regressão linear simples estima a geração eólica para o vento informado.
3. O programa soma a previsão eólica à energia solar e compara com o consumo.
4. O motor de regras decide entre operação normal, economia, modo crítico ou emergência.
5. O balanço final calcula carga/descarga de bateria, excedente não armazenado e eventual demanda não atendida.

### Modelo de previsão

Histórico **fictício e didático** de intervalos de uma hora:

| Vento (m/s) | Energia eólica (kWh) |
|---|---|
| 8 | 20 |
| 10 | 25 |
| 12 | 30 |
| 14 | 35 |

A reta estimada pelo método dos mínimos quadrados é `energia_eolica = 2,5 × vento`. Portanto, com vento de **11 m/s**, a previsão é **27,5 kWh**.

### Regras de decisão

- **NORMAL:** geração maior ou igual ao consumo original; excedente vai para bateria, dentro da capacidade.
- **ECONOMIA:** geração insuficiente, mas a reserva projetada sem ação permanece acima do mínimo; reduzir em 50% o consumo não essencial.
- **CRITICO:** a reserva projetada sem ação ficaria abaixo do mínimo; desligar consumo não essencial e priorizar suporte à vida.
- **EMERGENCIA:** mesmo após os ajustes, geração + bateria não cobrem o consumo; sinalizar demanda não atendida e necessidade de fonte auxiliar.
- O suporte à vida **nunca é desligado por uma regra do software**; em falta de energia, o sistema emite alerta de impossibilidade de atendimento.

## Exemplo de entrada e saída

**Entrada:** solar = 15 kWh, vento = 11 m/s, consumo essencial = 50 kWh, consumo não essencial = 20 kWh, bateria = 40 kWh, capacidade = 100 kWh, reserva mínima = 20 kWh.

**Resultado:** eólica prevista = 27,5 kWh; geração = 42,5 kWh; consumo original = 70 kWh. Sem ação, a reserva cairia a 12,5 kWh, abaixo do mínimo. O sistema ativa o modo CRÍTICO, desliga os 20 kWh de cargas não essenciais, reduz o consumo para 50 kWh e utiliza 7,5 kWh da bateria, encerrando com **32,5 kWh**.

**Mensagem:** `CRITICO - Desligar cargas NÃO essenciais e priorizar suporte à vida.`

## Casos demonstrados

- Normal: há energia excedente armazenável.
- Economia: redução parcial de consumo não essencial.
- Crítico: proteção da reserva e priorização de sistemas essenciais.
- Excedente: bateria cheia, geração não armazenada.
- Insuficiência: demanda não atendida, exigindo fonte auxiliar.

## Limitações e hipóteses

- Sistema **acadêmico**, sem integração a sensores, inversores ou instalações reais.
- Dados históricos sintéticos; a reta de regressão é apenas ilustrativa, não considera curva física de potência da turbina, velocidade de corte ou limites de operação.
- Todas as quantidades de energia em kWh se referem a **um mesmo intervalo de uma hora**.
- Bateria idealizada: sem perdas de conversão, limites de carga/descarga ou degradação.
- As regras simulam decisões, mas não executam desligamentos físicos.

## Repositório

https://github.com/pedrocastrovs/Colony-Energy
