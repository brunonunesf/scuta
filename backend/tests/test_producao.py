import pytest
from sqlalchemy.exc import OperationalError

from app.config import origens_permitidas, validar_producao


def test_health_e_cors(client, monkeypatch):
    assert client.get("/health").json() == {"status": "ok"}
    headers = {"Origin": "http://localhost:3000", "Access-Control-Request-Method": "POST",
               "Access-Control-Request-Headers": "content-type,authorization"}
    assert client.options("/auth/login", headers=headers).status_code == 200
    headers["Origin"] = "https://origem-desconhecida.example"
    resposta = client.options("/auth/login", headers=headers)
    assert resposta.status_code == 400
    assert "access-control-allow-origin" not in resposta.headers

    from app.main import engine

    def falhar():
        raise OperationalError("detalhe privado", {}, Exception("credencial privada"))

    monkeypatch.setattr(engine, "connect", falhar)
    resposta = client.get("/health")
    assert resposta.status_code == 503
    assert resposta.json() == {"status": "unavailable"}


@pytest.mark.parametrize("origens", ["*", "https://site.example/caminho", "", "https://user:senha@site.example"])
def test_cors_exige_origens_explicitas(monkeypatch, origens):
    monkeypatch.setenv("CORS_ORIGINS", origens)
    with pytest.raises(ValueError):
        origens_permitidas()


def test_producao_nao_aceita_banco_efemero_ou_bypass(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./app.db")
    with pytest.raises(ValueError, match="PostgreSQL"):
        validar_producao()
    monkeypatch.setenv("DATABASE_URL", "postgresql://exemplo/banco")
    monkeypatch.setenv("CORS_ORIGINS", "https://scuta-app.vercel.app")
    monkeypatch.setenv("DEBUG", "true")
    with pytest.raises(ValueError, match="DEBUG"):
        validar_producao()
    monkeypatch.setenv("DEBUG", "false")
    validar_producao()
