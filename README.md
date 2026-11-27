# scuta — rede social de descoberta musical

Mini-projeto 3 do TRILHA, desenvolvido por **Bruno Nunes (@brunonunesf), Cecília Candeia (@cec1l14) e Daniel Dantas (@dnieldantas)**.

A proposta é descobrir e divulgar músicas pelas recomendações de outras pessoas, registrar como essas descobertas se espalham e reconhecer quem contribui para elas. Isso pode dar visibilidade a artistas pequenos e independentes.

A rede se chama **scuta**. MeetMusic foi apenas o nome provisório do começo do projeto.

## Vídeo

[▶ Assista à demonstração do scuta](https://www.youtube.com/watch?v=amKUq18zHKE) (1 min 29 s, no YouTube). Mostra o site com dados de demonstração.

## O que o scuta faz hoje

- **Conta e perfil:** cadastro, login, perfil com reputação, seguir e deixar de seguir.
- **Reviews de músicas do catálogo:** nota de 0 a 10 e texto opcional, uma review por pessoa e música. O feed mostra as reviews de quem você segue, com curtidas e comentários. Há busca de músicas, página da música e "mais avaliadas".
- **Árvore de recomendações:** uma review pode partir de outra ("escrever review a partir desta"), e a corrente aparece como árvore. A origem pode ser corrigida, e os descendentes e a reputação acompanham.
- **Reputação:** curtidas e novas reviews derivadas pontuam a corrente, com **4 pontos** para quem escreveu, **2** para a origem imediata e **1** para a seguinte.
- **Descobrir:** sugestões de reviews de músicas que você ainda não avaliou, com uma explicação em cada uma, a partir do que você avaliou e curtiu (TF-IDF sobre artista, gênero e tags).
- **Bibliotecas:** as músicas que você descobriu por outras pessoas (privadas por padrão) e as que você indicou (públicas), com controle de privacidade.
- **Reescutas:** o aviso "Ouvi novamente", com comentário opcional e no máximo um por pessoa e música a cada 24 horas.

**Ainda não existem:** a integração com Spotify e Deezer, os grupos de amigos e as mensagens diretas. O parecer técnico de cada um está em [DECISIONS.md](DECISIONS.md). O catálogo da demonstração tem 20 músicas brasileiras.

## Como rodar a demonstração

Precisa de [uv](https://docs.astral.sh/uv/) e Node.js. Em dois terminais, a partir da raiz do repositório:

```bash
# terminal 1: backend com a demonstração carregada (25 contas, 50 reviews)
cd backend
uv sync
mkdir -p demo
DATABASE_URL=sqlite:///./demo/issue13.db CATALOGO_MUSICAL_PATH=data/musicas_demo.json uv run python scripts/seed.py
DATABASE_URL=sqlite:///./demo/issue13.db CATALOGO_MUSICAL_PATH=data/musicas_demo.json uv run uvicorn app.main:app --port 8000
```

```bash
# terminal 2: o site
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Abra `http://localhost:3000` e entre com `daniel_dantas` e a senha `demo-trilha-13-2026` (todas as contas da demonstração usam a mesma senha). Para criar uma conta nova, use "Criar conta". O banco da demonstração é um arquivo separado (`backend/demo/issue13.db`).

## Ideias discutidas

- **Feed de reviews de músicas**, com curtidas e comentários.
- **Árvores de recomendações:** uma review publicada a partir de outra se conecta à publicação de origem.
- **Reputação:** curtidas e novas recomendações geram pontos para quem participa da corrente; a parcela diminui conforme a distância até a publicação que gerou a interação.
- **Bibliotecas pessoais:** músicas descobertas por meio de outras pessoas e músicas recomendadas pelo próprio usuário.
- **Perfis e follow:** acompanhar pessoas, suas recomendações, reputação e árvores.

Exemplo: Ana recomenda uma música; Júlia a descobre pelo post de Ana e publica uma review derivada; Pedro faz o mesmo pelo post de Júlia. A corrente fica **Ana → Júlia → Pedro**. Uma curtida no post de Pedro pode pontuar os três, com valores decrescentes. **Curtir não cria uma conexão na árvore; publicar uma review derivada cria.** A fórmula aprovada dá 4 pontos a quem escreveu, 2 à origem imediata e 1 à seguinte (detalhes em [DECISIONS.md](DECISIONS.md)).

Também foram sugeridos grupos de amigos para comparar e conversar sobre o que ouviram na semana e mensagens diretas. São possibilidades em discussão, sem compromisso de implementação nesta etapa.

## Decisões de produto e o que já foi entregue

Cada pessoa terá uma review por música, com texto editável. Reviews derivadas têm uma única origem, que poderá ser corrigida sem criar ciclos; seus descendentes serão preservados e a reputação anterior será recalculada conforme a nova árvore.

O aviso “Ouvi novamente” terá comentário opcional e limite de uma publicação por pessoa/música a cada 24 horas. Ele aponta para a análise atual, sem criar outra review ou pontuar sozinho. Sua data e comentário permanecem nos avisos antigos.

- [#18: reescutas](https://github.com/brunonunesf/miniprojeto3-musica/issues/18).
- [#19: correção de origem](https://github.com/brunonunesf/miniprojeto3-musica/issues/19) e [#20: recálculo de reputação](https://github.com/brunonunesf/miniprojeto3-musica/issues/20).
- [#21: Spotify](https://github.com/brunonunesf/miniprojeto3-musica/issues/21) e [#22: Deezer](https://github.com/brunonunesf/miniprojeto3-musica/issues/22): integrações opcionais para sugerir reescutas, com confirmação antes de publicar e dependentes da disponibilidade de acesso às APIs.

Estas decisões já estão implementadas, exceto o Spotify e o Deezer, que seguem como integrações opcionais, sem implementação (o parecer técnico está em [DECISIONS.md](DECISIONS.md)). O registro manual continua disponível.

## Descobrir para você

O scuta tem uma área própria de sugestões de reviews, baseada em gêneros, tags e artista das músicas e nas curtidas e análises do usuário. Sem interações, a área mostra reviews recentes e variadas. [Planejamento e critérios da issue #23](https://github.com/brunonunesf/miniprojeto3-musica/issues/23). A área está implementada (`GET /descobrir`, com o recomendador TF-IDF do Bruno e uma explicação em cada sugestão).

## Estado atual

Este repositório contém a base oficial do [miniprojeto 3](https://github.com/TrilhaUFPB/miniproj3) e a documentação inicial da proposta. A rede musical está implementada (veja "O que o scuta faz hoje", acima). A autenticação tem cadastro, entrada automática, login, sessão persistente e saída.

- Backend: FastAPI, SQLAlchemy e SQLite.
- Frontend: Next.js, TypeScript e Tailwind.
- [Decisões e pontos em aberto](DECISIONS.md).
- [Instruções originais do projeto](docs/README-base-trilha.md), [avaliação](RUBRICA.md), [catálogo](CATALOGO.md) e [guias](docs/guias/).

### Preparar o ambiente

```bash
git clone https://github.com/brunonunesf/scuta.git
cd scuta
cd backend && uv sync && cd ..
cd frontend && npm install && cp .env.local.example .env.local && cd ..
make check
make seed-minimo
make test
```

Rodar em dois terminais:

```bash
make dev-back   # http://localhost:8000/docs
make dev-front  # http://localhost:3000/login
```

Acesse `/registro` para criar uma conta ou `/login` para entrar. O cadastro entra automaticamente. Se a conta for criada mas o login falhar, a tela de login confirma a criação e mantém o usuário preenchido; não é preciso cadastrar novamente.

O seed mínimo oferece `ana`, `bruno` e `carlos`, com a senha de demonstração `senha-forte-123`. `make seed-minimo` só popula um banco vazio; contas antigas sem hash não passam a ter senha automaticamente. Não apague um banco existente para testar: use um `DATABASE_URL` separado.

A página inicial e `/usuarios` exigem sessão na interface. A tela de usuários mantém a demonstração original do esqueleto, incluindo criação sem senha; para criar uma conta que possa entrar, use `/registro`. As rotas públicas de usuários mantêm o contrato original. A proteção de cada ação futura deve ser imposta também pelo backend.

### Sessão e validações

- O token opaco fica na chave `token` do `localStorage` e segue em `Authorization: Bearer`. Ao recarregar, `/auth/eu` valida a sessão antes de mostrar as páginas privadas.
- Uma resposta 401 autenticada limpa a sessão e leva ao login. Falha de conexão ou do servidor durante a verificação preserva o token e oferece nova tentativa, sem mostrar conteúdo privado.
- “Sair” remove a sessão deste navegador e sincroniza a saída entre abas. Não revoga o token no servidor; não há endpoint de logout nem expiração nesta entrega. `localStorage` segue o guia didático e pode ser lido por scripts da mesma origem.
- Usuário: 3–30 letras minúsculas, números ou `_`. Nome: 1–80 caracteres, sem espaços nas extremidades. Senha: pelo menos 8 caracteres e no máximo 72 bytes UTF-8, sem truncamento; acentos e emojis podem usar vários bytes.
- O bypass `X-User-Id` só funciona com `DEBUG=true`. Teste a autenticação real com DEBUG desligado.

### Identidade visual

A interface usa laranja e Merriweather. Login e boas-vindas seguem uma composição de capa de álbum, responsiva, com pautas e notas em movimento suave. O título do login usa um alfabeto musical próprio aprovado por Bruno, disponível nas [pranchas de desenho](docs/identidade/README.md). O controle de pausa e a preferência de movimento reduzido permitem uma versão estática.

### Verificar a autenticação

```bash
make test
make check
cd frontend
npm run build
npm run typecheck
npx playwright install chromium
npm run test:e2e
```

Os testes do navegador iniciam frontend de produção e backend nas portas 3000 e 8000, que precisam estar livres. Eles usam um SQLite descartável em pasta temporária, com `DEBUG=false`, sem alterar o banco local. O build deve usar `NEXT_PUBLIC_API_URL=http://localhost:8000` (valor padrão do projeto). Caso já tenha Google Chrome instalado, pode usar `PLAYWRIGHT_CHANNEL=chrome npm run test:e2e`.

A suíte cobre desktop e largura de 360 px, cadastro, login, refresh, Bearer, páginas privadas, token inválido, falhas de conexão/servidor, saída entre abas, teclado e validação de formulários. Capturas ficam em `frontend/test-results/`, ignorado pelo Git. Os testes de outras features ainda marcados como pendentes não significam conclusão do núcleo.

Os detalhes de setup estão no [guia de setup](docs/guias/00-setup.md).

## Trabalho em equipe

Cada integrante pode contribuir com código e documentação. Para implementação, o guia oficial sugere uma branch por feature e revisão por outra pessoa. As responsabilidades serão combinadas entre os três; nenhuma foi atribuída automaticamente.

As [issues iniciais](https://github.com/brunonunesf/miniprojeto3-musica/issues) organizam o núcleo, os diferenciais musicais e a avaliação de ideias opcionais. São um ponto de partida: qualquer integrante com acesso ao repositório pode criar novas issues, sugerir funcionalidades e discutir mudanças de escopo. Não é necessário estar atribuído a uma issue para propor outra. As responsabilidades serão combinadas pelo time.

Usem o template de feature ou abram uma issue em branco para decisões, dúvidas e novas ideias. Este repositório (`scuta`) é um fork público do projeto do Trilha: só quem for convidado como colaborador altera o código. As issues e os PRs até 27/11 ficaram no repositório original, renomeado para [`scuta-backup`](https://github.com/brunonunesf/scuta-backup).

**Entrega:** 27/11/2026, conforme o material oficial. O guia de setup menciona um convite do GitHub Classroom para gerar o repositório do time. Como esse convite não foi fornecido, este repositório foi preparado na conta de Bruno; confirmem com a organização se a entrega deverá ser vinculada ou transferida para o Classroom.

## Origem da proposta

Síntese das mensagens de texto sobre música da conversa do grupo em 18 e 19/11/2026, priorizando a proposta detalhada de Daniel em 19/11. Os áudios não foram transcritos e seu conteúdo não foi inferido. O histórico privado, os áudios e os demais anexos não fazem parte do repositório.

### Catálogo musical — entrega de dados da #9

O catálogo inicial contém seis faixas e artistas **fictícios**, com identidades distintas para original, remix, ao vivo e remaster. A entrega inclui dados, carregamento/validação independente e testes, sem banco, API ou interface. Veja o [contrato, a curadoria e os comandos de validação](backend/data/README.md). Persistência e vínculo com reviews serão integrados pelos responsáveis de backend; seleção e apresentação, pela responsável de frontend. A #9 permanece aberta.

### Seed musical da issue #13

`make seed-validar` confere a massa de demonstração sem banco. `make seed` agora
exige `DATABASE_URL=sqlite:///./demo/issue13.db` (resolvido dentro de `backend/`)
e usa a carga completa com origens oficiais. Configure também
`CATALOGO_MUSICAL_PATH=data/musicas_demo.json` no seed e no backend.
O seed antigo de três usuários continua disponível em `make seed-minimo`;
a orientação anterior de `make seed` para essas contas foi substituída.
Consulte [cenários, versões musicais e pendências](docs/demo-issue-13.md).
A entrega de dados da #13 tem carga completa, preservação e reset com backup validados.
O reset exige aplicação parada e `--reset-demo --confirmar-reset --aplicacao-parada`.
Veja o [relatório de aceite e evidências](docs/evidencias/issue13/README.md).

## Feed e descoberta — planejamento visual aprovado em 25/11

O feed continua cronológico, com reviews dos seguidos. Pesquisa e músicas mais avaliadas na comunidade formam uma área própria; Descobrir mantém sugestões personalizadas. Veja o [plano, contratos e responsabilidades](docs/feed-e-descoberta.md) e o [rascunho visual aprovado](docs/planejamento/feed-descoberta-rascunho.png). São entregas planejadas, ainda dependentes das implementações e integrações nas issues.

Na demo musical, use `CATALOGO_MUSICAL_PATH=data/musicas_demo.json` tanto no seed
quanto no backend. O adaptador incorpora as origens oficiais do #78 e permite a carga completa
com corrente, ramo e raiz independente. O encerramento da entrega de dados não
declara Descobrir ou reputação pelo perfil/API concluídos; veja os limites e o
roteiro na [documentação da demonstração](docs/demo-issue-13.md).
