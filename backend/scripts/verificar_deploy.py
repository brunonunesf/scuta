"""Confere um deploy público: o backend responde, a demonstração foi carregada, o fluxo da banca funciona e o site aponta
para este backend.

Uso (de backend/):
    uv run python scripts/verificar_deploy.py --api https://scuta-backend.onrender.com --site https://scuta.vercel.app

O fluxo da banca é cadastro, login, post, seguir e feed. O script cria uma pessoa de teste (`verif_xxxxx`) e uma review, e
apaga a review e o follow ao terminar. Só a pessoa de teste fica. A primeira chamada pode levar cerca de 1 minuto: o plano
gratuito do Render hiberna sem tráfego. Sai com código 1 se algum passo falhar.
"""

import argparse
import re
import secrets
import sys
import time

import httpx

SENHA_DEMO = "demo-trilha-13-2026"
falhas: list[str] = []


def passo(titulo: str, ok: bool, detalhe: str = "") -> bool:
    print(("OK       " if ok else "PROBLEMA ") + titulo + (f" — {detalhe}" if detalhe else ""))
    if not ok:
        falhas.append(titulo)
    return ok


def esperar_o_backend(api: str, http: httpx.Client, limite: int = 150) -> bool:
    print(f"Esperando o backend responder (até {limite}s, o plano gratuito acorda devagar)...")
    inicio = time.time()
    while time.time() - inicio < limite:
        try:
            if http.get(f"{api}/openapi.json").status_code == 200:
                return True
        except httpx.HTTPError:
            pass
        time.sleep(5)
    return False


def conferir_o_site(site: str, api: str, http: httpx.Client) -> None:
    resposta = http.get(f"{site}/login")
    if not passo("o site abre", resposta.status_code == 200, f"HTTP {resposta.status_code}"):
        return
    # O endereço do backend fica embutido nos scripts do site quando ele é compilado (NEXT_PUBLIC_API_URL).
    scripts = sorted(set(re.findall(r"/_next/static/[A-Za-z0-9_./~%-]*\.js", resposta.text)))[:60]
    conteudo = ""
    for caminho in scripts:
        try:
            conteudo += http.get(f"{site}{caminho}").text
        except httpx.HTTPError:
            continue
    passo("o site NÃO aponta para localhost", "localhost:8000" not in conteudo,
          "ele ainda chama localhost:8000: falta NEXT_PUBLIC_API_URL na Vercel (e um novo deploy)" if "localhost:8000" in conteudo else "")
    passo("o site aponta para este backend", api.split("://", 1)[1].rstrip("/") in conteudo,
          "não achei o endereço do backend nos scripts do site; confira NEXT_PUBLIC_API_URL" if api.split("://", 1)[1].rstrip("/") not in conteudo else "")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--api", required=True, help="endereço do backend, ex.: https://scuta-backend.onrender.com")
    parser.add_argument("--site", help="endereço do site, ex.: https://scuta.vercel.app (confere o CORS e a ligação com o backend)")
    args = parser.parse_args()
    api = args.api.rstrip("/")
    site = args.site.rstrip("/") if args.site else None

    with httpx.Client(timeout=30, follow_redirects=False) as http:
        if not passo("o backend responde", esperar_o_backend(api, http)):
            print("\nO backend não respondeu. Veja o log do serviço no painel do Render.")
            return 1

        usuario = f"verif_{secrets.token_hex(3)}"
        registro = http.post(f"{api}/auth/registro", json={"username": usuario, "name": "Verificação", "password": "senha-forte-123"})
        passo("cadastro funciona", registro.status_code == 201, f"HTTP {registro.status_code}")
        login = http.post(f"{api}/auth/login", json={"username": usuario, "password": "senha-forte-123"})
        if not passo("login funciona", login.status_code == 200, f"HTTP {login.status_code}"):
            return _fim()
        cabecalho = {"Authorization": f"Bearer {login.json()['token']}"}

        musicas = http.get(f"{api}/musicas?limit=100", headers=cabecalho).json()
        total_musicas = musicas.get("total", 0)
        passo("o catálogo da demonstração está carregado (20 músicas)", total_musicas >= 20,
              f"{total_musicas} músicas" + ("; com 6 é o catálogo de teste: falta CATALOGO_MUSICAL_PATH=data/musicas_demo.json" if total_musicas == 6 else ""))

        pessoas = http.get(f"{api}/usuarios?limit=100").json().get("total", 0)
        passo("as pessoas da demonstração estão carregadas (25)", pessoas >= 25,
              f"{pessoas} pessoas" + ("; o seed não rodou antes do servidor subir" if pessoas < 25 else ""))
        demo = http.post(f"{api}/auth/login", json={"username": "daniel_dantas", "password": SENHA_DEMO})
        passo("a conta da demonstração (daniel_dantas) entra", demo.status_code == 200, f"HTTP {demo.status_code}")

        seguiu = http.post(f"{api}/usuarios/daniel_dantas/follow", headers=cabecalho)
        passo("seguir alguém funciona", seguiu.status_code == 204, f"HTTP {seguiu.status_code}")
        musica = musicas["items"][0] if musicas.get("items") else None
        review = http.post(f"{api}/posts", headers=cabecalho, json={"musica_id": musica["id"], "nota": 8, "texto": "verificação"}) if musica else None
        passo("publicar uma review funciona", review is not None and review.status_code == 201, f"HTTP {review.status_code}" if review is not None else "catálogo vazio")
        feed = http.get(f"{api}/feed", headers=cabecalho).json()
        passo("o feed mostra as reviews de quem a pessoa segue", feed.get("total", 0) > 0, f"{feed.get('total', 0)} reviews")
        passo("a área Descobrir responde", http.get(f"{api}/descobrir", headers=cabecalho).status_code == 200)
        passo("a reputação aparece no perfil", http.get(f"{api}/usuarios/daniel_dantas", headers=cabecalho).json().get("reputacao") is not None)

        if review is not None and review.status_code == 201:  # deixa o banco como estava
            http.delete(f"{api}/posts/{review.json()['id']}", headers=cabecalho)
        http.delete(f"{api}/usuarios/daniel_dantas/follow", headers=cabecalho)

        if site:
            print()
            pergunta = {"Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "authorization,content-type"}
            previa = http.options(f"{api}/auth/login", headers={"Origin": site, **pergunta})
            passo("o backend aceita pedidos do site (CORS)", previa.headers.get("access-control-allow-origin") == site,
                  "o navegador bloquearia o cadastro: coloque o endereço do site em CORS_ORIGINS no Render" if previa.headers.get("access-control-allow-origin") != site else "")
            outra = http.options(f"{api}/auth/login", headers={"Origin": "https://site-qualquer.example", **pergunta})
            passo("e recusa um site qualquer", "access-control-allow-origin" not in outra.headers)
            conferir_o_site(site, api, http)
    return _fim()


def _fim() -> int:
    print()
    if falhas:
        print(f"{len(falhas)} problema(s): " + "; ".join(falhas))
        return 1
    print("Tudo certo: o deploy está funcionando.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
