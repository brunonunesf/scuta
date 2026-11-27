"""Exercita a jornada pública e a recuperação do estado num PostgreSQL real."""
from fastapi.testclient import TestClient


def test_cadastro_reviews_e_reinicio(app_postgres):
    senha = "senha-integracao-123"
    with TestClient(app_postgres) as client:
        assert client.get("/health").status_code == 200
        preflight = {"Origin": "https://scuta-app.vercel.app", "Access-Control-Request-Method": "POST",
                     "Access-Control-Request-Headers": "content-type,authorization"}
        assert client.options("/auth/login", headers=preflight).headers["access-control-allow-origin"] == preflight["Origin"]
        preflight["Origin"] = "https://nao-permitido.example"
        assert client.options("/auth/login", headers=preflight).status_code == 400
        cabecalhos = {}
        for nome in ("ana_pg", "bia_pg"):
            dados = {"username": nome, "name": nome, "password": senha}
            assert client.post("/auth/registro", json=dados).status_code == 201
            assert client.post("/auth/registro", json=dados).status_code == 409
            assert client.post("/auth/login", json={"username": nome, "password": "errada"}).status_code == 401
            login = client.post("/auth/login", json={"username": nome, "password": senha})
            assert login.status_code == 200
            cabecalhos[nome] = {"Authorization": "Bearer " + login.json()["token"]}
        ana, bia = cabecalhos.values()
        assert client.get("/auth/eu", headers=ana).json()["username"] == "ana_pg"
        assert client.get("/auth/eu").status_code == 401
        catalogo = client.get("/musicas?limit=100", headers=ana).json()
        assert catalogo["total"] > 0
        musica = catalogo["items"][0]["id"]
        corpo = {"musica_id": musica, "nota": 8, "texto": "Teste de persistência PostgreSQL"}
        resposta = client.post("/posts", json=corpo, headers=ana)
        assert resposta.status_code == 201, resposta.text
        raiz = resposta.json()["id"]
        assert client.post("/posts", json=corpo, headers=ana).status_code == 409
        resposta = client.post("/posts", json={**corpo, "origem_id": raiz}, headers=bia)
        assert resposta.status_code == 201, resposta.text
        derivada = resposta.json()["id"]
        assert client.get("/usuarios/ana_pg", headers=ana).json()["reputacao"] == 4
        assert client.delete(f"/posts/{raiz}", headers=ana).status_code == 204
        nova = client.post("/posts", json=corpo, headers=ana)
        assert nova.status_code == 201, nova.text
        assert nova.json()["id"] > derivada  # sequência não reutiliza a origem apagada
        nova_id = nova.json()["id"]

    # Novo lifespan + pool descartado: reabre conexões e reconstrói todas as estruturas.
    from app.db import engine
    from app.core.floresta import floresta
    from app.core.reputacao import reputacao_reviews
    engine.dispose()
    floresta.reconstruir([])
    reputacao_reviews.reconstruir(floresta, [])
    with TestClient(app_postgres) as client:
        assert client.get("/auth/eu", headers=ana).json()["username"] == "ana_pg"
        assert client.post("/auth/login", json={"username": "ana_pg", "password": senha}).status_code == 200
        assert client.get("/musicas?limit=100", headers=ana).json()["total"] == catalogo["total"]
        assert client.get(f"/posts/{nova_id}", headers=ana).json()["texto"] == corpo["texto"]
        assert client.get(f"/posts/{derivada}", headers=bia).json()["origem_id"] == raiz
        arvore = client.get(f"/posts/{derivada}/arvore", headers=bia)
        assert arvore.status_code == 200, arvore.text
        assert arvore.json()["raiz"]["id"] == raiz
        assert client.get("/usuarios/ana_pg", headers=ana).json()["reputacao"] == 4
