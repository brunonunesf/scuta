"""Configuração lida do ambiente.

Hoje só o CORS: de quais endereços o navegador pode chamar a API. Localmente o site roda em `localhost:3000`; publicado,
ele tem o endereço da Vercel, que precisa estar na lista, senão o navegador bloqueia todo pedido do site ao backend.
"""

from collections.abc import Mapping

ORIGEM_PADRAO = "http://localhost:3000"


def origens_cors(ambiente: Mapping[str, str]) -> tuple[list[str], str | None]:
    """`(origens, regex)` para o CORS.

    - `CORS_ORIGINS`: endereços do site separados por vírgula (ex.: `https://scuta.vercel.app,http://localhost:3000`).
      Sem a variável, vale só `http://localhost:3000`. A barra final é ignorada, e `*` é recusado (junto com o envio de
      credenciais o navegador o rejeitaria, e liberaria qualquer site a falar com a API).
    - `CORS_ORIGIN_REGEX` (opcional): um padrão para endereços que mudam, como as prévias da Vercel
      (ex.: `https://scuta-.*\\.vercel\\.app`).
    """
    bruto = ambiente.get("CORS_ORIGINS", "").strip()
    origens = [o.strip().rstrip("/") for o in bruto.split(",") if o.strip()] or [ORIGEM_PADRAO]
    if "*" in origens:
        raise ValueError("CORS_ORIGINS não aceita '*': liste os endereços do site, separados por vírgula")
    regex = ambiente.get("CORS_ORIGIN_REGEX", "").strip() or None
    return origens, regex
