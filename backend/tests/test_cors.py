"""CORS configurável (deploy): o site publicado precisa estar na lista, e um site qualquer não."""

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from app.config import ORIGEM_PADRAO, origens_cors

SITE = "https://scuta.vercel.app"


def app_com(ambiente: dict[str, str]) -> TestClient:
    """Um app mínimo com o CORS configurado exatamente como o `main.py` faz, para testar o comportamento do navegador."""
    origens, regex = origens_cors(ambiente)
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware, allow_origins=origens, allow_origin_regex=regex,
        allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
    )

    @app.post("/auth/login")
    def login():
        return {"ok": True}

    return TestClient(app)


def pergunta_previa(cliente: TestClient, origem: str):
    """O que o navegador pergunta antes de um POST com `Authorization` de outro endereço."""
    return cliente.options(
        "/auth/login",
        headers={"Origin": origem, "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "authorization,content-type"},
    )


def test_sem_configuracao_vale_so_o_localhost():
    assert origens_cors({}) == ([ORIGEM_PADRAO], None)
    assert origens_cors({"CORS_ORIGINS": "   "}) == ([ORIGEM_PADRAO], None)


def test_lista_separada_por_virgula_ignora_espacos_e_barra_final():
    origens, regex = origens_cors({"CORS_ORIGINS": f" {SITE}/ , http://localhost:3000 ,,"})

    assert origens == [SITE, "http://localhost:3000"] and regex is None


def test_a_regex_e_opcional():
    assert origens_cors({"CORS_ORIGINS": SITE, "CORS_ORIGIN_REGEX": r"https://scuta-.*\.vercel\.app"})[1] == r"https://scuta-.*\.vercel\.app"


def test_curinga_e_recusado():
    with pytest.raises(ValueError, match="não aceita"):
        origens_cors({"CORS_ORIGINS": "*"})
    with pytest.raises(ValueError):
        origens_cors({"CORS_ORIGINS": f"{SITE},*"})


def test_o_site_publicado_e_aceito_pelo_navegador_e_um_site_qualquer_nao():
    cliente = app_com({"CORS_ORIGINS": SITE})

    permitido = pergunta_previa(cliente, SITE)
    recusado = pergunta_previa(cliente, "https://site-malicioso.example")

    assert permitido.status_code == 200 and permitido.headers["access-control-allow-origin"] == SITE
    assert "authorization" in permitido.headers["access-control-allow-headers"].lower()
    assert recusado.status_code == 400 and "access-control-allow-origin" not in recusado.headers
    # e o pedido de verdade também volta com o cabeçalho, para o navegador entregar a resposta ao site
    resposta = cliente.post("/auth/login", headers={"Origin": SITE})
    assert resposta.headers["access-control-allow-origin"] == SITE


def test_sem_configurar_o_site_publicado_e_recusado_e_o_local_continua_valendo():
    cliente = app_com({})

    assert pergunta_previa(cliente, ORIGEM_PADRAO).status_code == 200
    assert pergunta_previa(cliente, SITE).status_code == 400  # era o problema: o site público não conseguia falar com a API


def test_a_regex_aceita_as_previas_da_vercel_e_so_elas():
    cliente = app_com({"CORS_ORIGINS": SITE, "CORS_ORIGIN_REGEX": r"https://scuta-[a-z0-9-]+\.vercel\.app"})

    assert pergunta_previa(cliente, "https://scuta-git-feat-x-bruno.vercel.app").status_code == 200
    assert pergunta_previa(cliente, "https://scuta-x.vercel.app.malicioso.example").status_code == 400
    assert pergunta_previa(cliente, "https://outra-coisa.vercel.app").status_code == 400
