# Deploy: colocar o scuta no ar

O site (frontend) fica na **Vercel** e o backend no **Render**, ambos no plano gratuito. O site sozinho não funciona: ele
chama o backend, e sem um backend publicado o cadastro e o login falham. Este passo a passo vale para o repositório
`brunonunesf/scuta` (o fork). O bônus de deploy da rubrica é conferido abrindo o endereço público e fazendo cadastro,
login, post, seguir e feed.

**Ordem importante:** primeiro o backend (para ter o endereço dele), depois o site (que precisa desse endereço) e, por fim,
voltar ao backend para liberar o endereço do site.

## Passo 1: backend no Render

1. Crie uma conta em [render.com](https://render.com) (dá para entrar com o GitHub).
2. **Opção A (Blueprint):** *New +* > *Blueprint* e escolha o repositório `scuta`. O Render lê o `render.yaml` da raiz e
   cria tudo sozinho. Se ele não listar o repositório, use a opção B.
3. **Opção B (manual):** *New +* > *Web Service* > *Public Git Repository*, cole `https://github.com/brunonunesf/scuta` e
   preencha (os mesmos valores do `render.yaml`):

   | Campo | Valor |
   |---|---|
   | Root Directory | `backend` |
   | Runtime | Python 3 |
   | Build Command | `pip install uv && uv sync --frozen` |
   | Start Command | `uv run python scripts/seed.py && uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | Instance Type | Free |

   Em *Environment Variables*:

   | Variável | Valor |
   |---|---|
   | `PYTHON_VERSION` | `3.12.3` |
   | `DATABASE_URL` | `sqlite:///./demo/issue13.db` |
   | `CATALOGO_MUSICAL_PATH` | `data/musicas_demo.json` |

   **Não crie a variável `DEBUG`.** Com `DEBUG=true` a autenticação tem um atalho de teste que vira porta aberta.
4. Espere o primeiro deploy (alguns minutos: ele instala as bibliotecas). Copie o endereço do serviço, parecido com
   `https://scuta-backend.onrender.com`.
5. Abra `<endereço>/docs`. Se a documentação da API aparecer, o backend está no ar.

O comando de início **carrega a demonstração** (25 pessoas, 50 reviews e o catálogo de 20 músicas brasileiras) toda vez que
o serviço sobe, porque o plano gratuito apaga o disco a cada reinício.

## Passo 2: site na Vercel

1. Na [vercel.com](https://vercel.com), abra o projeto do site. Ele está na conta do Bruno e foi criado a partir do repositório
   antigo: em *Settings* > *Git*, aponte-o para `brunonunesf/scuta`. (Para criar um projeto novo: *Add New* > *Project* e
   importe o `scuta`; o endereço do site muda.)
2. **Root Directory:** `frontend`. A Vercel reconhece o Next.js sozinha.
3. Em *Settings* > *Environment Variables*, crie **`NEXT_PUBLIC_API_URL`** com o endereço do backend do passo 1, **sem barra
   no fim** (`https://scuta-backend.onrender.com`), para *Production* (e *Preview*, se quiser testar prévias).
4. **Faça um novo deploy.** A variável é gravada no site na hora de compilar: mudá-la sem um novo deploy não tem efeito.
5. Copie o endereço do site, parecido com `https://scuta.vercel.app`.

## Passo 3: liberar o site no backend (CORS)

Sem isto o navegador **bloqueia** todo pedido do site ao backend, mesmo com os dois no ar.

1. No Render, abra o serviço > *Environment* e crie **`CORS_ORIGINS`** com o endereço do site do passo 2, **com `https` e sem
   barra no fim** (`https://scuta.vercel.app`). Para mais de um endereço, separe por vírgula.
2. *Opcional:* para as prévias da Vercel (endereços que mudam), crie `CORS_ORIGIN_REGEX`, por exemplo
   `https://scuta-.*\.vercel\.app`.
3. O Render reinicia o serviço sozinho (e carrega a demonstração de novo).

## Passo 4: verificar

Na máquina de qualquer pessoa do time, de dentro de `backend/`:

```
uv run python scripts/verificar_deploy.py --api https://scuta-backend.onrender.com --site https://scuta.vercel.app
```

Ele espera o backend acordar (até 2 minutos e meio) e confere: cadastro, login, o catálogo e as pessoas da demonstração,
seguir, publicar uma review, o feed, a área Descobrir, a reputação, o CORS e se o site aponta para este backend e não para
`localhost`. Termina com **"Tudo certo: o deploy está funcionando."**; qualquer problema vem com a causa e o que corrigir.
Depois, abra o site no navegador e faça o fluxo à mão.

## Limites do plano gratuito

- **O disco é apagado a cada reinício**: contas e reviews criadas por quem testar **somem**, e a demonstração volta ao normal.
- **Sem acessos, o Render hiberna** o backend, e a primeira abertura demora cerca de 1 minuto. Abra o site alguns minutos
  antes de uma avaliação ou de gravar o vídeo.
- **Mantenha uma única instância.** As estruturas de dados (árvore e reputação) ficam na memória de um processo só.

## Se algo não funcionar

| O que você vê | Causa provável |
|---|---|
| O site abre, mas o cadastro dá "Não foi possível conectar" | `NEXT_PUBLIC_API_URL` não foi criada na Vercel, ou faltou um novo deploy depois de criá-la |
| Erro de CORS no console do navegador, com o backend no ar | `CORS_ORIGINS` sem o endereço **exato** do site (confira `https` e a barra no fim) |
| Só 6 músicas (fictícias) ou o login da demonstração não entra | Faltou `CATALOGO_MUSICAL_PATH`, ou o Start Command não roda o `scripts/seed.py` antes do servidor |
| O deploy do Render falha ao instalar | Confira a versão do Python (`PYTHON_VERSION`) e o log de build |
| Tudo lento só na primeira vez | O serviço estava hibernado |
