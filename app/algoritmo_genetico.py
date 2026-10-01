from __future__ import annotations

import random

from app.regras_puzzle import MOVIMENTOS, distancia_manhattan, executar_movimentos, objetivo


class AlgoritmoGeneticoNPuzzle:
    def __init__(self, tabuleiro_inicial, tamanho=3, populacao=240, geracoes=700, taxa_mutacao=0.18, seed=None):
        self.inicial = tuple(tabuleiro_inicial)
        self.tamanho = tamanho
        self.populacao = populacao
        self.geracoes = geracoes
        self.taxa_mutacao = taxa_mutacao
        self.tamanho_elite = 12
        self.rng = random.Random(seed)
        self.historico = []
        self.tentativas_por_geracao = []

    def criar_tentativa(self):
        """Cria um individuo: uma possivel sequencia de movimentos do puzzle."""
        return [self.rng.choice(MOVIMENTOS) for _ in range(self.rng.randint(8, 55))]

    def avaliar_tentativa(self, tentativa):
        """Aplica uma tentativa pelas regras do jogo e mede sua qualidade."""
        final, invalidos = executar_movimentos(self.inicial, tentativa, self.tamanho)
        distancia = distancia_manhattan(final, self.tamanho)
        # Penaliza movimentos inuteis e solucoes longas, mas prioriza montar o tabuleiro.
        custo = distancia * 100 + invalidos * 3 + len(tentativa) * 0.05
        return custo, final, distancia, invalidos

    def cruzar_tentativas(self, pai, mae):
        """Cria um filho juntando o inicio da tentativa do pai ao fim da tentativa da mae."""
        corte_a = self.rng.randint(0, len(pai))
        corte_b = self.rng.randint(0, len(mae))
        return pai[:corte_a] + mae[corte_b:]

    def mutar_tentativa(self, tentativa):
        """Altera uma tentativa com pequena probabilidade para manter diversidade na populacao."""
        filho = tentativa[:]
        if self.rng.random() < self.taxa_mutacao:
            acao = self.rng.choice(("trocar", "inserir", "remover"))
            if acao == "trocar" and filho:
                filho[self.rng.randrange(len(filho))] = self.rng.choice(MOVIMENTOS)
            elif acao == "inserir" and len(filho) < 80:
                filho.insert(self.rng.randrange(len(filho) + 1), self.rng.choice(MOVIMENTOS))
            elif acao == "remover" and len(filho) > 2:
                filho.pop(self.rng.randrange(len(filho)))
        return filho

    def selecionar_pai_por_torneio(self, avaliados):
        """Sorteia quatro tentativas e escolhe como pai a que tem o menor custo entre elas."""
        return min(self.rng.sample(avaliados, 4), key=lambda item: item["custo"])["movimentos"]

    def criar_proxima_geracao(self, avaliados):
        """Preserva a elite e preenche o restante da populacao com filhos cruzados e mutados."""
        elite = [item["movimentos"][:] for item in avaliados[:self.tamanho_elite]]
        proxima_geracao = elite[:]

        while len(proxima_geracao) < self.populacao:
            pai = self.selecionar_pai_por_torneio(avaliados)
            mae = self.selecionar_pai_por_torneio(avaliados)
            filho = self.cruzar_tentativas(pai, mae)
            proxima_geracao.append(self.mutar_tentativa(filho))

        return proxima_geracao

    def evoluir_algoritmo(self, registrar_tentativas=False):
        """Executa geracoes ate resolver o puzzle ou atingir o limite configurado."""
        populacao = [self.criar_tentativa() for _ in range(self.populacao)]
        melhor = None
        for geracao in range(self.geracoes):
            # Cada membro da populacao e uma tentativa concreta de resolver o puzzle.
            avaliados = []
            for tentativa in populacao:
                custo, final, distancia, invalidos = self.avaliar_tentativa(tentativa)
                avaliados.append({
                    "movimentos": tentativa[:], "custo": custo, "tabuleiro_final": final,
                    "distancia": distancia, "invalidos": invalidos,
                })
            avaliados.sort(key=lambda item: item["custo"])
            candidato = avaliados[0]
            custo, final, distancia, invalidos = (candidato["custo"], candidato["tabuleiro_final"], candidato["distancia"], candidato["invalidos"])
            if registrar_tentativas:
                self.tentativas_por_geracao.append({
                    "geracao": geracao,
                    "tentativas": [
                        {"posicao": posicao, "movimentos": item["movimentos"], "distancia": item["distancia"], "invalidos": item["invalidos"]}
                        for posicao, item in enumerate(avaliados, start=1)
                    ],
                })
            if melhor is None or custo < melhor["custo"]:
                melhor = {"movimentos": candidato["movimentos"][:], "custo": custo, "tabuleiro_final": final, "distancia": distancia, "invalidos": invalidos, "geracao": geracao}
            self.historico.append({"geracao": geracao, "fitness": round(1 / (1 + custo), 6), "distancia": distancia})
            if final == objetivo(self.tamanho):
                break
            populacao = self.criar_proxima_geracao(avaliados)
        melhor["resolvido"] = melhor["tabuleiro_final"] == objetivo(self.tamanho)
        melhor["historico"] = self.historico
        melhor["tentativas_por_geracao"] = self.tentativas_por_geracao
        return melhor
