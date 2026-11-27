# Popular a demonstração no site público

**Estado:** proposta para decisão do grupo. Nada disto foi executado no banco público. O script foi testado só em
backends locais descartáveis.

## Por que isto existe

O site público (`scuta-app.vercel.app`) foi publicado, por decisão registrada no `DECISIONS.md`, com banco novo, **sem
seed de demonstração**. Resultado hoje: catálogo com 6 músicas fictícias de teste e só contas de teste. Quem abre o
site vê o feed vazio, não tem ninguém para seguir e o nicho de música brasileira não aparece. O `scripts/seed.py` não
serve para o banco público (só aceita o SQLite da demonstração), então `scripts/popular_via_api.py` faz o mesmo conteúdo
**pela API**: 25 pessoas, 50 reviews (com a corrente de origens), 20 seguidas e 30 curtidas.

## Decisões que antecedem (do grupo, principalmente do Bruno)

1. **Queremos demonstração pública?** Se sim, o catálogo precisa conter as 20 músicas da demo; o `data/musicas_publico.json` tem essas 20 mais 30 clássicas brasileiras.
2. **A senha.** A senha padrão da demonstração está no repositório público. Use `--senha` com uma senha privada se
   as 25 contas ficarem num site aberto na internet. As contas não podem ser apagadas pela API.
3. **Os dados anteriores.** Hoje o banco tem 3 contas de teste. Mantê-las é inofensivo.

## O ponto que pega: o catálogo não se "troca"

Definir `CATALOGO_MUSICAL_PATH=data/musicas_demo.json` num banco que já importou o catálogo padrão **soma** as
músicas: ficam **26** (6 de teste + 20). Testado localmente. O script **recusa** esse estado. Para um catálogo
limpo, o primeiro boot com a variável nova tem de acontecer num banco **vazio**.

O guia 08 diz para nunca apagar/recriar o banco. Por isso o caminho abaixo **não apaga**: cria um banco novo ao
lado e deixa o atual intacto, para voltar atrás.

## Passo a passo (Bruno, que tem as contas do Neon e do Render)

1. **Neon:** criar um banco novo e vazio (ex.: `scuta_demo`) no mesmo projeto, ou uma nova branch vazia. Copiar a
   string de conexão. **Não apagar** o banco `scuta` atual.
2. **Render:** no serviço `scuta-api-hbo2`, em Environment:
   - trocar `DATABASE_URL` pela string do banco novo;
   - adicionar `CATALOGO_MUSICAL_PATH` = `data/musicas_publico.json` (as 20 da demo + 30 clássicas; use `data/musicas_demo.json` se quiser só as 20).
3. **Render:** fazer o deploy manual (o guia mantém o deploy automático desligado). Esperar `/health` responder 200.
4. **Conferir sem gravar nada** (de `backend/`):
   ```bash
   uv run python scripts/popular_via_api.py --api https://scuta-api-hbo2.onrender.com --dry-run
   ```
   Como a conta de referência ainda não existe, ele só mostra o plano. Para que ele confira o catálogo antes, o
   passo seguinte cria **uma** conta (`bruno_nunes`) e, se o catálogo estiver errado, para ali.
5. **Popular de verdade** (as flags de confirmação são obrigatórias, de propósito):
   ```bash
   uv run python scripts/popular_via_api.py \
     --api https://scuta-api-hbo2.onrender.com \
     --confirmar-banco-publico --permitir-contas-existentes \
     --senha '<senha privada>'
   ```
   Pode demorar alguns minutos (o plano gratuito hiberna; o script espera e tenta de novo). Rodar de novo é seguro:
   não duplica nada.
6. **Verificar:** entrar no site com `bruno_nunes` e a senha escolhida: o feed deve mostrar reviews, Descobrir deve
   sugerir músicas, e o catálogo deve mostrar as 50 músicas brasileiras.
7. **Voltar atrás, se algo der errado:** restaurar `DATABASE_URL` para o banco `scuta` antigo, remover
   `CATALOGO_MUSICAL_PATH` e fazer o deploy manual.

Nota: `--permitir-contas-existentes` só é necessário se o banco novo já tiver contas. Num banco novo e vazio, pode
ser omitido.

## O que o script garante (testado localmente)

- Em endereço não local, **recusa sem `--confirmar-banco-publico`**, antes de qualquer pedido.
- **Catálogo errado → para.** Com 6 músicas (faltam as 20) ou com as 6 de teste misturadas às outras, ele não cria a demonstração. Com o catálogo de 50 ele popula normalmente (testado).
- **Idempotente:** a segunda rodada reporta 0 contas, 0 reviews criadas.
- Resultado no teste local: 25 contas, 50 reviews, 20 seguidas, 30 curtidas; o feed de `bruno_nunes` mostra 7
  reviews e o Descobrir 10 sugestões.

## Limites

- As datas das reviews são as de agora (a API não aceita data), mas a ordem de publicação é a do cenário.
- O `--dry-run` não consegue conferir o catálogo se a conta de referência ainda não existe (a rota de músicas exige
  login).
- Não foi testado contra PostgreSQL. A parte do script só usa a API, mas a execução real é a primeira prova.
