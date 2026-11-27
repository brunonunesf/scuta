"""Configuração explícita do ambiente; nenhum segredo é registrado em logs."""
import os
from urllib.parse import urlsplit


def origens_permitidas() -> list[str]:
    origens = [o.strip().rstrip("/") for o in os.getenv(
        "CORS_ORIGINS", "http://localhost:3000"
    ).split(",") if o.strip()]
    if not origens:
        raise ValueError("CORS_ORIGINS precisa conter pelo menos uma origem")
    for origem in origens:
        url = urlsplit(origem)
        if (url.scheme not in {"http", "https"} or not url.hostname or "*" in url.netloc
                or url.path or url.query or url.fragment or url.username or url.password):
            raise ValueError("CORS_ORIGINS deve conter origens HTTP(S), sem caminhos ou curingas")
    return list(dict.fromkeys(origens))


def validar_producao() -> None:
    if os.getenv("ENVIRONMENT") == "production":
        if not os.getenv("DATABASE_URL", "").startswith(("postgres://", "postgresql://", "postgresql+psycopg://")):
            raise ValueError("Produção exige DATABASE_URL PostgreSQL persistente")
        if os.getenv("DEBUG", "false").lower() == "true":
            raise ValueError("DEBUG deve ser false em produção")
        if not os.getenv("CORS_ORIGINS"):
            raise ValueError("Produção exige CORS_ORIGINS explícito")
