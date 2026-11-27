"""Popula a demonstração em um backend que já está no ar, **pela API**, sem tocar no banco.

Reproduz o mesmo conteúdo da demonstração local (25 pessoas, 50 reviews com a corrente de origens, 20 seguidas e 30
curtidas), a partir do cenário de `cenarios_demo.py`. Como só usa a API, funciona com qualquer banco, inclusive o
PostgreSQL da publicação, onde o `seed.py` (que só aceita o SQLite da demonstração) não serve. O passo a passo, com as
decisões que antecedem o uso, está em `docs/popular-demonstracao-publica.md`.

Uso (de backend/):
    uv run python scripts/popular_via_api.py --api http://localhost:8000
    uv run python scripts/popular_via_api.py --api https://API --confirmar-banco-publico --senha '<uma senha privada>'

Garantias:
- **Num endereço que não é local, só roda com `--confirmar-banco-publico`.** Sem a confirmação ele recusa antes de qualquer
  pedido de escrita, e `--dry-run` mostra o que faria.
- **Confere o catálogo antes de criar a demonstração.** Se faltarem músicas da demonstração, ou se houver músicas a mais (por
  exemplo, as 6 de teste misturadas às 20), ele para. Criar a demonstração num catálogo errado é o erro que este passo evita.
- **É idempotente:** rodar de novo não duplica contas, reviews, seguidas nem curtidas.
- As datas das reviews são as de agora (a API não aceita outra), mas a ordem de publicação é a do cenário.
- As contas criadas **não podem ser apagadas pela API**. Quem usar isto num banco público deve preferir `--senha` privada,
  porque a senha padrão da demonstração está no repositório.
"""

import argparse
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from catalogo_musical import carregar_catalogo  # noqa: E402
from cenarios_demo import preparar_cenario  # noqa: E402
from seed_demo import SENHA_DEMO  # noqa: E402

HOSTS_LOCAIS = {"localhost", "127.0.0.1", "::1", "testserver"}
ESPERAS = (5, 10, 20, 30, 45)  # entre tentativas, quando o serviço está acordando ou instável
STATUS_TRANSITORIOS = {502, 503, 504}


class ErroPreparacao(Exception):
    """Algo impede de popular com segurança. A mensagem diz o quê e como resolver."""


@dataclass
class Resumo:
    contas_criadas: int = 0
    contas_existentes: int = 0
    reviews_criadas: int = 0
    reviews_existentes: int = 0
    seguidas: int = 0
    curtidas: int = 0
    avisos: list[str] = field(default_factory=list)


def endereco_e_local(api: str) -> bool:
    return (urlparse(api).hostname or "") in HOSTS_LOCAIS


def exigir_confirmacao(api: str, confirmado: bool, dry_run: bool) -> None:
    """Recusa, antes de qualquer pedido, popular um endereço que não é local sem a confirmação explícita."""
    if endereco_e_local(api) or confirmado or dry_run:
        return
    raise ErroPreparacao(
        f"{api} não é um endereço local, e popular um banco público grava dados que ficam lá. "
        "Se é isso mesmo, repita o comando com --confirmar-banco-publico (ou use --dry-run para só ver o plano)."
    )


def chamar(http: httpx.Client, metodo: str, caminho: str, *, esperas: tuple[int, ...] = ESPERAS, **kwargs) -> httpx.Response:
    """Um pedido com novas tentativas para o que costuma ser passageiro (o Render gratuito hiberna e acorda devagar)."""
    ultimo: Exception | None = None
    for espera in (*esperas, None):
        try:
            resposta = http.request(metodo, caminho, **kwargs)
            if resposta.status_code not in STATUS_TRANSITORIOS:
                return resposta
            ultimo = RuntimeError(f"HTTP {resposta.status_code}")
        except (httpx.TimeoutException, httpx.TransportError) as erro:
            ultimo = erro
        if espera is None:
            break
        time.sleep(espera)
    raise ErroPreparacao(f"o servidor não respondeu a {metodo} {caminho} depois de várias tentativas ({ultimo})")


def entrar(http: httpx.Client, username: str, senha: str) -> str | None:
    resposta = chamar(http, "POST", "/auth/login", json={"username": username, "password": senha})
    if resposta.status_code == 200:
        return resposta.json()["token"]
    if resposta.status_code == 401:
        return None
    raise ErroPreparacao(f"login de {username} deu HTTP {resposta.status_code}: {resposta.text[:120]}")


