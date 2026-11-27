# Deploy do Scuta: Vercel + Render Free + Neon Free

O frontend permanece em https://scuta-app.vercel.app/ (também acessível em
https://miniprojeto3-musica.vercel.app/). A API é um serviço Python no Render;
o banco persistente é PostgreSQL 16 no Neon. Apenas os planos Free são usados.
O banco público começa novo: o catálogo versionado é importado no boot, sem
contas locais e sem seed de demonstração.

## Publicação verificada em 27/11/2026

- Site: https://scuta-app.vercel.app/
- API: https://scuta-api-hbo2.onrender.com
- Saúde: https://scuta-api-hbo2.onrender.com/health
- Código publicado: `5ebd403cb2f180272678ceb422d8f4b9e3eb9d7a` ([PR #2](https://github.com/brunonunesf/scuta/pull/2)).
- Render Free: `scuta-api-hbo2`, uma instância/worker; Blueprint `scuta-api` acompanha `main`, com sync e deploy automáticos desativados.
- Neon: projeto `scuta`, PostgreSQL 16, plano Free; banco `scuta`, branch `production`.
- Vercel: projeto existente `scuta`, domínio preservado e Git reconectado ao fork atual (antes apontava ao backup).

Validação: 549 testes SQLite e uma jornada de integração PostgreSQL aprovados;
build/typecheck, dois testes de configuração do frontend e 14 cenários de
autenticação desktop/mobile aprovados. No site real, cadastro com entrada
automática, saída, novo login, catálogo e publicação de review funcionaram.
Após uma republicação real da API, a sessão, conta e review permaneceram;
`/health` retornou 200. O bundle público aponta para a API HTTPS e o preflight
CORS do domínio público retornou 200. Sem logs de nível error na janela da
publicação (13:51–13:57, America/Fortaleza).

Foi criada uma conta identificada como **Teste de publicação**, com uma review
de validação. Não foram importados usuários locais nem executado seed de demo.
A conta de teste foi desconectada do navegador após a verificação.
A hibernação real após 15 minutos sem acesso não foi aguardada nesta sessão;
a indisponibilidade temporária e a tentativa posterior estão cobertas nos
testes, e a limitação de início a frio permanece aplicável ao plano gratuito.

## 1. Banco no Neon

Criar um projeto **Free** chamado `scuta`, região AWS US East 1, PostgreSQL 16,
banco `scuta`, branch `production`. Manter o plano gratuito e o comportamento
de suspensão oferecido pelo plano. Não ativar upgrade nem recursos pagos.
Guardar a connection string na variável secreta `DATABASE_URL` do Render.
A aplicação aceita `postgresql://` e `postgresql+psycopg://`, normaliza o driver
e exige TLS para hosts remotos. Não colocar essa URL em `NEXT_PUBLIC_*`, no
Git ou em exemplos de comandos com senha real.

O esquema novo é criado pelos modelos SQLAlchemy. O atualizador legado por
`PRAGMA` só roda no SQLite; não é um sistema de migrações PostgreSQL. Mudanças
futuras de esquema precisam de migração explícita antes do deploy.

## 2. Serviço no Render

Conectar o repositório **brunonunesf/scuta** atual, não `scuta-backup`.
O `render.yaml` da raiz é a configuração de referência:

- Runtime Python 3.12, região Virginia, plano **Free**, branch `main`.
- Root Directory: `backend`.
- Build: `pip install uv && uv sync --frozen --no-dev`.
- Start: `uv run --no-sync uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1`.
- Health Check Path: `/health`.
- Deploy automático desativado: publicar somente depois dos testes.

Variáveis:

| Nome | Valor |
| --- | --- |
| `ENVIRONMENT` | `production` |
| `DEBUG` | `false` |
| `DATABASE_URL` | Connection string secreta do Neon |
| `CORS_ORIGINS` | `https://scuta-app.vercel.app,https://miniprojeto3-musica.vercel.app` |
| `PYTHON_VERSION` | `3.12.12` |

Se a criação for feita pelo formulário/API sem Root Directory, prefixar os
comandos de build e start com `cd backend &&`. Não executar o seed de demo,
reset de banco nem manter dados no filesystem efêmero do Render.

**Uma instância, um worker:** árvores e reputação têm estado em memória,
reconstruído a partir do banco no boot. Não aumentar workers ou sobrepor
instâncias atendendo escritas sem rever essa arquitetura.

`GET /health` consulta o banco e retorna `200 {"status":"ok"}` ou
`503 {"status":"unavailable"}`. É público e não expõe credenciais.

## 3. Frontend na Vercel

Usar o projeto existente `scuta`, Root Directory `frontend`, Node 22 e domínio
`scuta-app.vercel.app`. Confirmar a conexão Git com o **identificador do novo
fork**: renomear o repositório anterior pode manter a integração no backup.

Definir `NEXT_PUBLIC_API_URL` em **Production** com a URL HTTPS real retornada
pelo Render, sem barra final. Então fazer um **novo build/deploy**: a variável
é incorporada ao JavaScript, não basta alterá-la depois do build. Não conectar
previews de PRs ao banco público automaticamente; para testá-los, usar uma API
separada e adicionar somente a origem exata dela no ambiente correspondente.

O build falha se a URL estiver ausente, não usar HTTPS ou apontar para localhost.
Em desenvolvimento permanece o padrão http://localhost:8000. Testes locais
podem usar a exceção explícita, que nunca funciona dentro da Vercel:

```bash
cd frontend
npm ci
node --test scripts/validar-api.test.mjs
ALLOW_LOCAL_API_FOR_TESTS=true NEXT_PUBLIC_API_URL=http://localhost:8000 npm run build
PLAYWRIGHT_CHANNEL=chrome npm run test:e2e -- tests/auth.spec.ts
```

## 4. Testes antes da publicação

SQLite, preservando todos os bancos pessoais:

```bash
cd backend
uv sync --frozen --group dev
uv run pytest -q
```

PostgreSQL real, em processo separado. `TEST_POSTGRES_URL` deve apontar a uma
base de testes e estar configurada no ambiente, nunca copiada com senha para
histórico de shell ou logs:

```bash
cd backend
uv run pytest tests_postgres -v
```

A suíte cria e remove apenas um schema aleatório `scuta_test_*`; cobre cadastro,
duplicatas, senha errada, Bearer, CORS, catálogo, reviews derivadas, exclusão sem
reutilizar IDs, reconstrução e persistência após novo lifespan/pool. Sem a
variável, os testes PostgreSQL são explicitamente pulados.

## 5. Aceite no site público

1. Abrir a URL real da API com `/health` e conferir HTTP 200.
2. Abrir o site; conferir no Network que nenhuma chamada vai a localhost.
3. Criar conta de teste identificada, sair, entrar, recarregar e abrir catálogo.
4. Publicar review de teste e consultar seu perfil.
5. Reiniciar/republicar a API; confirmar conta, senha, token e review preservados.
6. Conferir desktop e 360 px. Repetir após a API ficar inativa.
7. Registrar URLs, commit, horário e resultados; nunca tokens ou senhas.

Se a API estiver indisponível, o formulário preserva os campos e permite nova
tentativa. Uma falha de rede ao validar sessão não apaga o token existente.

## 6. Limites, backup e recuperação

O Render Free suspende por inatividade e pode levar aproximadamente um minuto
para iniciar. Seu disco é efêmero; o Neon mantém os dados fora desse disco.
O PostgreSQL gratuito do Render expira em 30 dias e não é usado nesta solução.
Não criar monitores que mantenham o serviço acordado artificialmente. Conferir
consumo e erros nos painéis durante a entrega; atingir cotas pode suspender o
serviço. Não contratar upgrades para contornar limites sem nova autorização.

Antes de mudar esquema ou executar manutenção, gerar backup do PostgreSQL com
`pg_dump` usando `PGSERVICE`/arquivo de senha com permissão 0600. Exemplo com
serviço libpq previamente configurado pelo titular:

```bash
pg_dump --dbname=service=scuta --format=custom --file=scuta-backup.dump
```

Guardar o dump fora do Git. Restaurar primeiro em outro banco vazio com
`pg_restore`, conferir contagens e jornada de login, e só então planejar uma
troca. O plano Free não substitui uma rotina própria de backup.

Para regressão sem mudança de esquema: voltar ao commit anterior compatível no
Render e ao deploy anterior na Vercel, mantendo as mesmas variáveis e banco.
Nunca apagar/recriar o banco como parte de rollback. Depois repetir `/health`,
login e consulta da review. Alterações futuras de esquema exigem um plano de
compatibilidade antes de qualquer rollback.

Referências: [Render Free](https://render.com/docs/free),
[Neon Free](https://neon.com/pricing),
[SQLAlchemy + psycopg](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg).
