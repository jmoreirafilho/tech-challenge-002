# Tech Challenge — N-Puzzle com Algoritmo Genético

Este projeto resolve o quebra-cabeça deslizante 3x3 por um **algoritmo genético**, uma técnica clássica de Inteligência Artificial para busca e otimização. Cada indivíduo é uma sequência de movimentos (`C`, `B`, `E`, `D`).

A função de avaliação combina distância Manhattan, movimentos inválidos e comprimento da sequência. A evolução usa elitismo, seleção por torneio, crossover de um ponto e mutações de substituição, inserção e remoção.

## Vídeo de apresentação

[Assistir ao vídeo no YouTube](https://youtu.be/zIm_cF4KKcg)

## Repositório GitHub

[github.com/jmoreirafilho/tech-challenge-002](https://github.com/jmoreirafilho/tech-challenge-002)

## Como funciona

Em cada geração, o sistema cria uma população de sequências de movimentos e avalia o quão perto cada uma deixa o tabuleiro da solução. As 12 melhores tentativas são preservadas; as demais são criadas combinando e mutando sequências da população. O processo encerra quando uma tentativa monta o puzzle ou quando o limite de gerações é alcançado.

## Executar

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Abra `http://localhost:8000`.

## Estrutura do projeto

```text
app/
  algoritmo_genetico.py  # Cria, avalia e evolui as tentativas
  regras_puzzle.py       # Regras do tabuleiro e cálculo de distância
  api.py                 # Endpoints da aplicação
frontend/
  index.html             # Interface para acompanhar as gerações
main.py                  # Inicialização do servidor
```

## Roteiro para relatório

Documente o problema N-Puzzle, codificação do cromossomo, função fitness, operadores genéticos, configuração experimental, curva de fitness por geração, taxa de solução, resultados e conclusões.