def cabecalho(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def conferir_catalogo(http: httpx.Client, token: str, cenario: dict, permitir_extras: bool) -> dict[str, int]:
    """`{chave do catálogo: id}`. Para se faltar música da demonstração ou se houver música a mais."""
    ids: dict[str, int] = {}
    offset, total = 0, 1
    while offset < total:
        pagina = chamar(http, "GET", f"/musicas?offset={offset}&limit=100", headers=cabecalho(token)).json()
        total = pagina["total"]
        ids.update({m["chave_catalogo"]: m["id"] for m in pagina["items"]})
        offset += len(pagina["items"]) or total
    esperadas = {m["chave_catalogo"] for m in cenario["musicas"]}
    faltam = sorted(esperadas - set(ids))
    # Músicas a mais são aceitas (ex.: o catálogo ampliado data/musicas_publico.json), exceto as fictícias de teste
    # do catálogo padrão, que indicam a mistura que o passo a passo manda evitar.
    de_teste = {m["chave_catalogo"] for m in carregar_catalogo()} & set(ids)
    if faltam:
        raise ErroPreparacao(
            f"faltam {len(faltam)} das {len(esperadas)} músicas da demonstração no catálogo deste servidor "
            f"(ele tem {len(ids)}). Provavelmente falta CATALOGO_MUSICAL_PATH=data/musicas_demo.json no servidor. "
            "Nada foi criado além da primeira conta."
        )
    if de_teste and not permitir_extras:
        raise ErroPreparacao(
            f"o catálogo deste servidor tem {len(de_teste)} música(s) fictícia(s) de teste misturadas às da "
            "demonstração. Para um catálogo limpo, recrie o banco antes (veja o passo a passo). "
            "Se quiser popular assim mesmo, use --permitir-musicas-extras."
        )
    return ids


def contas_fora_da_demo(http: httpx.Client, cenario: dict) -> list[str]:
    demo = {u["username"] for u in cenario["usuarios"]}
    existentes: list[str] = []
    offset, total = 0, 1
    while offset < total:
        pagina = chamar(http, "GET", f"/usuarios?offset={offset}&limit=100").json()
        total = pagina["total"]
        existentes += [u["username"] for u in pagina["items"]]
        offset += len(pagina["items"]) or total
    return sorted(set(existentes) - demo)


def popular(http: httpx.Client, cenario: dict, senha: str, *, permitir_extras: bool = False, dry_run: bool = False,
            log=print) -> Resumo:
    resumo = Resumo()
    usuarios = cenario["usuarios"]
    primeiro = usuarios[0]["username"]

    # 1) uma conta para poder consultar o catálogo (a rota exige login); é a única coisa criada antes da conferência
    token = entrar(http, primeiro, senha)
    if token is None:
        if dry_run:
            log("[dry-run] a conta de referência ainda não existe, então não dá para conferir o catálogo sem criar nada.")
            _mostrar_plano(cenario, log)
            return resumo
        resposta = chamar(http, "POST", "/auth/registro", json={"username": primeiro, "name": usuarios[0]["name"], "password": senha})
        if resposta.status_code == 409:
            raise ErroPreparacao(f"a conta {primeiro} já existe com outra senha. Use --senha igual à da primeira execução.")
        if resposta.status_code != 201:
            raise ErroPreparacao(f"não foi possível criar {primeiro}: HTTP {resposta.status_code} {resposta.text[:120]}")
        resumo.contas_criadas += 1
        http.patch("/usuarios/eu", json={"bio": usuarios[0]["bio"]}, headers=cabecalho(entrar(http, primeiro, senha) or ""))
        token = entrar(http, primeiro, senha)
    else:
        resumo.contas_existentes += 1
    ids_de_musica = conferir_catalogo(http, token, cenario, permitir_extras)
    log(f"Catálogo conferido: as {len(cenario['musicas'])} músicas da demonstração estão no servidor.")
    if dry_run:
        _mostrar_plano(cenario, log)
        return resumo

    # 2) as demais contas
    tokens = {primeiro: token}
    for u in usuarios[1:]:
        tk = entrar(http, u["username"], senha)
        if tk is None:
            r = chamar(http, "POST", "/auth/registro", json={"username": u["username"], "name": u["name"], "password": senha})
            if r.status_code == 409:
                raise ErroPreparacao(f"a conta {u['username']} já existe com outra senha. Use --senha igual à da primeira execução.")
            if r.status_code != 201:
                raise ErroPreparacao(f"não foi possível criar {u['username']}: HTTP {r.status_code} {r.text[:120]}")
            tk = entrar(http, u["username"], senha)
            chamar(http, "PATCH", "/usuarios/eu", json={"bio": u["bio"]}, headers=cabecalho(tk))
            resumo.contas_criadas += 1
        else:
            resumo.contas_existentes += 1
        tokens[u["username"]] = tk
    log(f"Contas: {resumo.contas_criadas} criadas, {resumo.contas_existentes} já existiam.")

    # 3) as reviews, na ordem do cenário (a origem de uma derivada sempre vem antes dela)
    id_da_review: dict[str, int] = {}
    existentes_por_autor: dict[str, dict[str, int]] = {}
    chave_da_musica = {v: k for k, v in ids_de_musica.items()}
    for p in cenario["posts"]:
        corpo = {"musica_id": ids_de_musica[p["musica"]], "nota": p["nota"], "texto": p["texto"]}
        if p["origem"]:
            corpo["origem_id"] = id_da_review[p["origem"]]
        r = chamar(http, "POST", "/posts", json=corpo, headers=cabecalho(tokens[p["autor"]]))
        if r.status_code == 201:
            id_da_review[p["chave"]] = r.json()["id"]
            resumo.reviews_criadas += 1
        elif r.status_code == 409:  # já existia: descobre o id para as curtidas e as origens
            if p["autor"] not in existentes_por_autor:
                lista = chamar(http, "GET", f"/usuarios/{p['autor']}/posts?limit=100", headers=cabecalho(tokens[p["autor"]])).json()
                existentes_por_autor[p["autor"]] = {chave_da_musica[i["musica"]["id"]]: i["id"] for i in lista["items"] if i["musica"]["id"] in chave_da_musica}
            id_da_review[p["chave"]] = existentes_por_autor[p["autor"]][p["musica"]]
            resumo.reviews_existentes += 1
        else:
            raise ErroPreparacao(f"não foi possível publicar {p['chave']} ({p['autor']}): HTTP {r.status_code} {r.text[:140]}")
    log(f"Reviews: {resumo.reviews_criadas} criadas, {resumo.reviews_existentes} já existiam.")

    # 4) seguidas e curtidas (as duas operações são idempotentes no servidor)
    for s in cenario["follows"]:
        r = chamar(http, "POST", f"/usuarios/{s['seguido']}/follow", headers=cabecalho(tokens[s["seguidor"]]))
        if r.status_code != 204:
            raise ErroPreparacao(f"seguir {s['seguido']} como {s['seguidor']} deu HTTP {r.status_code}")
        resumo.seguidas += 1
    for c in cenario["likes"]:
        r = chamar(http, "POST", f"/posts/{id_da_review[c['post']]}/curtir", headers=cabecalho(tokens[c["usuario"]]))
        if r.status_code != 200:
            raise ErroPreparacao(f"curtir {c['post']} como {c['usuario']} deu HTTP {r.status_code}")
        resumo.curtidas += 1
    log(f"Seguidas: {resumo.seguidas}. Curtidas: {resumo.curtidas}.")
    return resumo


def _mostrar_plano(cenario: dict, log) -> None:
    log(f"[dry-run] criaria até {len(cenario['usuarios'])} contas, {len(cenario['posts'])} reviews "
        f"({sum(1 for p in cenario['posts'] if p['origem'])} derivadas), {len(cenario['follows'])} seguidas e "
        f"{len(cenario['likes'])} curtidas. Nada foi gravado.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--api", required=True, help="endereço do backend, ex.: http://localhost:8000")
    parser.add_argument("--senha", default=SENHA_DEMO, help="senha das contas da demonstração (padrão: a do repositório)")
    parser.add_argument("--dry-run", action="store_true", help="só mostra o plano e confere o catálogo; não grava nada")
    parser.add_argument("--confirmar-banco-publico", action="store_true", help="obrigatório para endereços que não são locais")
    parser.add_argument("--permitir-contas-existentes", action="store_true", help="aceita popular um banco que já tem contas fora da demonstração")
    parser.add_argument("--permitir-musicas-extras", action="store_true", help="aceita um catálogo com músicas além das 20 da demonstração")
    args = parser.parse_args()
    api = args.api.rstrip("/")
    cenario = preparar_cenario()
    try:
        exigir_confirmacao(api, args.confirmar_banco_publico, args.dry_run)
        with httpx.Client(base_url=api, timeout=60, follow_redirects=False) as http:
            print(f"Servidor: {api} ({'local' if endereco_e_local(api) else 'PÚBLICO'})")
            chamar(http, "GET", "/openapi.json", esperas=(5, 10, 20, 30, 45, 60))  # espera o servidor acordar
            estranhas = contas_fora_da_demo(http, cenario)
            if estranhas:
                print(f"Contas que já existem e não são da demonstração: {', '.join(estranhas)}")
                if not endereco_e_local(api) and not args.permitir_contas_existentes and not args.dry_run:
                    raise ErroPreparacao("o banco público já tem contas de outras pessoas; elas ficam como estão. "
                                         "Se é isso mesmo, repita com --permitir-contas-existentes.")
            popular(http, cenario, args.senha, permitir_extras=args.permitir_musicas_extras, dry_run=args.dry_run)
    except ErroPreparacao as erro:
        print(f"\nNÃO POPULEI: {erro}", file=sys.stderr)
        return 2 if "--confirmar-banco-publico" in str(erro) else 1
    print("\nPronto." if not args.dry_run else "\nPlano conferido; nada foi gravado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
