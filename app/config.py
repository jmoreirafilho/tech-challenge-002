from pathlib import Path


DIRETORIO_BASE = Path(__file__).resolve().parent.parent
DIRETORIO_FRONTEND = DIRETORIO_BASE / "frontend"

DIRETORIO_FRONTEND.mkdir(exist_ok=True)
