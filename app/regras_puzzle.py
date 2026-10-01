"""Regras e operacoes do quebra-cabeca deslizante N-Puzzle."""

from __future__ import annotations

import random


MOVIMENTOS = ("C", "B", "E", "D")  # cima, baixo, esquerda, direita
DELTA = {"C": (-1, 0), "B": (1, 0), "E": (0, -1), "D": (0, 1)}
OPPOSTO = {"C": "B", "B": "C", "E": "D", "D": "E"}


def objetivo(tamanho: int) -> tuple[int, ...]:
    return tuple(range(1, tamanho * tamanho)) + (0,)


def aplicar_movimento(tabuleiro: tuple[int, ...], movimento: str, tamanho: int) -> tuple[tuple[int, ...], bool]:
    """Move o espaco vazio quando o movimento respeita os limites do tabuleiro."""
    indice_vazio = tabuleiro.index(0)
    linha, coluna = divmod(indice_vazio, tamanho)
    deslocamento = DELTA[movimento]
    nova_linha, nova_coluna = linha + deslocamento[0], coluna + deslocamento[1]
    if not (0 <= nova_linha < tamanho and 0 <= nova_coluna < tamanho):
        return tabuleiro, False

    outro = nova_linha * tamanho + nova_coluna
    novo = list(tabuleiro)
    novo[indice_vazio], novo[outro] = novo[outro], novo[indice_vazio]
    return tuple(novo), True


def executar_movimentos(tabuleiro: tuple[int, ...], movimentos: list[str], tamanho: int) -> tuple[tuple[int, ...], int]:
    """Aplica uma sequencia e devolve o tabuleiro final e quantos movimentos foram invalidos."""
    invalidos = 0
    atual = tabuleiro
    for movimento in movimentos:
        atual, valido = aplicar_movimento(atual, movimento, tamanho)
        invalidos += not valido
    return atual, invalidos


def distancia_manhattan(tabuleiro: tuple[int, ...], tamanho: int) -> int:
    """Calcula o quanto as pecas ainda estao distantes da posicao correta."""
    total = 0
    for indice, peca in enumerate(tabuleiro):
        if peca == 0:
            continue
        linha, coluna = divmod(indice, tamanho)
        linha_obj, coluna_obj = divmod(peca - 1, tamanho)
        total += abs(linha - linha_obj) + abs(coluna - coluna_obj)
    return total


def embaralhar(tamanho: int, passos: int, seed: int | None = None) -> tuple[tuple[int, ...], list[str]]:
    """Embaralha a partir do objetivo; por isso todo tabuleiro criado e solucionavel."""
    rng = random.Random(seed)
    tabuleiro = objetivo(tamanho)
    movimentos = []
    anterior = None
    for _ in range(passos):
        candidatos = [m for m in MOVIMENTOS if m != OPPOSTO.get(anterior)]
        rng.shuffle(candidatos)
        for movimento in candidatos:
            proximo, valido = aplicar_movimento(tabuleiro, movimento, tamanho)
            if valido:
                tabuleiro, anterior = proximo, movimento
                movimentos.append(movimento)
                break
    return tabuleiro, movimentos
