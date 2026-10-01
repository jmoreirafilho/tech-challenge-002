from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.algoritmo_genetico import AlgoritmoGeneticoNPuzzle
from app.config import DIRETORIO_FRONTEND
from app.regras_puzzle import distancia_manhattan, embaralhar, objetivo


class RequisicaoSolucao(BaseModel):
    tamanho: int = Field(default=3, ge=3, le=4)
    tabuleiro: list[int] | None = None
    embaralhamento: int = Field(default=14, ge=4, le=70)
    populacao: int = Field(default=240, ge=40, le=800)
    geracoes: int = Field(default=700, ge=10, le=3000)
    seed: int | None = None


aplicacao = FastAPI(title="N-Puzzle com Algoritmo Genetico", version="1.0.0")
aplicacao.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
aplicacao.mount("/static", StaticFiles(directory=DIRETORIO_FRONTEND), name="static")


@aplicacao.get("/")
def inicio():
    return FileResponse(DIRETORIO_FRONTEND / "index.html")


@aplicacao.post("/api/novo-jogo")
def novo_jogo(requisicao: RequisicaoSolucao):
    tabuleiro, _ = embaralhar(requisicao.tamanho, requisicao.embaralhamento, requisicao.seed)
    return {"tabuleiro": tabuleiro, "objetivo": objetivo(requisicao.tamanho), "dificuldade": requisicao.embaralhamento}


@aplicacao.post("/api/solucionar")
def solucionar(requisicao: RequisicaoSolucao):
    try:
        if requisicao.tabuleiro is None:
            inicial, movimentos_embaralhamento = embaralhar(requisicao.tamanho, requisicao.embaralhamento, requisicao.seed)
        else:
            inicial = tuple(requisicao.tabuleiro)
            esperado = set(range(requisicao.tamanho * requisicao.tamanho))
            if len(inicial) != requisicao.tamanho ** 2 or set(inicial) != esperado:
                raise ValueError("O tabuleiro informado não contem todas as peças esperadas.")
            movimentos_embaralhamento = []
            
        alg_gen = AlgoritmoGeneticoNPuzzle(inicial, requisicao.tamanho, requisicao.populacao, requisicao.geracoes, seed=requisicao.seed)
        resultado = alg_gen.evoluir_algoritmo(registrar_tentativas=True)
        return {
            "tabuleiro_inicial": inicial,
            "tabuleiro_final": resultado["tabuleiro_final"],
            "objetivo": objetivo(requisicao.tamanho),
            "distancia_inicial": distancia_manhattan(inicial, requisicao.tamanho),
            "movimentos_embaralhamento": movimentos_embaralhamento,
            "melhor_sequencia": resultado["movimentos"],
            "resolvido": resultado["resolvido"],
            "distancia_final": resultado["distancia"],
            "movimentos_invalidos": resultado["invalidos"],
            "geracao_final": resultado["geracao"],
            "historico": resultado["historico"],
            "tentativas_por_geracao": resultado["tentativas_por_geracao"],
            "tamanho_elite": alg_gen.tamanho_elite,
        }
    except Exception as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro
