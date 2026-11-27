# Decisões do time

**Time:** Bruno Nunes (@brunonunesf), Cecília Candeia (@cec1l14) e Daniel Dantas (@dnieldantas).

Documento inicial baseado nas mensagens de texto da conversa de WhatsApp. Ideias discutidas não significam funcionalidades prontas nem escopo fechado.

## Produto

- **Público inicial proposto:** ouvintes que descobrem músicas pelas indicações de amigos e outros ouvintes, com atenção à divulgação de artistas pequenos e independentes. O recorte mais específico ainda será validado pelo time.
- **Problema:** recomendações isoladas não mostram a corrente de descobertas nem reconhecem as pessoas que ajudaram uma música a chegar a novos ouvintes.
- **Como a rede resolve:** conectar reviews derivadas às suas origens e tornar visível a contribuição das pessoas por meio de árvores de recomendações e reputação.
- **Impacto pretendido:** incentivar a descoberta e a divulgação de artistas com menor visibilidade, como Daniel destacou na conversa.
- **Sinal de sucesso proposto, a validar:** pessoas descobrem uma música por outra pessoa e publicam uma review ligada à recomendação original.
- **Pendente de reunião (Etapa 1):** recorte específico do público (a rubrica valoriza algo como "estudantes da UFPB que querem descobrir artistas independentes locais" mais que "gente que gosta de música") Enquanto isso, seed e interface usam o recorte provisório acima. O nome da rede foi definido em 27/11: **scuta**.

## Direções de produto registradas

### 1. Descoberta musical com origem visível

A referência inicial foi um “Letterboxd de músicas”. A conversa citou Music Board como concorrente e levantou a preocupação com diferenciação. A proposta posterior de Daniel acrescenta árvores de recomendações e reconhecimento de quem divulga. A comparação com concorrentes é um relato da conversa, não uma pesquisa verificada neste repositório.

### 2. Reviews derivadas criam conexões

Uma nova review vinculada à anterior cria uma conexão na árvore. Curtir apenas gera uma interação; não adiciona uma pessoa à árvore. Exemplo: Ana → Júlia → Pedro.

### 3. Reputação distribuída pela corrente

A proposta é que curtidas e novas recomendações gerem pontos, distribuídos também aos participantes anteriores, em parcelas menores conforme a distância. Pesos, profundidade máxima, tratamento de descurtidas, exclusões, repetições e prevenção de abuso continuam em aberto.

### 4. Nome e funcionalidades complementares em aberto

“MeetMusic” é placeholder: Daniel comentou que o nome já existe. Grupos de amigos, comparação semanal do que ouviram e mensagens diretas foram sugeridos, mas ainda não são compromisso de implementação. Um recorte exclusivamente paraibano foi levantado e considerado limitado; não foi adotado como restrição do produto.

## Funcionalidades e responsabilidades

Os itens de núcleo vêm da base oficial. As prioridades e decisões de produto continuam sendo do trio; a divisão de áreas foi confirmada por Bruno em 24/11/2026.

| Pessoa | Área | Responsabilidades |
|---|---|---|
| Cecília (@cec1l14) | Frontend (`front`) | Telas, componentes, navegação e integração da interface com a API. |
| Daniel (@dnieldantas) | Backend (`back`) | APIs, persistência, permissões e integrações externas. |
| Bruno (@brunonunesf) | Dados e machine learning (`dados`) | Seed, catálogo, estruturas de dados, algoritmos de reputação e recomendador com sua validação. |

Uma funcionalidade pode envolver várias áreas. As etiquetas indicam participação, não exclusividade: o simples uso do banco é backend e não exige `dados`. Os responsáveis já atribuídos no GitHub e as contribuições anteriores são preservados. A autenticação (#2), concluída com participação de Bruno, não será redistribuída retroativamente.

| Funcionalidade | Participação por área |
|---|---|
| Autenticação (#2) | Cecília: front; Daniel: back nas manutenções futuras. Preservado o histórico de implementação de Bruno e do time. |
| Perfil, posts, follow, feed, curtidas e comentários (#3–#8) | Cecília: front; Daniel: back. |
| Músicas e reviews (#9) | Cecília: interface; Daniel: modelo persistido e API; Bruno: catálogo, gêneros, tags e consistência das identidades musicais. |
| Árvores de recomendações (#10) | Cecília: visualização; Daniel: persistência e API; Bruno: estrutura e algoritmos de percurso e prevenção de ciclos. |
| Reputação (#11) e recálculo (#20) | Bruno: cálculo e validação; Daniel: eventos, persistência e API; Cecília: exibição e feedback. |
| Bibliotecas (#12) | Cecília: telas; Daniel: consultas e autorização. |
| Seed e demonstração (#13) | Bruno: dados fictícios, cenários e validação do seed; roteiro e apresentação continuam coletivos. |
| Grupos e mensagens (#14–#15) | Avaliação coletiva; Cecília avalia a experiência e Daniel a viabilidade do backend. Implementação depende da decisão de produto. |
| Reescutas (#18) | Cecília: interface; Daniel: registros, permissões e limite de 24 horas. |
| Correção de origem (#19) | Cecília: confirmação e feedback; Daniel: alteração persistida e integração; Bruno: validação da árvore e integração com o recálculo. |
| Spotify e Deezer (#21–#22) | Daniel: viabilidade, autorização e API; Cecília: conexão e confirmação na interface. Integrações opcionais. |
| Descobrir (#23) | Bruno: recomendador TF-IDF, similaridade e validação; Daniel: endpoint e integração; Cecília: tela e explicação das sugestões. |

A divisão organiza o trabalho futuro e não altera o estado de conclusão das funcionalidades. Os registros de andamento e implementação nas demais seções são históricos e devem ser lidos com suas datas.

## Escopo e cortes (proposta)

- **Entra:** núcleo oficial; review de música com nota (nota ainda é proposta); review derivada que aponta para a origem; visualização da árvore; reputação com pontuação decrescente por distância.
- **Prioridade para a demonstração de 27/11:** árvores de recomendações e área personalizada “Descobrir” (#23), após o núcleo necessário. Reputação entra com a fórmula básica 4/2/1; detalhes de interface e otimizações podem evoluir depois. O time tentará entregar o máximo viável conforme o andamento. Bibliotecas, grupos, mensagens diretas e integrações com streaming não são pré-requisitos das duas prioridades.

## Decisões técnicas propostas (a confirmar na reunião)

1. **Identificação das músicas:** a decisão de produto é distinguir cada faixa/versionamento selecionado. O modelo técnico deve guardar identificadores de serviço quando disponíveis e identificador local para entradas manuais; não presumir equivalência entre serviços apenas por título/artista.
2. **Review como post:** a review é um post com campos extras (música, nota, `origem_id`), reaproveitando feed, curtidas e comentários.
3. **Reputação:** a proposta anterior de pesos 1, 1/2 e 1/4 foi substituída pela decisão de 21/11/2026, descrita abaixo. A prevenção de abuso e o efeito de exclusões continuam em discussão.

## Decisões técnicas implementadas — autenticação (22/11/2026)

Seguem o guia 01 e estão na `main`. Dos 10 testes do núcleo, os 3 de autenticação passam. Além deles, `backend/tests/test_auth_casos.py` cobre os casos de borda da issue #2: cabeçalho inválido, token falso, login de usuário sem senha, resposta única de erro, ausência de senha e hash nas respostas, limites de senha e bypass com e sem `DEBUG`. Na versão da `main` de 22/11, `make test` mostrava 19 passed e 7 skipped; os 7 restantes (posts, feed, perfil, follow, curtidas, comentários e seed) continuam por fazer.

- **Sessão por token opaco em tabela.** O login cria um token aleatório (`secrets.token_urlsafe(32)`) salvo na tabela `sessions`, enviado em `Authorization: Bearer <token>`. É mais simples de depurar e revogar que JWT, que o guia deixa como opcional.
- **Senha com hash bcrypt.** A senha nunca é guardada nem devolvida. Nesta branch, o registro valida no mínimo 8 caracteres e no máximo 72 bytes UTF-8 antes do bcrypt, sem truncamento. A contagem anterior somente por caracteres foi corrigida no PR #27.
- **Login com uma única resposta de erro.** Usuário inexistente, usuário sem senha e senha errada devolvem o mesmo `401`, para não revelar quais usernames existem. Username repetido no registro devolve `409`.
- **Bypass só em desenvolvimento.** O header `X-User-Id` só vale com `DEBUG=true`. Essa variável nunca deve ser ligada no deploy; sem ela só o token autentica.
- **Token no `localStorage` do navegador.** Foi escolhido por ser mais simples de entender e depurar. A troca por cookie `httpOnly` exigiria configurar CORS com credenciais, e o trade-off (XSS contra CSRF) está descrito no guia 01.
- **Forma de saída.** Sair apaga o token guardado no navegador, como o guia 01 descreve, e leva para `/login`. Não existe rota de logout no servidor: a sessão não é revogada e o token não expira, então um token copiado antes de sair continua válido. É uma limitação conhecida e aceita para este projeto; se o time decidir revogar, bastaria uma rota `POST /auth/logout` que apague a linha de `sessions` e, se necessário, uma data de validade na tabela.
- **A home exige login.** Nesta branch, o `AuthProvider` central valida `/auth/eu` antes de montar as páginas privadas. Quem implementar o feed em `app/page.tsx` deve manter a guarda central. Uma resposta `401` com token salvo apaga o token e volta para `/login`.
- **CORS só para `localhost:3000`.** O frontend precisa rodar nessa porta; em outra, o navegador bloqueia as chamadas e a interface mostra que não conseguiu falar com o backend.
- **Seed de desenvolvimento** com os usuários `ana`, `bruno` e `carlos`, todos com a mesma senha de desenvolvimento. Esses usuários e essa senha não devem existir no deploy.

## Proposta visual da branch `feat/telas-auth` (22/11/2026)

Proposta de Cecília, implementada na branch `feat/telas-auth` e sujeita à revisão do time, já que as cores afetam todas as páginas. Esta seção registra as escolhas daquele PR; a identidade aprovada por Bruno e aplicada no PR #27 está descrita ao final deste documento.

- **Tema escuro com neon.** Fundo quase-preto, cartões um tom acima e texto em branco suave. Magenta marca as ações, ciano marca foco e navegação, e o amarelo fica reservado para notas e pontos. O brilho aparece só no botão principal e no campo em foco, para o neon continuar sendo destaque.
- **Cores centralizadas.** Ficam em um único bloco `@theme` do `globals.css`; trocar a identidade custa mudar esses valores, não as telas.
- **Componentes reutilizáveis** em `frontend/components/`: `Botao`, `Cartao`, `Campo` e `MensagemErro`. As próximas telas devem usá-los para evitar repetir classes.
- **Títulos com fonte serifada.** Dão um tom editorial e combinam com o nicho de música.
- **Alternativa descartada:** uma paleta quente (creme e laranja), usada por pouco tempo. Foi trocada pelo tema escuro porque combina mais com o clima de show e de música.
- **Pendente:** nome definitivo da rede e logo. A navbar ainda mostra "Rede da Trilha".

## Escolhas técnicas pendentes

A stack inicial é a do esqueleto oficial: FastAPI + SQLAlchemy + SQLite e Next.js + TypeScript + Tailwind. A árvore de recomendações sugere explorar uma estrutura de árvores, mas nenhuma representação, algoritmo ou complexidade foi escolhida ou medida ainda.

O modelo técnico de catálogo, os identificadores externos e a interface das árvores serão definidos nas issues de implementação. Foram aprovadas issues opcionais para investigar e implementar sugestões de reescuta via Spotify e Deezer; acesso e viabilidade ainda precisam ser validados. Não há compromisso de reprodução de áudio ou de entrega dessas integrações em 27/11.

O time validou o uso de ML de forma simples na área “Descobrir” (#23): TF-IDF dos metadados musicais e similaridade de cosseno com preferências derivadas de curtidas e reviews. A rubrica disponível não menciona ML como exigência; eventual instrução adicional da organização pode ser acompanhada na entrega. Reputação por fórmula não é ML.

## Organização e entrega

- O time decidirá a divisão das features e revisará as contribuições entre si.
- Após a preparação inicial, Bruno autorizou a criação das issues iniciais. Elas organizam o trabalho sem fechar o escopo: qualquer integrante com acesso pode abrir novas propostas. Responsáveis das Pessoas B e C permanecem a combinar.
- Já foram abertos PRs: o #16 (backend de autenticação) e o #17 (documentação) estão mesclados, e o PR das telas de cadastro e login (`feat/telas-auth`) aguarda revisão. Os PRs mesclados até agora ainda não passaram por revisão de outra pessoa do time; os próximos devem passar.
- O guia oficial menciona GitHub Classroom. O convite não foi fornecido; confirmar o destino exigido para a entrega antes da submissão.

## Uso de IA

Na preparação inicial, Codex foi usado para ler os textos exportados do WhatsApp, separar as ideias sobre música, consultar o material do miniprojeto e preparar o repositório e esta documentação. Naquela etapa, não implementou funcionalidades da rede social, não transcreveu áudios e não definiu decisões de produto ausentes da conversa.

Codex também foi usado para organizar e abrir as issues iniciais com critérios de conclusão e dependências sugeridas, mantendo ideias opcionais separadas de compromissos de implementação.

Claude Code foi usado para analisar a pasta do projeto, propor o plano de etapas até a entrega e redigir as seções de donos, escopo e decisões técnicas propostas acima. Essas propostas estão sendo decididas pelo time.

Claude Code também implementou o backend da autenticação do núcleo (bypass `X-User-Id`, registro, login, `/auth/eu`, model de sessão) e atualizou o seed com os usuários `ana`, `bruno` e `carlos`. A implementação segue o guia 01 e foi verificada com `make test` (7 passed, 7 skipped). O código ainda precisa ser revisado por uma pessoa do time.

Claude Code também implementou o frontend da autenticação (páginas `/registro` e `/login`, token no `localStorage`, guarda de rota, botão de sair na navbar) e aplicou o tema visual escuro com neon, com os componentes reutilizáveis `Botao`, `Cartao`, `Campo` e `MensagemErro`. Foi verificado com `npx tsc --noEmit` e testado à mão no navegador (cadastro, login, erro de senha e sair). Também foi usado para diagnosticar problemas de ambiente (porta do frontend e CORS, processo preso na porta do backend e cache `.next`). O código e as cores ainda precisam ser revisados por uma pessoa do time.

## Decisões de produto validadas pelo trio — 22/11/2026

Bruno informou que Cecília e Daniel revisaram e validaram as decisões de produto discutidas. O nome “MeetMusic” permanece provisório; escolher outro nome não bloqueia as funcionalidades.

| Tema | Regra aprovada |
|---|---|
| Público | Descoberta de músicas entre amigos, com espaço para artistas menores. |
| Identidade da música | Cada faixa/versionamento selecionado no aplicativo de música é um item próprio: gravação original, remix e versão ao vivo podem receber reviews diferentes. Quando uma faixa vier de Spotify ou Deezer, guardar identificador do serviço; para entrada local, usar identificador interno. Relacionar faixas de serviços diferentes somente após confirmar que representam a mesma gravação. |
| Review | Uma review ativa e editável por pessoa e item musical. Nova recomendação derivada exige texto próprio e uma única origem. Raiz não tem origem. |
| Descoberta | Publicar uma review derivada registra na biblioteca que a música foi descoberta a partir daquela origem. Publicar uma review independente registra recomendação própria, sem afirmar descoberta por outra pessoa. Visitar ou curtir não registra escuta. |
| Origem | O autor pode corrigir para outra review da mesma música sem criar ciclos; descendentes permanecem. Corrigir a origem recalcula pontos antigos e futuros. |
| Reescuta | Aviso separado no feed com comentário opcional, no máximo um por pessoa/música a cada 24 horas; aponta para a review atual, mas preserva data e comentário do aviso. Não cria nó nem pontua. |
| Bibliotecas | Controles separados. Descobertas começam privadas e recomendações públicas; o dono pode alternar. Terceiros veem aviso de acesso restrito para lista privada, sem itens, contagem ou origens. Reviews públicas seguem visíveis. |
| Prioridade | Para 27/11, tentar entregar o máximo viável, com árvores e área “Descobrir” (#23) como diferenciais de demonstração e reputação 4/2/1 básica. |
| ML | Escolha de produto: recomendar faixas e reviews em “Descobrir” com TF-IDF e similaridade, usando curtidas e reviews como sinais. O material disponível não afirma que ML é obrigação do curso. |
| Classroom | Não é condição para fechar esta decisão; o time usará o repositório atual como trabalho útil e seguirá as instruções de entrega que receber. |

**Decisão adiada:** transformar uma raiz em derivada ou remover a origem de uma derivada. A primeira versão permite corrigir uma origem já existente; ampliar esse fluxo exige regra e teste próprios. Spotify e Deezer continuam integrações opcionais para sugerir reescutas confirmadas pelo usuário.

**Exemplo de corrente:** Ana recomenda; Júlia publica uma review derivada da de Ana; Pedro publica outra a partir da de Júlia. Uma segunda pessoa pode publicar a partir da review de Ana, formando outro ramo. Cada review derivada tem uma origem, e curtidas não acrescentam nós.

### Issues relacionadas

- [#9 — Música e review](https://github.com/brunonunesf/miniprojeto3-musica/issues/9); [#10 — Árvore](https://github.com/brunonunesf/miniprojeto3-musica/issues/10); [#11 — Reputação](https://github.com/brunonunesf/miniprojeto3-musica/issues/11); [#12 — Bibliotecas](https://github.com/brunonunesf/miniprojeto3-musica/issues/12).
- [#18 — Reescutas](https://github.com/brunonunesf/miniprojeto3-musica/issues/18); [#19 — Correção de origem](https://github.com/brunonunesf/miniprojeto3-musica/issues/19); [#20 — Recálculo](https://github.com/brunonunesf/miniprojeto3-musica/issues/20); [#23 — Descobrir](https://github.com/brunonunesf/miniprojeto3-musica/issues/23).
- [#21 — Spotify](https://github.com/brunonunesf/miniprojeto3-musica/issues/21) e [#22 — Deezer](https://github.com/brunonunesf/miniprojeto3-musica/issues/22) são opcionais.

## Fórmula e exclusão confirmadas com Bruno — 21/11/2026

- **Curtida de outra pessoa em uma review:** o autor recebe 4 pontos, o autor da review de origem imediata recebe 2 e o ancestral seguinte recebe 1. Níveis anteriores não recebem. O evento de curtida é único por usuário/review; descurtir retira exatamente os pontos que ele concedeu. Recurtir após descurtir volta a conceder uma única vez.
- **Review derivada:** sua publicação gera 4 pontos para o autor da origem imediata, 2 para o ancestral seguinte e 1 para o próximo ancestral. O autor da nova review não recebe pontos por esse evento. Cada review derivada gera esse evento uma única vez; alterar a origem recalcula os créditos existentes segundo a árvore corrigida, sem criar um novo evento.
- **Curtida própria:** concede 1 ponto somente ao autor da review, sem propagar para ancestrais; descurtir remove esse ponto. A regra de unicidade também se aplica.
- **Exemplo:** Ana → Júlia → Pedro. Uma curtida externa na review de Pedro dá 4 a Pedro, 2 a Júlia e 1 a Ana. Publicar a review de Pedro dá 4 a Júlia e 2 a Ana; não há terceiro ancestral nesse caminho. Uma curtida de Pedro na própria review dá 1 somente a Pedro.
- **Exclusão:** excluir a review de Ana remove seu conteúdo e seus avisos de reescuta. A review de Júlia e as demais descendentes permanecem ligadas a um registro de origem apagada. O link para a review apagada abre uma página que informa que ela não existe mais, sem mostrar a análise. Mesmo após a exclusão, Ana conserva o crédito de origem: interações futuras com reviews descendentes continuam percorrendo o registro apagado e podem pontuar Ana conforme a fórmula. Ana pode publicar uma nova review da mesma música, como outra raiz, sem ligação automática com a antiga. A nova review não recupera o texto ou os avisos anteriores.

A fórmula usa pontos inteiros, sem arredondamento. Caso o mesmo autor apareça em mais de um nível do mesmo evento, recebe somente sua maior parcela. O recálculo após edição de origem aplica a mesma regra.

## Descobrir para você — prioridade de demonstração

- **Local:** área própria “Descobrir”, separada do feed cronológico de pessoas seguidas.
- **Sinais:** músicas analisadas e curtidas pela pessoa; review própria pesa 3 e curtida em review de outra pessoa pesa 1. Curtida própria não duplica o sinal da review.
- **Dados:** gêneros, tags e artista associados a cada identidade musical. Não usar texto de review como aprovação automática. Original, remix e versão ao vivo são identidades distintas.
- **Método inicial:** TF-IDF aprendido do catálogo local e similaridade de cosseno com o perfil de gosto. Não requer áudio, API de streaming ou treinamento supervisionado. É um recomendador simples; sua qualidade depende do catálogo e das interações disponíveis.
- **Saída:** reviews públicas e ativas de músicas ainda não analisadas, uma por identidade musical, com motivo curto baseado em características compartilhadas. Sem sinais, exibir reviews recentes e variadas e explicar que a personalização começará com interações.
- **Prioridade:** junto às árvores, é um dos dois diferenciais pretendidos para a demonstração de 27/11. Reputação básica permanece no escopo planejado; a implementação real será ajustada conforme o andamento.

Implementação e validação estão na [issue #23](https://github.com/brunonunesf/miniprojeto3-musica/issues/23). O material consultado não confirma obrigação de ML. O guia de setup cita GitHub Classroom, mas o convite não está disponível; a decisão do produto não depende dele.


## Implementação da autenticação — issue #2 — 24/11/2026

- A base local já continha o backend de autenticação integrado em `main`; a referência anterior a backend ainda isolado em branch estava desatualizada. A conclusão do front foi implementada em `feat/issue-2-autenticacao`, sem alterar branches do time.
- Escolhas finais aprovadas por Bruno: fundo claro, destaque laranja, Merriweather nos textos e alfabeto musical geométrico próprio no título do login. A entrada automática após cadastro foi mantida. A proposta inicial violeta foi substituída durante a revisão visual. O nome definitivo da rede continua em aberto; não foram adicionadas bibliotecas de componentes ou animação.
- Sessão centralizada em um provedor de contexto com verificação no carregamento. O token opaco permanece em `localStorage`, conforme o guia 01, e o cliente de API envia Bearer. Página inicial e usuários só são montados após validação de `/auth/eu`; a guarda visual não substitui autorização no backend.
- Resposta 401 de chamada autenticada limpa o estado e redireciona para login. Erros de rede/servidor preservam o token e permitem repetir a verificação. Respostas antigas não devem invalidar um token já substituído. A saída se propaga entre abas.
- Logout é local, sem revogação no servidor ou expiração de tokens. Recuperação de senha, e-mail, login social, JWT e cookies ficam fora desta entrega. Não há mudança de esquema, migração ou exclusão de dados.
- Senhas aceitam mínimo de 8 caracteres e máximo de 72 bytes UTF-8, validado antes do bcrypt. Não há truncamento. Hash vazio/inválido recebe 401 genérico; colisão de username na gravação recebe 409 após rollback. Sessão sem usuário recebe 401.
- O cadastro usa `/auth/registro`, seguido de `/auth/login`. Se o segundo passo falhar, a conta permanece criada e a interface encaminha ao login com confirmação e usuário preenchido. `/usuarios` mantém o slice de exemplo sem senha e não substitui o cadastro.
- Foi encontrado o PR #24 de Cecília (`feat/telas-auth`), que também implementa autenticação e tem proposta visual própria, descrita na seção de 22/11. Esta branch é uma implementação alternativa do plano aprovado neste chat, não uma alteração daquele PR. O time precisa conciliar as duas propostas antes de integrar; os PRs de perfil e página inicial também podem se sobrepor ao layout. Nenhum merge foi realizado automaticamente.
- Codex implementou formulários, provedor de sessão, navegação, guarda, tratamento de erros, ajustes no backend e testes. A revisão por outra pessoa continua pendente.
- Verificação: 26 testes de backend passaram; 7 testes de outras features seguem pendentes. Build de produção e TypeScript passaram. Os 12 testes de navegador passaram com Google Chrome em desktop e largura de 360 px, incluindo cadastro, login, refresh, Bearer, token inválido, erro 500, conexão interrompida, saída entre abas e teclado. Capturas de login e registro foram inspecionadas visualmente. `make check` passou com banco separado em `/tmp`, sem alterar dados locais.


## Identidade visual aprovada — 24/11/2026

- Bruno aprovou o laranja claro `#f58220`, hover `#e67412`, texto de destaque `#ad4c00` e texto escuro dos botões `#431d08`. Os contrastes calculados dos botões normal/hover são 5,71:1 e 4,85:1; links sobre branco têm 5,51:1.
- Merriweather é carregada por `next/font/google`, servida localmente após o build. Login e página após entrar adotam composição de capa de álbum: arte à esquerda e conteúdo à direita, empilhados abaixo de 900 px. Cadastro e usuários preservam sua largura.
- Após rejeitar os primeiros adornos sobre letras da Merriweather, Bruno aprovou 52 desenhos geométricos próprios: maiúsculas e minúsculas construídas com hastes, barras e cabeças de notas. As pranchas e a amostra aprovadas estão em `docs/identidade/`; os dados reutilizáveis dos 52 glifos, espaço, pontuação e acentos da frase estão em `frontend/components/music-glyphs.json`.
- O título “Novas músicas, novas conexões.” usa os vetores aprovados, sem substituir a fonte dos formulários. O lettering é desenho SVG, não uma fonte TTF/WOFF instalada. Os contornos anteriores derivados da Merriweather foram removidos.
- A entrada revela as duas linhas continuamente em aproximadamente 4 segundos, sem efeito de digitação. Pautas ondulam em ciclo de 18 segundos; notas flutuam em ciclos de 12–20 segundos. O botão pausa/retoma as animações. A preferência de movimento reduzido mostra o título completo e o fundo parado. A interação com o formulário não reinicia a entrada.
- A home saúda o usuário autenticado, oferece o acesso real a `/usuarios` e informa que o feed está em preparação. Não inclui posts, contagens ou interações fictícias. As regras de autenticação e o banco permanecem inalterados nesta revisão visual.
- Codex criou os componentes, as animações e os desenhos vetoriais a partir das orientações e da referência visual fornecida por Bruno. As pranchas foram aprovadas antes da aplicação. Não foi usado um novo pacote de fontes ou animação.
- Validação visual e de comportamento em 1440, 1024, 768 e 360 px: ausência de cortes nos glifos/rolagem horizontal, pausa/retomada, movimento reduzido, nomes longos e ausência de reinício ao digitar. Build de produção e TypeScript passaram. As suítes de backend e navegador são registradas no PR com os resultados finais.

- Na preparação do PR #27, as atualizações recentes de `origin/main` foram incorporadas sem reescrever o histórico: preservados os testes adicionais `test_auth_casos.py`, a documentação de Cecília e o registro das propostas visuais em revisão. O conflito na tabela de andamento foi conciliado para mencionar os dois PRs.
- Verificação final após conciliar a `main`: **38 testes de backend passaram**, com 7 pendentes de outras features; **12 testes de navegador passaram** em desktop e celular. TypeScript e o build da versão final passaram; os testes de navegador usaram os servidores locais de prévia com SQLite separado dos dados de desenvolvimento.

## Posts e reviews — issues #3 e #9 — 25/11/2026

Inspirado no Letterboxd, o post da rede **é uma review de uma música do catálogo**: a música e a nota são obrigatórias e o texto é opcional. Uma review pode ser só a nota. A pessoa **escolhe** a música em um catálogo curado; não digita uma música nova.

- **Rotas de posts:** `POST /posts` (201), `GET /posts/{id}`, `PATCH /posts/{id}` e `DELETE /posts/{id}` (204). Todas exigem login.
- **Corpo de `POST /posts`:** `{"musica_id": int, "nota": 0 a 10, "texto"?}`. Esta é uma **evolução do contrato do núcleo**, que aceitava só `texto`; o `test_posts_crud` foi adaptado sem remover nenhuma verificação. Os testes ainda `@skip` de feed, curtidas, comentários e perfil usam o formato antigo e serão adaptados quando cada feature for implementada. Um `musica_id` fora do catálogo devolve `422`.
- **Resposta:** `id`, `texto`, `tem_texto`, `nota`, `musica` (todos os dados do catálogo), `autor` (usuário completo) e `created_at`.
- **Rotas do catálogo:** `GET /musicas?q=&offset=&limit=` (busca por termos de título e artista, sem diferença de caixa, paginada, limite de 1 a 100) e `GET /musicas/{id}`. Exigem login. Não há cadastro de música pela API.
- **Catálogo:** o backend importa `backend/data/musicas.json` (entrega de dados do Bruno, #32) a cada subida, de forma idempotente: a chave curada `chave_catalogo` identifica a gravação e o `id` do banco é atribuído uma vez e preservado. Um catálogo inválido impede a subida, em vez de gravar parte dele. A busca ignora caixa e acentos ("mare" encontra "Maré"); ela filtra em Python, porque o SQLite não faz essa comparação Unicode, e custa O(n) por consulta, o que é aceitável para um catálogo curado pequeno.
- **Identidade da música:** a chave curada é a identidade; título e artista iguais não unem gravações. Original, remix, ao vivo e remaster são músicas distintas e recebem reviews distintas.
- **Nota:** inteira de 0 a 10, obrigatória e editável. Escala provisória, aprovada "por enquanto"; meia nota ou estrelas podem vir depois. Nota fora do intervalo ou decimal devolve `422`.
- **Texto:** opcional, até 5000 caracteres, com espaços das pontas removidos. O limite é generoso, na linha do Letterboxd, porque o feed mostra só o indicador e o texto completo aparece apenas no detalhe; ele existe para proteger a API e o banco. O valor foi proposto por Daniel e a #3 pede que o time o confirme. Quando houver review derivada (#10), o DECISIONS.md já exige texto próprio nela.
- **Forma da review no feed (decisão de produto):** cartão compacto com a **capa**, o **nome da música** e a **nota**, mais um **indicador de que existe texto** (`tem_texto`); clicar na review abre o detalhe com o texto completo.
- **Capa (atualizado após revisão):** catálogo aceita `capa_url` ausente/null; importador normaliza para texto vazio no banco/API. Quando preenchida, o limite é 2048 caracteres. A normalização corrige a falha na segunda subida descrita em `docs/revisao-integracao-capas.md`.
- **Uma review por pessoa e versão.** Uma segunda review da mesma versão pelo mesmo autor devolve `409`, inclusive em envios simultâneos, porque a decisão é da restrição única do banco e não de uma consulta prévia; apagar a review libera uma nova. A oferta de edição ou reescuta fica para a #18.
- **A música não muda na edição.** `PATCH` altera só nota e texto, e um `musica_id` enviado ali é ignorado; trocar a música de uma review é decisão pendente da #9.
- **Ids absurdos:** um id maior que o inteiro do banco (`musica_id` no corpo, ou `post_id` e `musica_id` na rota) devolve `422`, e não um erro `500`. Foi apontado na revisão da Cecília.
- **Autoria vem da sessão.** Um `autor_id` enviado pelo cliente é ignorado. Editar ou excluir review de outra pessoa devolve `403` sem alterar o banco; review inexistente devolve `404`, verificado antes da permissão.
- **Preparação da árvore:** `origem_id` ainda não existe. Será uma coluna opcional do `Post` na #10, sem quebrar o contrato acima.
- **Exclusão:** por enquanto apaga a review. A política para descendentes de uma review excluída será definida junto com a #10.
- **Esquema do banco:** `create_all` cria tabelas ausentes, mas não altera colunas existentes. Não apagar `app.db` para esta correção: a normalização não muda nulabilidade e o SQLite não impõe o comprimento de VARCHAR. Use banco separado para testar; outros tipos de alteração de esquema exigem migração específica.
- Claude Code implementou o CRUD de reviews, a importação e as rotas do catálogo e seus testes (`test_posts_crud`, `test_posts.py` e `test_musicas.py`). Foi verificado com `make test` (75 passed, 6 skipped). O código ainda precisa ser revisado por outra pessoa do time.

## Follow e feed — issues #4 e #6 — 25/11/2026

**O que vem das issues e o que foi escolha de implementação.** Já estava nas issues #4 e #6 e no `test_nucleo`: o feed mostra somente quem a pessoa segue, sem as próprias reviews, da mais nova para a mais antiga, com `items` e `total`, e o follow é idempotente e atualiza os contadores. As issues pedem para *definir* e foram escolhas de quem implementou, abertas a revisão do time: o desempate pelo `id`, o `limit` de 1 a 100 com padrão 10, o `422` ao seguir a si mesmo, o `204` do follow, o campo `eu_sigo` no perfil (para o estado do botão, #35) e o formato dos itens do feed. A disposição visual do feed é da tela (#36, Cecília) e ainda não foi combinada.

- **Seguir:** `POST /usuarios/{username}/follow` e `DELETE` na mesma rota, ambos `204` e **idempotentes**: seguir de novo ou deixar de seguir quem não se segue não é erro nem altera contadores. A relação é única por par (chave composta no banco). Usuário inexistente devolve `404`; **seguir a si mesmo devolve `422`**. Seguir não cria nem pontua nada: não gera reputação, escuta nem nó.
- **Perfil:** `GET /usuarios/{username}` passou a devolver também `seguidores`, `seguindo` e `eu_sigo` (se quem olha já segue a pessoa), que é o estado do botão de seguir. Os contadores são calculados por contagem na hora, e nunca ficam negativos.
- **Feed:** `GET /feed?offset=0&limit=10` devolve as reviews **somente de quem a pessoa segue**, sem incluir as próprias, da mais nova para a mais antiga, com `items`, `total`, `offset` e `limit`. O `total` conta o conjunto inteiro filtrado. `limit` vai de 1 a 100 (padrão 10) e `offset` não pode ser negativo nem maior que o inteiro do banco (`422`).
- **Empates:** reviews criadas no mesmo instante são ordenadas pelo `id` (maior primeiro), para a ordem ser estável.
- **Formato dos itens:** os mesmos de `GET /posts/{id}`, com `musica`, `nota`, `tem_texto`, `autor` e `texto`. A interface decide o que mostrar: o cartão compacto usa capa, nome, nota e o indicador `tem_texto`, e abre a review para ler o texto. Autor e música são carregados em lote, sem uma consulta extra por review.
- **Limite da paginação por offset:** o banco precisa contar e pular as linhas anteriores, então páginas muito fundas custam mais (O(offset)). Além disso, se alguém publicar uma review entre duas páginas, um item pode aparecer repetido ou ser pulado. É aceitável para este tamanho de rede; uma paginação por cursor (a partir da data e do `id` do último item) resolveria os dois problemas, se for preciso.
- **Testes:** o `test_feed_cronologico_dos_seguidos` foi adaptado ao formato de review (cada autor avalia uma versão uma vez) sem remover nenhuma verificação, e `test_follow_unfollow_com_contadores` foi ativado. `make test`: 93 passed, 4 skipped (perfil, curtidas, comentários e seed).
- **Fora desta entrega:** curtidas e comentários (#6, próxima parte) e `GET /usuarios/{username}/posts` (#4), que o `test_perfil_editavel` ainda exige.
- Claude Code implementou follow, feed e os testes. O código ainda precisa ser revisado por outra pessoa do time.

## Curtidas — issue #6 — 25/11/2026

- **Rotas:** `POST /posts/{post_id}/curtir` e `DELETE` na mesma rota. Ambas exigem login, são **idempotentes** e devolvem `200` com `{"curtidas": n, "curtido_por_mim": bool}`, para a tela confirmar o estado real sem uma segunda consulta. Review inexistente devolve `404` e id fora do limite do banco devolve `422`.
- **Uma curtida por pessoa e review:** a chave composta do banco impede duplicatas, inclusive em envios simultâneos. Curtir de novo ou descurtir o que não está curtido não é erro, e a contagem nunca fica negativa.
- **Curtir a própria review é permitido.** Isso segue a regra de reputação já aprovada, que dá 1 ponto ao autor por curtida própria sem propagar para ancestrais. O ponto em si ainda não é calculado aqui.
- **Onde aparecem:** toda review (`GET /posts/{id}`, edição, criação e itens do feed) traz `curtidas` e `curtido_por_mim`. O segundo é de quem olha: a mesma review mostra `true` para quem curtiu e `false` para os demais. No feed, as curtidas de uma página inteira vêm em 2 consultas, e não em uma por review.
- **Curtir não cria review, escuta nem nó na árvore, e não altera a nota.** A reputação (#11) fica com o Bruno; a tabela `curtidas`, com uma linha por pessoa e review, é a base do evento de curtida único que a fórmula pede, e descurtir a remove.
- **Apagar uma review apaga as curtidas dela.** Sem isso as curtidas ficariam órfãs e poderiam grudar numa review nova que reaproveite o mesmo id.
- **Esquema do banco:** a tabela `curtidas` é nova. `create_all` cria tabelas ausentes sem apagar os dados existentes. Validar em banco separado; não apagar `app.db` como preparação do seed.
- **Testes:** o `test_curtidas_idempotentes` foi adaptado ao formato de review e ativado, sem remover verificações, e `test_curtidas.py` cobre o resto. `make test`: 106 passed, 3 skipped (perfil, comentários e seed).
- Claude Code implementou as curtidas e os testes. O código ainda precisa ser revisado por outra pessoa do time.

## Comentários — issue #6 — 26/11/2026

- **Rotas:** `POST /posts/{post_id}/comentarios` (`201`, devolve o comentário) e `GET /posts/{post_id}/comentarios`. Ambas exigem login. Review inexistente devolve `404` e id acima do inteiro do banco devolve `422`.
- **Comentário plano:** só texto de 1 a 1000 caracteres, com espaços das pontas removidos; vazio, só espaços ou acima do limite devolve `422` e nada é gravado. Não há respostas, e comentar **não gera reputação, nem review derivada, nem nó na árvore**, e não altera a nota. A autoria vem da sessão: um `autor_id` enviado pelo cliente é ignorado. O limite de 1000 é escolha de implementação, aberta a revisão.
- **Lista:** do mais antigo para o mais novo, com desempate pelo `id`, paginada (`offset` e `limit` de 1 a 100, padrão 50, `items`, `total`, `offset`, `limit`). O `total` conta todos os comentários da review.
- **Contagem nas reviews:** toda review (detalhe, criação, edição e itens do feed) traz `comentarios`, o número de comentários, para o cartão do feed. Curtidas e comentários de uma página inteira saem em 3 consultas, e não em uma por review.
- **Apagar a review apaga os comentários dela**, para não grudarem numa review nova que reaproveite o id.
- **Fora desta entrega:** editar e apagar comentário, que a #6 e a #38 não pedem. Podem virar uma issue própria se o time quiser.
- **Testes:** o `test_comentarios_planos_cronologicos` foi adaptado ao formato de review e ativado, sem remover verificações, e `test_comentarios.py` cobre o resto. `make test`: 280 passed, 2 skipped (perfil e seed).
- **Esquema do banco:** a tabela `comentarios` é nova. `create_all` cria tabelas ausentes sem apagar os dados existentes. Validar em banco separado; não apagar `app.db` como preparação do seed.
- Claude Code implementou os comentários e os testes. O código ainda precisa ser revisado por outra pessoa do time.

## Reviews no perfil — issue #4 — 26/11/2026

- **Rota:** `GET /usuarios/{username}/posts?offset=0&limit=10` devolve as reviews de uma pessoa, da mais nova para a mais antiga, com desempate pelo `id`, e `items`, `total`, `offset` e `limit`. Exige login. Pessoa sem reviews devolve lista vazia; usuário inexistente devolve `404`.
- **Visibilidade:** qualquer pessoa logada vê as reviews de outra no perfil, sem precisar segui-la. Isso difere do feed, que mostra só quem se segue. As reviews são públicas dentro da rede; as bibliotecas privadas seguem outra regra (#12) e não passam por aqui.
- **Formato:** os itens são os mesmos do feed e de `GET /posts/{id}`, com música, nota, `tem_texto`, `curtidas`, `curtido_por_mim` e `comentarios`, vistos por quem olha.
- **Paginação:** `limit` de 1 a 100 (padrão 10) e `offset` limitado ao inteiro do banco (`422` fora disso), como no feed, com a mesma ressalva sobre o custo e a repetição de itens da paginação por offset.
- **Sem duplicação:** o feed e o perfil passam a usar a mesma consulta (`listar_reviews`), que também servirá às reviews de uma música (#65).
- **Testes:** o `test_perfil_editavel` foi adaptado ao formato de review e ativado, sem remover verificações, e `test_reviews_do_usuario.py` cobre o resto.
- Claude Code implementou a rota e os testes. O código ainda precisa ser revisado por outra pessoa do time.

## Músicas mais avaliadas e reviews por música — issue #65 — 26/11/2026

Segue o contrato de `docs/feed-e-descoberta.md`.

- **`GET /musicas/populares?offset=0&limit=10`:** as músicas do catálogo com o número de reviews (`quantidade_reviews`) além dos dados musicais de `GET /musicas`. Exige login e devolve `items`, `total`, `offset` e `limit`. A rota fixa é registrada **antes** de `/musicas/{id}`, para "populares" não ser lido como um id.
- **O que conta:** a quantidade de reviews ativas de cada gravação, em todo o período. É a contagem de reviews na rede: **não** é popularidade em serviço de streaming nem contagem de escutas. Curtir, comentar, editar e seguir não aumentam o número, e apagar uma review o reduz. **Só entram músicas com pelo menos uma review**, e uma música sem reviews sai da vitrine.
- **Ordem:** mais reviews primeiro, e o `id` da música desempata, do menor para o maior. Original, remix, ao vivo e remaster são gravações distintas, contadas separadamente, e o mesmo título de outro artista também.
- **`GET /musicas/{id}/reviews?offset=0&limit=10`:** as reviews de uma gravação, no formato do feed (música, nota, `tem_texto`, `curtidas`, `curtido_por_mim`, `comentarios`), da mais nova para a mais antiga e com desempate pelo `id`. Música inexistente devolve `404`, e música sem reviews devolve lista vazia. Usa a mesma consulta do feed e do perfil.
- **Busca:** `GET /musicas?q=` já existia e é reaproveitada, por título e artista, sem diferença de caixa nem de acento.
- **Limites e erros:** `limit` de 1 a 100 e `offset` limitado ao inteiro do banco (`422` fora disso), sem sessão `401`. Como o ranking é uma contagem feita na hora, o custo cresce com o número de reviews (O(n) por consulta), o que é aceitável para este tamanho de rede, e a paginação por offset pode mudar com novas interações, sem promessa de snapshot.
- **Testes:** `test_populares.py` cobre empates, exclusão, edição, curtidas e comentários, versões distintas, zero reviews, paginação, autorização, parâmetros inválidos e a ordem das rotas. `make test` passou.
- Claude Code implementou as rotas e os testes. O código ainda precisa ser revisado por outra pessoa do time.

## Integridade ao apagar uma review — revisão do PR #74 — 26/11/2026

- **Problema apontado por Bruno:** curtir e comentar conferiam se a review existia e só depois gravavam. Se outra requisição a apagasse no intervalo, a interação era gravada mesmo assim, porque o SQLite não confere chave estrangeira por padrão, e uma review nova que reaproveitasse o id apagado herdava a curtida ou o comentário antigo. Foi reproduzido com duas sessões.
- **Correção em três partes:** (1) as conexões SQLite passam a ligar `PRAGMA foreign_keys=ON`, então gravar curtida ou comentário numa review que já não existe é recusado pelo banco; (2) a tabela `posts` usa `AUTOINCREMENT`, então o id de uma review apagada **nunca é reaproveitado**, o que cobre também o caso em que a review é apagada e recriada antes da gravação; (3) quando o banco recusa a gravação, o serviço confere de novo e devolve `404` se a review sumiu, e mantém o comportamento idempotente quando a curtida já existia.
- **Testes de regressão:** `test_corrida_exclusao.py` simula a intercalação (apagar, e apagar e recriar, no meio da operação) para curtidas e comentários, e confere que o id não é reaproveitado. Sem a correção, os 5 testes falham. `test_feed_nao_faz_uma_consulta_por_review` garante que o número de consultas do feed não cresce com o tamanho da página.
- **Esquema do banco:** `posts` mudou (`AUTOINCREMENT`). Tabelas `posts` já existentes não recebem essa proteção por `create_all`; precisam de migração explícita, fora desta entrega de dados. Não apagar `app.db`. O preflight do seed rejeita esquema sem AUTOINCREMENT; a reconstrução da demo é separada e depende da integração completa.
- **Limite:** a chave estrangeira vale para o SQLite. Em outro banco, a garantia seria a das restrições dele.
- Claude Code corrigiu e escreveu os testes. O código ainda precisa ser revisado por outra pessoa do time.


## Issue #13 — seed e cenários aprovados — 25/11/2026

- Prioridade: cenários reproduzíveis de árvores e Descobrir, com integração conforme contratos do backend. Documentação não encerra a issue.
- Catálogo de demonstração: 20 gravações reais da playlist de Bruno, com Apesar de Você substituindo Sozinho. IDs Spotify são referências externas; sem download de áudio/OAuth. Catálogo fictício anterior preservado como fixture técnica.
- 25 personagens fornecidos por Bruno; Bruno Nunes, Cecília Candeia e Daniel Dantas protagonizam a corrente. Reviews e ações são fictícias. Massa inicial: 50 reviews, 20 follows e 30 likes; semente fixa 13. Clareou possui corrente, ramo e raiz independente; Ryan Rodrigues inicia sem sinais.
- Banco exclusivo de demonstração; preservar ações dos ensaios e registrar carga aplicada. Reexecução não restaura registros removidos. Reset separado e explícito; sem carga parcial: requisitos ausentes interrompem antes de gravar.
- Implementados definição/validação independente e orquestração com contrato de adaptador. Persistência real, reset funcional e validação integrada continuam pendentes dos modelos do backend; não são considerados entregues.
- Detalhes, nomes, faixas, contratos, roteiro e limites: [docs/demo-issue-13.md](docs/demo-issue-13.md). Bruno prepara dados; Daniel alinha persistência; algoritmos continuam nas #41/#43/#55.


## Issue #13 — continuação do contrato e reset — 25/11/2026

- Bruno confirmou: Daniel entrega os modelos/serviços; não criar persistência paralela na #13. Primeiro marco é carga e APIs; as demais integrações seguem progressivamente.
- Reset com backup anterior, reconstrução/validação em temporário e substituição atômica; aplicação parada e confirmação explícita obrigatórias. Cópias locais não são apagadas automaticamente.
- Implementado mecanismo independente dos modelos e ligação automática à fábrica proposta `app.services.demo_seed.criar_adaptador()`. O adaptador requer verificar/gravar/preparar_banco/validar. A interface concreta precisa ser alinhada aos modelos entregues por Daniel.
- Os modelos necessários continuam ausentes na base consultada. Adaptador real, carga pela API e validação do reset com a rede real permanecem pendentes; testes de infraestrutura não comprovam essas entregas.

## Perfil — conciliação com a identidade aprovada (25/11/2026)

- As telas de perfil passaram a usar o visual e a sessão central do PR #27. Os componentes do tema escuro (`feat/telas-auth`) foram removidos.
- `eu` e `stats` são usernames reservados, porque colidem com rotas fixas de `/usuarios`.
- Cada perfil recria o componente e descarta respostas de um perfil já abandonado.
- Claude Code fez a conciliação e as correções apontadas na revisão de Bruno, verificadas com `pytest`, TypeScript, build e testes de navegador. A revisão por outra pessoa continua pendente.

## Perfil: seguir e reviews — issue #34 (25/11/2026)

- O perfil ganhou contadores, botão de seguir e a lista paginada de reviews. Feed e perfil compartilham a paginação (`usePaginacao` e `ListaDeReviews`).
- Contrato **proposto**: `GET /usuarios/{username}` com `seguidores`, `seguindo` e `eu_sigo`; `POST` e `DELETE /usuarios/{username}/follow`; `GET /usuarios/{username}/posts?offset=&limit=`. Os campos e as rotas de follow seguem a branch `feat/back-curtidas` de Daniel, ainda fora da `main`; a rota de reviews por usuário ainda não existe.
- Sem esses campos, o perfil não mostra botão nem contadores. Com `NEXT_PUBLIC_PERFIL_SIMULADO=true`, usa exemplos e avisa isso.
- Claude Code implementou a tela e os testes de navegador. A revisão por outra pessoa continua pendente.

## Página inicial pública (25/11/2026)

- `/` apresenta a rede a visitantes e mostra o início a quem entrou. As demais páginas continuam exigindo sessão, e uma sessão inválida continua levando a `/login`.
- A apresentação usa a arte da identidade aprovada; o fundo de ondas neon foi descartado. Claude Code fez a adaptação.

## Issue #9 — recorte exclusivo de dados — 25/11/2026

- Bruno confirmou limitar esta entrega à sua área: catálogo, gêneros, tags e validação de identidades/versões. Não implementar posts (#3), follow (#5), feed (#6), republicação (#18) ou API/interface dentro desta entrega.
- Catálogo manual com as seis faixas fictícias anteriores, sem expansão. Original, remix, ao vivo e remaster são itens distintos; versões não originais exigem descrição. Chave curada única e estável; correções de metadados não mudam a chave, nem autorizam unir gravações por título/artista.
- Entregues carregador e validador independentes da aplicação/banco, com limpeza de metadados em memória, diagnóstico por entrada/campo e rejeição do conjunto inteiro quando inválido. IDs internos serão atribuídos pelo backend; integrações externas exigem confirmação de equivalência.
- Review única, edição e republicação ficam documentadas como requisitos futuros. Daniel integra persistência, vínculo e validações; Cecília integra seleção/apresentação. Troca da música de uma review continua pendente. A issue #9 não é concluída somente com estes dados.
- O PR exclusivo de dados substitui o #28, preservando sua branch com API/seletor como referência. Os PRs #29–#31 permanecem fechados, sem incorporar suas implementações. O trabalho parte da main atual; a alteração anterior de responsabilidades já consta nessa base e foi preservada.
- Validação: 37 testes de dados passaram sem carregar a infraestrutura de API/banco, incluindo bloqueio explícito de imports da aplicação e das bibliotecas de banco. O validador aprovou as seis entradas. Não foram alterados modelos persistidos, rotas, frontend ou o seed de usuários.

## Catálogo — ajuste da revisão do PR #32 — 25/11/2026

- Bruno autorizou adicionar `capa_url` opcional: ausente ou `null` representa música sem capa; valor preenchido deve ser URL absoluta HTTP/HTTPS de até 2048 caracteres. O carregador devolve texto JSON compatível e não consulta/baixa a imagem.
- As seis faixas fictícias permanecem sem imagens inventadas; `capa_url: null` explícito. A interface pode apresentar fallback, sob responsabilidade do front. Persistência/exposição pela API continuam com o backend.
- Conflito em DECISIONS.md resolvido preservando o registro de dados e os registros recentes da main sobre perfil e página inicial. Sem merge do PR nem reescrita do histórico.


## Revisão da integração — atualização da base do #59 — 25/11/2026

- Incorporada a base atualizada do #32 com `capa_url` opcional e a main já conciliada. Resolvido conflito em DECISIONS.md preservando decisões de seed, catálogo, capas, perfil e página inicial. Sem incorporar a branch de backend do #60.
- A revisão combinada encontrou falha de `None` versus `NOT NULL` na reimportação do catálogo do #60, capaz de impedir a segunda inicialização. Correção implementada no #60: normalizar ausência/null para texto vazio no importador; modelo/schema alinhados a 2048 caracteres.
- Evidências e causa documentadas no #60 em `docs/revisao-integracao-capas.md`; testes de reinício, reimportação, URL longa e remoção de capa adicionados lá. Nenhum aviso, comentário ou menção ao time foi enviado nesta correção.
- A atualização não conclui o adaptador do seed: origens/follows/likes e validação integrada continuam dependências da #13.

## Estrutura e percursos de árvores — issue #41 — 25/11/2026

- Entrega exclusivamente de dados em `app/core/arvores.py`, sem banco/FastAPI.
  Classe instanciável e singleton para futura integração da #10; não altera
  endpoints, modelos, startup, seed ou interface. Troca de origem fica na #49.
- Floresta indexada por ID, filhos por pai e raízes por música. Nó imutável:
  IDs de review/música/autor, origem opcional e marca de apagada, sem conteúdo.
  IDs int/string sem coerção; mesma música significa mesma identidade interna,
  não igualdade de título. Várias raízes por música são válidas.
- Reconstrução aceita registros fora de ordem, exige referências completas e
  rejeita integralmente duplicata, pai ausente, outra música e ciclo, preservando
  o estado anterior. Referência apagada existente é válida e conserva autoria.
- Inserção incremental exige ID novo e pai ativo da mesma música. Exclusão
  estrutural idempotente apenas marca apagada; descendentes, distância e raiz
  permanecem. Unicidade de review ativa, texto, permissões e transações são do
  backend. Curtidas, comentários e reescutas não alimentam a floresta.
- BFS e DFS pré-ordem iterativos; ancestrais do pai à raiz; nó inicial excluído.
  Referências apagadas aparecem como nós sem conteúdo e contam como nível.
  Irmãos/raízes seguem inserção; backend deve fornecer carga ordenada e estável.
- Percursos paginados: offset não negativo, limit padrão 50/máximo 200,
  profundidade opcional sem corte padrão; zero retorna vazio. Profundidade
  aplicada antes da paginação. Retorno imutável com itens, distância e tem_mais,
  sem total. Mudanças entre consultas podem alterar páginas.
- Custos reais: reconstrução O(n) esperado com detecção de ciclos linear,
  memória O(n); inserção/consulta/pai/exclusão O(1) esperado/amortizado;
  raiz O(h); listar raízes O(r). Percursos custam o trabalho examinado,
  incluindo offset e um item extra. Descendentes também pagam pelas ligações
  enfileiradas, com fronteira O(n) no pior caso mesmo com página pequena.
  Contrato e exemplos completos em `backend/app/core/README.md`.
- Testes puros em `backend/tests_dados/test_arvores.py`, incluindo corrente
  profunda, ramificação, raízes independentes, apagadas, carga inválida atômica,
  paginação e cenário da #13. Isso não comprova integração com API/banco.

### Revisão ampliada da #41 — 25/11/2026

- Corrigida a descoberta de testes: o pytest padrão (e `make test`) agora inclui
  `tests_dados` além de `tests`. Antes, uma execução padrão podia passar sem
  validar árvores, catálogo e seed. O isolamento por diretório foi preservado.
- Ampliada a validação com comparação dos percursos/páginas a um modelo
  independente em 12 florestas determinísticas, árvore larga com 501 filhos,
  tipos inválidos em todos os identificadores e falhas de entrada sem mutação.
  A revisão não encontrou defeito funcional nos algoritmos de árvore.

## Integração de capas — erro encontrado e corrigido — 25/11/2026

- Revisão adicional de Codex, autorizada por Bruno, encontrou incompatibilidade entre `None` do catálogo e coluna `NOT NULL` do backend. Reproduzida falha na reimportação e segunda inicialização com o mesmo banco.
- Corrigida no importador: copiar registro e converter capa ausente/null para texto vazio antes de INSERT e UPDATE, preservando o contrato externo e os IDs. Limite do modelo e schema alinhado ao catálogo: 2048 caracteres.
- Testes de regressão cobrem reimportação, reinício real via lifespan, URLs longas, remoção de capa e credenciais preservadas. Detalhes e evidências em [docs/revisao-integracao-capas.md](docs/revisao-integracao-capas.md).
- Conciliação da base do #32 preserva decisões de posts, dados, perfil, página inicial e capas, sem duplicar a seção de dados. Sem avisos/comentários/menções ao time; revisão humana e merge continuam pendentes.

## Feed e descoberta — decisão de 25/11/2026

Bruno confirmou feed cronológico dos seguidos, pesquisa e ranking de músicas por quantidade de reviews, e republicação como criação de review derivada. Aprovou o rascunho gerado por IA como referência visual e autorizou sua publicação e organização no GitHub. Descobrir personalizado permanece separado.

Padrões adotados neste plano: ranking de reviews públicas ativas em todo o período, desempate por ID, layout de três colunas a partir de 1024 px e navegação compacta abaixo disso. Não são afirmações extraídas dos áudios, que não foram transcritos. Detalhes, contratos, critérios e uso de IA: [feed e descoberta](docs/feed-e-descoberta.md). Backend de populares: #65; frontend: #66; demais tarefas preservam issues e responsáveis existentes. Imagem e documentação não significam funcionalidades prontas.

## Revisão integral e integração autorizada dos PRs #32/#60/#59 — 25/11/2026

- Bruno autorizou revisar integralmente e mesclar os três PRs, corrigindo falhas antes da integração. #32 e #60 entram primeiro; #59 passa a ter main como base para não ser mesclado apenas numa branch de funcionalidade.
- Revisão do #59 incluiu massa, contrato, rollback/preservação, reset/backup, catálogo, estrutura de árvores e testes. Corrigidos fechamento explícito das conexões SQLite do backup e ausência de nota nos cenários; reforçada rejeição de identidades duplicadas. Evidências em docs/demo-issue-13.md.
- Integração não conclui a #13: seed real depende de adaptador e persistência dos requisitos restantes. Sem comentários, menções ou mensagens ao time nesta etapa.

## Telas de review — issue #3 (25/11/2026)

- Front de criar, ver, editar e excluir review sobre a API de `feat/posts`: `/posts/novo` e `/posts/[id]`.
- Música sem capa, ou com imagem indisponível, mostra um substituto. A exclusão pede confirmação.
- O feed e a lista de reviews do perfil dependem de rotas que ainda não existem.
- Claude Code implementou as telas e os testes de navegador. A revisão por outra pessoa continua pendente.

## Seleção de música no catálogo — issue #33 (25/11/2026)

- `/posts/novo` deixou de aceitar título, artista, versão e capa digitados: a pessoa busca no catálogo (`GET /musicas`) e a review envia `musica_id`. Substitui o formulário descrito em "Telas de review".
- A busca mostra até 20 resultados e pede para refinar quando há mais. A música escolhida aparece com artista e versão antes de publicar.
- A troca de música de uma review existente continua não oferecida.
- Claude Code fez a adaptação e os testes. A revisão por outra pessoa continua pendente.


## Issue #13 — adaptador sobre #74 corrigido — 26/11/2026

- #74 no commit a68afe2 passou com 312 testes aprovados/1 skip e foi integrado à main. Preservadas as correções de foreign keys por conexão, AUTOINCREMENT e exclusão concorrente.
- Implementada fábrica de adaptador com mapeamento para User/Musica/Post/Follow/Curtida, hash oficial, schemas, preflight de esquema/constraints/colisões e validação semântica antes do commit e da marca. Serviços que fazem commit interno não são chamados na carga.
- Catálogo configurável por CATALOGO_MUSICAL_PATH: demo e startup devem usar as mesmas 20 gravações; padrão mantém as seis fictícias. Cenário issue13-v2 tem contagens controladas para ranking: 5, 4, 4, sete vezes 3, oito vezes 2 e duas sem reviews.
- Persistência de origens ainda ausente: carga completa interrompe antes de gravar, sem transformar derivadas em raízes. Testes usam fixtures explicitamente sem origens, não acessíveis por flag do produto; não comprovam carga completa nem concluem #13.
- Ajustado teste do núcleo para tabela real curtidas; skip mantido e explica dependência da #10. Atualizados documentos de esquema para não recomendar apagar app.db. Detalhes em docs/demo-issue-13.md.

## Tela de feed — issue #36 (25/11/2026)

- `/feed` consome `GET /feed?offset=&limit=` no formato de página (`items`, `total`) com reviews no formato de `PostOut`. A rota ainda não existe no backend.
- Cartão compacto, como decidido para o feed: capa, música, nota e indicador de análise; o texto abre no detalhe.
- Com `NEXT_PUBLIC_FEED_SIMULADO=true`, a tela usa dados fictícios e avisa isso. A variável não deve ser ligada na demonstração como se fosse o feed real.
- Curtidas e comentários, também da #36, não foram feitos.
- Claude Code implementou a tela e os testes de navegador. A revisão por outra pessoa continua pendente.

## Botão de curtir — issue #36 (25/11/2026)

- Feed e detalhe mostram contagem e estado, com `POST` e `DELETE /posts/{id}/curtir` (branch `feat/back-curtidas`, ainda fora da `main`).
- A tela usa a contagem devolvida pelo servidor; em falha nada muda. Curtir não é tratado como descoberta.
- Sem os campos `curtidas` e `curtido_por_mim`, o botão não aparece. Reviews de exemplo não têm botão.
- Claude Code implementou o botão e os testes. A revisão por outra pessoa continua pendente.


## Tela da árvore de recomendações — issue #42 (25/11/2026)

- `/posts/[id]/arvore` mostra a corrente como lista hierárquica, com a review atual destacada e o caminho "Descoberta via …".
- Contrato **proposto** para o backend: `GET /posts/{id}/arvore` devolve `{musica, raiz}`, e cada nó tem `id`, `apagada`, `autor`, `nota` e `filhos`. Falta combinar com Daniel e Bruno.
- Review apagada mantém os ramos e não mostra autoria nem conteúdo. O backend também não deve enviá-los.
- Com `NEXT_PUBLIC_ARVORE_SIMULADA=true`, a tela usa uma corrente fictícia e avisa isso.
- Publicar review derivada, corrigir origem e exibir reputação, também da #42, não foram feitos.
- Claude Code implementou a tela e os testes de navegador. A revisão por outra pessoa continua pendente.

## Novo layout do feed — issues #36 e #66 (26/11/2026)

- `/feed` segue a referência aprovada em `docs/feed-e-descoberta.md`: perfil à esquerda, reviews no centro e pesquisa, mais avaliadas e Descobrir à direita a partir de 1024 px; abaixo disso, atalhos compactos.
- Cabeçalho com Feed, Descobrir e Pessoas, avatar e "Sair". Entraram `/musicas`, `/musicas/[id]` e `/descobrir`.
- Compartilhar usa o recurso do aparelho ou copia o link.
- Aparecem desativados, como "em breve": comentários, review derivada e biblioteca. O selo de origem só aparece se o servidor enviar `origem`.
- `GET /musicas/populares` e `GET /musicas/{id}/reviews` (#65) ainda não existem; a tela explica a indisponibilidade. Com `NEXT_PUBLIC_FEED_SIMULADO=true`, feed e vitrine usam exemplos identificados.
- A branch reúne o trabalho dos PRs #58, #61, #62 e #63.
- Claude Code implementou as telas e os testes. O time decidiu em 26/11 não fazer revisão cruzada dos PRs.

## Reviews derivadas e árvore de recomendações — issue #10 — 26/11/2026

Primeira parte da #10 (criação, leitura e exclusão). **Correção de origem (#19) e reputação (#11) não estão nesta entrega.**

- **Criar uma derivada:** `POST /posts` aceita `origem_id` (opcional). A review passa a ser **derivada** da outra, que precisa existir, **estar ativa** e ser **da mesma música** (`422` se não). A derivada **exige texto próprio** (`422` se vier vazio ou só com espaços) e continua valendo **uma review ativa por pessoa e música** (`409`): quem já avaliou a música não deriva dela, e ninguém deriva da própria review. Uma raiz continua podendo ser só a nota. Não há ciclo possível na criação, porque a origem sempre já existe.
- **A origem não muda na edição:** `PATCH` ignora `origem_id`, e uma derivada não pode ficar sem texto ao ser editada. Trocar a origem é a #19 (não feita).
- **Resposta:** toda review traz `origem_id` (se for derivada) e `origem` (`id` e `autor`), este só se a review de origem ainda existe. Vale para detalhe, criação, edição, feed, perfil e reviews por música.
- **Ler a árvore:** `GET /posts/{id}/arvore` devolve `{musica, raiz, truncada}`; cada nó tem `id`, `apagada`, `autor` (`username` e `name`), `nota` e `filhos`, em ordem de publicação. Funciona a partir de **qualquer** review da árvore e dá a mesma árvore. Segue o contrato proposto na tela da árvore (#42). Exige login; review desconhecida devolve `404`.
- **Limite de leitura:** no máximo 200 reviews além da raiz; passou disso, `truncada` vem verdadeiro.
- **Excluir:** o conteúdo some (nota, texto, curtidas e comentários), mas o **lugar na árvore fica**, numa tabela `reviews_apagadas` com o mesmo `id` (que nunca é reaproveitado, pelo `AUTOINCREMENT`). As derivadas **continuam ligadas** a esse lugar, e a pessoa mantém o crédito de origem. Na árvore, o nó vem com `apagada: true`, sem `autor` nem `nota`, e os descendentes mantêm os dados deles. A review apagada responde `404` em tudo o mais (detalhe, curtir, comentar). Uma **nova review da mesma pessoa e música é uma raiz nova**, sem ligação com a antiga. A referência `origem_id` não tem chave estrangeira de propósito, para continuar válida depois da exclusão.
- **Estrutura de dados:** a árvore usa a `FlorestaReviews` de `core/arvores.py` (Bruno, #41), por uma instância única em `core/floresta.py`. Ela é **reconstruída no startup** a partir do banco (reviews e reviews apagadas) e só é atualizada **depois da gravação confirmada**; se sair de sincronia, o serviço a reconstrói. Complexidades reais: inserir e marcar como apagada são O(1); subir até a raiz é O(profundidade); descer pela árvore devolve no máximo 200 reviews além da raiz, mas o percurso em largura pode enfileirar **todos** os filhos de um nó largo, então o tempo e a memória são O(n) no pior caso (o limite restringe a saída, e não o trabalho; correção apontada por Bruno na revisão). Percorrer uma corrente inteira **não** é O(1). Na reconstrução, as reviews existentes e as apagadas entram ordenadas pelo mesmo id estável, para a ordem dos ramos não mudar depois de reiniciar.
- **Banco antigo (correção do que estava escrito antes):** a coluna nova `posts.origem_id` é acrescentada automaticamente na subida a quem já tem `app.db` (`ALTER TABLE`, repetir é seguro), e a tabela `reviews_apagadas` é criada pelo `create_all`. **Mas isso não basta**: um `posts` criado antes do `AUTOINCREMENT` continua sem ele, porque o SQLite não permite acrescentá-lo a uma tabela existente. Nesse banco o id da última review apagada é reaproveitado e colide com o lugar dela em `reviews_apagadas`. O defeito foi achado por Cecília ao testar o #78 (publicar de novo e apagar davam `500`, e o servidor não reiniciava). O que o sistema faz agora: publicar e apagar **não dão erro** (o registro da review apagada é substituído), o servidor **reinicia** e **avisa no log** para recriar o banco, e a árvore dessas reviews pode ficar inconsistente (`503`). **Quem tem um `app.db` de antes do `AUTOINCREMENT` deve recriá-lo: `rm backend/app.db && make seed`.** Reconstruir a tabela na subida foi descartado por mexer nos dados de todos.
- **Dados gravados por fora da API:** um seed, por exemplo, escreve direto no banco com o backend ligado, e a floresta em memória fica para trás. Apagar uma review ou ler a árvore dessas reviews **refaz a floresta a partir do banco** em vez de falhar, e uma review que não existe continua devolvendo `404`. A reconstrução custa O(reviews) e só acontece nessa situação. Foi encontrado ao juntar este PR com o adaptador do seed (#75), cujo teste de integração apagava uma review carregada por fora.
- **Concorrência:** o backend atende as requisições em várias threads e a estrutura de `core/arvores.py` não tem trava, então toda leitura e escrita nela passa por uma trava única (`services/arvores.TRAVA`). A floresta vive na memória de **um processo**: com vários processos do backend, cada um teria a sua cópia (a maioria dos desencontros se corrige sozinha, porque a árvore se refaz ao não conhecer uma review, mas um apagar feito em outro processo pode aparecer como nó desatualizado até reiniciar). No uso normal, com um processo, isso não ocorre.
- **Dado inconsistente não derruba o sistema:** se o banco tiver uma inconsistência na árvore (por exemplo, uma origem que sumiu por edição manual), a reconstrução **não impede o backend de subir** nem uma review gravada de responder: vira um aviso no log, e feed, reviews, curtidas e comentários seguem funcionando. Só a leitura da árvore dessas reviews devolve `503` ("árvore indisponível"), e não um erro `500`. Review que nunca existiu continua devolvendo `404`.
- **Testes:** `test_arvore.py` cobre corrente de três níveis, dois ramos, raiz isolada e raízes distintas da mesma música, regras da derivada, exclusão (meio, raiz e folha), nova raiz depois de apagar, leitura limitada, reinício (a árvore reconstruída é igual), permissões e a atualização de banco antigo.
- **Fora desta entrega:** correção de origem (#19), reputação (#11) e recálculo (#20), e a tela de escrever review derivada, da Cecília (#33 e #42).
- Claude Code implementou a derivada, a árvore e os testes. O código ainda precisa ser revisado por outra pessoa do time.

## Motor puro de reputação — #43 (26/11/2026)

- Separar `calcular_creditos` do acumulador `Reputacao`, reutilizando somente
  consultas públicas da floresta da #41, sem banco, FastAPI ou nova dependência.
- Eventos imutáveis identificados por tipo + usuário/review na curtida e
  tipo + review na derivada, compatíveis com a chave composta do PR #74.
- Manter contribuição por evento e total por autor. Fórmula 4/2/1, auto-curtida
  de 1 só ao autor e maior parcela por autor/evento; nunca redistribuir sobras.
- Aplicação/remoção idempotentes; reversão usa créditos originalmente concedidos.
  Reconstrução completa deduplica e substitui estado atomicamente, inclusive
  preservando estado anterior em falha da fonte de entrada.
- Apagados preservam posição, autoria e eventos históricos. A #10 ainda deve
  adaptar a exclusão física do PR #74, persistir eventos recuperáveis e sincronizar
  somente writes confirmados. Este motor não comprova integração de API/banco.
- A #51 fica com seleção e atualização retroativa dos eventos afetados por troca
  de origem. A #43 fornece cálculo, contribuições e reconstrução como referência.
- Custo esperado O(1) por evento, O(E) na reconstrução e O(A + U) de memória,
  além da floresta; reconstrução mantém estado temporário até sucesso.
- Código e testes elaborados com Codex. Na publicação original, a revisão
  independente estava pendente; atualização de revisão registrada abaixo.
- Validação local: suíte completa com 337 aprovados e 1 ignorado; após adicionar
  dois cenários de contrato, suíte específica com 27 aprovados e suíte de dados
  com 185 aprovados. Aviso preexistente de depreciação do TestClient/HTTPX.

## Conciliação e estado atual — PRs #75/#76 — 26/11/2026

- Main incorporada à branch da #43 por merge, sem rebase ou force push.
  O único conflito era a adição de seções ao final deste documento; preservados
  integralmente os registros da main e a seção de reputação, sem mudar contratos.
- #75 integrado: adaptador real disponível, mas carga completa da #13 ainda
  bloqueada pela persistência de origens da #10; fixtures de raízes não comprovam
  árvore persistida nem encerram a demonstração.
- Feed, curtidas e populares já possuem rotas entregues pelo #74. Descrições
  anteriores de indisponibilidade nas seções de telas são registros históricos.
- #43 entrega o motor puro. Persistência/API e preservação dos eventos na exclusão
  permanecem na #10; recálculo retroativo de subárvore permanece na #51.
- Bruno informou nesta conversa que revisou o #76 e considerou a entrega correta.
  Esse relato não equivale a uma aprovação registrada pelo GitHub nem transforma
  a revisão automatizada local em revisão independente.
- Preservadas as correções da #75: sem apagar app.db para preparar o seed,
  catálogo compartilhado por configuração e migração explícita quando necessária.
- Validação após conciliação: 27 testes específicos de reputação, 189 testes de
  dados e suíte completa com 352 aprovados/1 ignorado. Único aviso: depreciação
  preexistente do TestClient/HTTPX. git diff --check aprovado; nenhuma mudança
  de código necessária na resolução. Merge na main não realizado nesta etapa.


## Revisão do PR #78 para integração da #13 — 26/11/2026

- Base já conciliada pelo autor com a main; preservada sem rebase.
- Reconstrução ordena referências ativas e apagadas conjuntamente por ID estável,
  preservando a ordem dos ramos após exclusão e reinício. Teste de regressão incluído.
- Limite de 200 descendentes restringe saída; BFS ainda pode enfileirar muitos
  filhos, com O(n) de trabalho/memória no pior caso, conforme #41.
- Exclusão ainda remove curtidas operacionais; persistência dos eventos históricos
  de reputação permanece pendente na #10. Referência apagada não substitui esse registro.


## #13 — carga completa sobre origens do #78 — 26/11/2026

- Adaptador usa os modelos oficiais com origem, valida floresta antes de gravar,
  insere pais antes dos filhos e valida vínculos exatos antes do commit/marca.
- Versão issue13-v2 e massa preservadas; sem transformação de derivadas em raízes.
  Referências apagadas existentes sem marca provocam colisão e são preservadas.
- Teste integrado do núcleo ativado. Testes reais verificam árvore/API/reinício,
  repetição, rollback de origem divergente, reset com backup e pontos via core #43.
- Pontos da carga inicial são comparados a oráculo independente, sem integração
  persistente da reputação. Exclusão de curtidas históricas permanece pendência #10.
- #13 continua aberta para critérios restantes, incluindo Descobrir. Implementação
  em branch própria baseada no #78; merge desse backend exige decisão de Bruno.
- Validação final desta combinação: 378 testes aprovados, sem skips; 189 testes
  de dados aprovados. Único aviso: depreciação preexistente TestClient/HTTPX.
  make check em SQLite separado, make seed-validar e git diff --check aprovados.
- Instalação limpa via uv sync --frozen e CLI real em cópia descartável:
  catálogo de 20 músicas válido, primeira carga completa, repetição preservada,
  inicialização da API e reset com backup concluídos. Nenhum banco pessoal alterado.
## Comentários e review derivada no front — issues #36, #33 e #42 (26/11/2026)

- O detalhe da review mostra os comentários em ordem cronológica, com paginação; em falha, o texto digitado é mantido. O cartão do feed mostra a contagem.
- "Escrever review a partir desta" abre o formulário com música e origem preenchidas e exige análise própria. Review repetida mostra o erro e o acesso às próprias reviews, sem trocar a origem.
- A ação só é habilitada quando a review traz `origem_id` (branch `feat/back-arvore`): um servidor sem esse campo ignoraria a origem.
- A correção de origem e a reputação continuam sem tela.
- Claude Code implementou as telas e os testes.

## Barra de navegação única — 26/11/2026

- A barra passou para `components/Navbar.tsx`, com a mesma largura e altura em todas as páginas e o item da seção atual destacado. Visitantes veem a marca e o acesso a entrar ou criar conta.
- Claude Code fez a mudança e o teste. Por decisão do time, não houve revisão por outra pessoa.

## Página da música e legenda da vitrine — issue #66 (26/11/2026)

- A falha ao carregar uma música oferece "Tentar novamente".
- A legenda "Quantidade de reviews nesta rede, em todo o período" fica no componente da vitrine, usado no feed e em `/musicas`.
- Claude Code fez os ajustes. Por decisão do time, não houve revisão por outra pessoa.


## Aceite e encerramento da entrega de dados #13 — 26/11/2026

- Bruno escolheu concluir a entrega de dados sem aguardar Descobrir e demais integrações de produto. A decisão não altera a pendência dessas funcionalidades nas respectivas issues nem declara reputação pelo perfil/API implementada.
- #78 conciliado com main e integrado após 375 testes aprovados/1 skip. #82 atualizado sobre essa main, sem novos defeitos bloqueantes encontrados; suíte final com 378 testes aprovados e zero skips, incluindo seed completo e cálculo independente de reputação.
- Instalação nova: catálogo/seed/CLI, startup/check, reexecução, reset com backup e restauração efetiva aprovados. Capturas da interface real mostram corrente/ramo, raiz independente, ranking e conta nova, sem mocks. Evidências em docs/evidencias/issue13/README.md e validacao.json.
- No ensaio, edição/exclusão/descurtida/unfollow foram preservados na reexecução. Reset recompôs a massa inicial e o backup recuperou o estado anterior; nenhum banco pessoal foi alterado. Não houve aviso, comentário ou menção ao time nesta etapa.
- Reputação histórica após exclusão, correção/recálculo, reescutas/bibliotecas e Descobrir permanecem nas issues próprias. Reescuta não foi apresentada como validada sem serviço integrado. Instruções institucionais foram conferidas no material versionado, sem afirmar envio ou acesso ao Classroom.

## Issue #39 — catálogo e identidade musical — 26/11/2026

- Bruno aprovou concluir o escopo de dados reaproveitando a entrega do #32 e a integração do #60. As referências históricas à #9 acima descrevem o estado daquela entrega; a integração já existe e o aceite atual é da #39.
- Preservadas seis fictícias para homônimos/versões e 20 reais para demo, sem expansão ou alteração de chaves. Gêneros/tags continuam listas abertas; normalização existente e revisão de consistência sem vocabulário fechado.
- Chave curada estável e opaca identifica a entrada; ID interno é atribuído pelo banco e preservado na reimportação. Entrada manual é curadoria do arquivo, sem cadastro pela interface. Metadados iguais não autorizam fusão; original/remix/ao vivo/remaster são distintos.
- Referências Spotify existentes não provam equivalência entre serviços. Vínculo futuro exige confirmação manual da gravação/edição, com fontes, responsável e justificativa registrados; sem confirmação, manter entradas separadas. Sem OAuth, matching ou schema novo nesta entrega.
- Codex atualizou documentação e acrescentou teste de navegador sem mocks para o aceite. Dados/API: 217 testes aprovados; validadores: 6 e 20 entradas; build/typecheck aprovados; Chrome desktop: cenário técnico e real aprovados, com duas contas, publicação, perfil e feed.
- Evidências e reprodução: `docs/evidencias/issue39/README.md`. Sem mudanças de contrato público, migração ou implementação de outra área. PR com `Closes #39`, sujeito à revisão de outra pessoa antes do merge.

### Revisão do PR #83 — 26/11/2026

- Atendidas as três sugestões publicadas por Bruno: corrigida frase histórica de catálogo real; teste agora identifica cada cartão de perfil/feed por link da review e exige quantidade, artista e versão; criada rotina única para executar os dois catálogos em bancos separados, interrompendo em erro.
- Seleção do cenário resolve caminho relativo/absoluto como o carregador, evitando depender da grafia literal da variável. Dados e contratos preservados. Nova revisão estática do diff e validações registradas nas evidências da #39; Bruno autorizou publicação e merge após as correções e a nova revisão.

## Apagar comentário — 26/11/2026

- **Rota:** `DELETE /posts/{post_id}/comentarios/{comentario_id}` (`204`), exige login. Antes não havia como apagar um comentário, e a tela não tinha o botão.
- **Quem pode:** **só quem escreveu o comentário** (`403` para outra pessoa, inclusive o autor da review). Decisão simples e igual à das reviews ("só o autor altera"); se o grupo quiser que o autor da review modere os comentários dela, é uma mudança pequena.
- **Erros:** `404` se o comentário não existe ou pertence a outra review; apagar duas vezes dá `404` na segunda; id acima de 2^63-1 dá `422`.
- **Efeito:** o contador `comentarios` das reviews diminui. Comentários não pontuam reputação, então nada mais muda.
- **Falta (Cecília):** o botão "apagar" ao lado dos comentários próprios na tela da review.
- **Testes:** `test_comentarios_apagar.py` (6 casos). Claude Code implementou; o código ainda precisa ser revisado por outra pessoa do time.

## Reputação ligada à API — issues #10 e #11 — 26/11/2026

Liga o motor de reputação de `core/reputacao.py` (Bruno, #43) ao banco e ao perfil. **Correção de origem (#19) e recálculo (#20) não fazem parte desta entrega.**

- **Fórmula (já aprovada, não mudou):** curtida de outra pessoa dá **4** ao autor da review, **2** ao autor da origem imediata e **1** ao ancestral seguinte; publicar uma review derivada dá 4, 2 e 1 aos três autores anteriores da corrente, e **o autor da nova não ganha**; curtida própria dá **1** só ao autor, sem propagar; se o mesmo autor aparece em mais de um nível do mesmo evento, fica a maior parcela. Publicar uma raiz, comentar, seguir e editar **não pontuam**. Os pontos são inteiros.
- **Onde aparece:** `GET /usuarios/{username}` passou a devolver `reputacao` (um número inteiro), visível a qualquer pessoa logada. Não é a contagem de curtidas nem a popularidade da música.
- **Fonte de verdade: eventos guardados no banco**, na tabela `eventos_reputacao` (uma linha por fato: `curtida:{usuario}:{review}` ou `derivada:{review}`, com chave única, então **nenhum fato conta duas vezes**). Ela é separada da tabela de curtidas de propósito: apagar uma review apaga as curtidas dela, mas os créditos já concedidos **são conservados**. Os totais não são guardados: são **refeitos a partir dos eventos e da árvore quando o backend sobe**, em O(eventos), o que também reproduz o mesmo resultado depois de reiniciar.
- **Atomicidade:** o evento é gravado no **mesmo commit** da curtida ou da review derivada, e só depois aplicado nos totais em memória, sob a mesma trava da árvore. Uma curtida repetida não grava evento nem pontua de novo. **Descurtir remove o evento e retira exatamente os pontos que ele concedeu**; curtir de novo concede uma vez só.
- **Exclusão:** apagar uma review conserva os créditos que ela já gerou e os que ela deu à corrente, e **interações futuras continuam percorrendo o registro apagado** na árvore: uma curtida nova numa review descendente ainda credita quem apagou a de origem. Isso usa `reviews_apagadas`, que guarda autor e origem.
- **Dados gravados por fora da API** (um seed, um banco antigo): na subida, `sincronizar_eventos` cria os eventos que faltam para curtidas e derivadas que já existem. Só acrescenta (nunca remove, para não perder créditos de reviews apagadas) e repetir é seguro.
- **Inconsistência não derruba o sistema:** se os eventos não baterem com a árvore, a reconstrução vira um aviso no log e o resto da rede continua funcionando; os totais ficam como estavam.
- **Ponto em aberto do time:** pela fórmula, quem está na corrente também ganha pontos ao **curtir uma review descendente** (a Ana, curtindo a da Júlia, recebe 2). O `DECISIONS.md` diz que a prevenção de abuso segue em discussão; esta entrega **não** muda a regra aprovada.
- **Fora desta entrega:** ranking global, e a tela do número no perfil (Cecília).
- **Testes:** `test_reputacao_api.py` cobre a corrente Ana → Júlia → Pedro, o quarto nível sem pontos, raiz isolada, curtida própria, repetição, descurtir e recurtir, o que não pontua, exclusão (meio, folha e a review curtida), curtida futura creditando o registro apagado, reinício com os mesmos totais, dados de fora e dado inconsistente.
- Claude Code implementou a ligação e os testes. O código ainda precisa ser revisado por outra pessoa do time.

## Review repetida leva à existente — issue #33 (26/11/2026)

- Quando o servidor recusa uma segunda review da mesma gravação, o formulário oferece abrir a review que já existe. Nada é duplicado e a origem dela não muda.
- O 409 não informa o id: a tela o procura nas reviews da própria pessoa e, se não achar, leva ao perfil.
- Claude Code fez o ajuste e os testes. Por decisão do time, não houve revisão por outra pessoa.

## Reputação no perfil e apagar comentário — telas de #42 e do PR #87 (26/11/2026)

- O perfil mostra o número de reputação que o servidor envia, inclusive zero, com uma frase de explicação. Sem o campo, nada aparece. A tela não recalcula pontos.
- "Apagar" aparece só nos próprios comentários e pede confirmação. Comentário já apagado em outro lugar sai da lista; em servidor sem a rota, ele permanece e a tela avisa.
- Dependem do backend dos PRs #86 e #87. A correção de origem (#42) continua pendente.
- Claude Code fez as telas e os testes. Por decisão do time, não houve revisão por outra pessoa.

## Recomendador puro TF-IDF — #55 — 26/11/2026

Regras fechadas com Bruno: qualquer nota gera peso 3 por gravação com review
própria ativa; uma ou várias curtidas externas elegíveis geram peso 1 por
gravação, sem somar à própria. Auto-curtida não aumenta o perfil. Nota e texto
não entram no contrato. Apagar a própria review remove sinal e exclusão;
curtida externa remanescente pode assumir peso 1. Versões são identidades
separadas; curtida externa não impede sugestão. Biblioteca privada não participa.

Escolhida biblioteca de ML: scikit-learn 1.9.1 no lockfile. TF-IDF binário,
IDF suavizado `log((1+N)/(1+df))+1`, normalização L2, sem TF sublinear; fit sobre
todo catálogo. Artista, gênero e tag têm multiplicador igual, com prefixos de
campo e valores inteiros normalizados por casefold/espaços; sem sinônimos ou
remoção de acentos. Vetores por gravação são somados com pesos 3/1 e o perfil
é normalizado novamente a cada consulta. Sem cache de perfil. Novo catálogo
exige novo índice, construído antes de substituir o anterior.

Afinidade positiva primeiro: cosseno decrescente, data da representante
decrescente, chave crescente. Uma review por gravação, escolhida por curtidas
atuais decrescentes, data decrescente e ID decrescente. Isso seleciona a review,
sem somar popularidade à afinidade. Curtidas para contagem são pares únicos.
Candidatas precisam de review pública ativa; review própria ativa exclui.

Completar com fallback de score zero: ordenar por data decrescente/chave crescente,
agrupar por artista e emitir um item por grupo a cada rodada, preservando a
ordem da primeira candidata dos grupos. Diversidade só no fallback. Sem perfil
utilizável, motivo sem_sinais; com perfil sem termos comuns, sem_afinidade.
Explicação personalizada usa até três termos comuns de maior contribuição ao
produto escalar (empate lexical). Nenhuma característica acústica é inferida.

Motor sem banco/FastAPI em core, com registros imutáveis e erros de domínio;
contrato, custos conservadores e recálculo em core/README.md. API/paginação,
autorização e snapshot consistente são #23; tela é #56. Feed e ranking de
quantidade de reviews não são alterados. Sem migração de banco.

Trata-se de recomendação baseada em conteúdo com representação estatística,
sem treinamento supervisionado. A escolha de biblioteca não comprova obrigação
de ML pela rubrica. Reviews negativas também sinalizam interesse; termos raros,
inclusive artista, podem dominar. Catálogo curado limita cobertura. Score não é
probabilidade; sugestão não comprova escuta/descoberta. Testes sintéticos não
comprovam satisfação real de usuários. Aceite escolhido: testes e relatório
local, sem avaliação humana ou métrica offline obrigatória.

Código, testes e documentação elaborados com Codex. Bruno autorizou publicar
e integrar esta entrega sem aguardar revisão independente; não há alegação de
aprovação de outra pessoa. Esta entrega não declara API integrada.

Validação local: suíte completa com 400 aprovados; após adicionar dois cenários
finais, suíte de dados com 208 aprovados e recomendador com 19 aprovados.
Aviso preexistente TestClient/HTTPX. Instalação congelada, consistência do lock,
compilação, demonstração e diff aprovados. Evidências e reprodução em
`docs/evidencias/issue55/README.md` e `demo.json`. Banco de testes temporário;
nenhum banco pessoal alterado.

## Parecer sobre as funcionalidades opcionais — issue #53 (26/11/2026)

- Esboços e comparação em [docs/funcionalidades-opcionais.md](docs/funcionalidades-opcionais.md). É proposta de Cecília, redigida com Claude Code; a priorização continua sendo do trio.
- Recomendação para 27/11: não implementar grupos, mensagens diretas nem integrações com streaming. O diferencial a demonstrar é a corrente de descobertas. Depois da entrega, avaliar primeiro os grupos, que reaproveitam os cartões do feed.
- Spotify: pela documentação oficial, o modo de desenvolvimento exige dono com Premium e aceita até 5 usuários; o modo estendido só aceita organizações. Deezer: viabilidade não comprovada. Nenhuma integração foi entregue nem testada.

## Correção de origem, reputação e Descobrir no front — #42 e #56 (26/11/2026)

- A reputação é buscada de novo depois de curtir ou descurtir no perfil; a tela não calcula pontos e explica a fórmula 4/2/1.
- Correção de origem e Descobrir foram feitas sobre contratos propostos pelo front, testados com respostas simuladas: `PATCH /posts/{id}/origem` e `GET /descobrir`. As rotas ainda não existem no backend (#10, #23); as telas não comprovam integração.
- "Corrigir origem" aparece só para quem escreveu uma review derivada e quando o servidor publica a rota. Pede confirmação e não converte raiz nem remove origem.
- Sem a rota de Descobrir, a página continua avisando que as sugestões estão em preparação.
- O PR #89 propõe encerrar a #42 e a #56 apenas quanto ao front, validado com respostas simuladas, como o texto das issues permite. O funcionamento com o servidor continua pendente na #10 e na #23. As issues pedem revisão de outra pessoa; o time havia decidido não revisar PRs.
- Claude Code fez as telas e os testes.

## API do Descobrir — issue #23 — 27/11/2026

Liga o recomendador TF-IDF do Bruno (`core/recomendador.py`, #55) à API, no contrato que a tela da Cecília (#56) já usa.

- **Rota:** `GET /descobrir?offset&limit` (login obrigatório; `limit` de 1 a 100, padrão 10; `offset` até 2^63-1, senão `422`). **Separada de `/feed`**: o feed continua só com quem a pessoa segue, em ordem cronológica, e não mudou.
- **Resposta:** `{items: [{review, explicacao}], total, offset, limit, personalizada}`. A `review` tem o mesmo formato do feed (música, nota, curtidas vistas por quem pede, comentários, autor). `personalizada` é falso enquanto a conta **não tem reviews nem curtidas**: nesse caso a lista é só uma amostra de reviews recentes da comunidade, não um ranking de afinidade. Ele vem **dos sinais da própria conta** (review própria, ou curtida na review de outra pessoa; auto-curtida não conta) e não do ranking: quem já avaliou todo o catálogo continua personalizado, com a lista vazia ("Nenhuma sugestão por enquanto" na tela).
- **O que entra:** uma review por gravação ainda **não avaliada** pela pessoa (a mais curtida, depois a mais recente), em ordem de afinidade; sem afinidade ela vem depois, com diversidade por artista. Quem já avaliou uma música não a recebe de volta; curtir a review de outra pessoa **não** impede sugerir essa música.
- **Sinais (já decididos com o Bruno):** só as interações **de quem pede** formam o perfil (review própria pesa 3, curtida em review alheia pesa 1, auto-curtida não conta). Curtir, descurtir, avaliar e apagar a própria review mudam o resultado **na próxima chamada**: não há cache de perfil, o ranking é refeito a cada consulta.
- **Privacidade:** a resposta traz só a explicação em texto e a review pública. **Nunca** score, termos ou perfil de gosto de outra conta. As curtidas dos outros entram apenas na contagem que escolhe a review mais curtida de cada música. Não há bibliotecas privadas no produto, então nada disso entra.
- **Explicação:** em português, a partir do motivo do recomendador: "Combina com o que você avaliou ou curtiu. Em comum: gênero indie, tag guitarra." (até 3 termos, só artista, gênero e tag, **com a grafia do catálogo**, e não a normalizada que o recomendador compara; nada de característica acústica), "Não tem nada em comum…" ou, sem sinais, "Você ainda não avaliou nem curtiu nada, então esta é uma review recente da comunidade.".
- **Paginação depois do ranking:** o `total` é o do ranking inteiro e a ordem é determinística (mesmas entradas, mesma ordem). Se alguém curtir ou avaliar entre duas páginas, itens podem mudar de lugar, como o recomendador já avisa.
- **Snapshot:** todas as reviews (só existem as ativas, apagar remove a linha) e as curtidas **dessas reviews**, filtradas em conjunto: uma review criada ou apagada entre as duas leituras não derruba a rota. Se o recomendador recusar a entrada, a rota responde `503` com mensagem simples e deixa um aviso no log.
- **Índice:** depende só do catálogo e é **refeito quando o catálogo muda** (comparação do conteúdo a cada chamada, barata), nunca editado no lugar.
- **Limites:** o custo por chamada é o do recomendador, **O(reviews + curtidas)**, aceitável para o tamanho da demo e não para uma rede grande; é um processo só, sem cache entre processos.
- **Testes:** `test_descobrir.py` (25 casos): login, formato, ausência de score e perfil, conta sem sinais, afinidade e explicação (com a grafia do catálogo), curtir e descurtir como sinal, apagar a própria review, review apagada de outra pessoa, uma review por música, isolamento entre contas, paginação estável, parâmetros inválidos, feed intacto, quem avaliou tudo continua personalizado e o `503` quando o recomendador recusa a entrada.
- Claude Code implementou a API e os testes. O código ainda precisa ser revisado por outra pessoa do time.


## Troca estrutural de origem — #49 (26/11/2026)

- Implementação pura em `FlorestaReviews`, em duas etapas: preparar sem mutação
  e aplicar plano imutável. Retorna subárvore BFS completa e caminhos anterior/novo
  para consumo futuro da #51; não calcula reputação nem cria eventos.
- Somente review ativa derivada pode mudar para destino ativo da mesma música.
  Impede próprio nó e descendentes, inclusive através de referências apagadas.
  Origem anterior apagada pode ser corrigida. Não converte raiz nem remove origem.
- Origem atual ativa é sucesso sem alteração: afetados vazios e caminhos iguais.
  Mutação efetiva ou reconstrução invalida planos; falhas/no-ops não invalidam.
  Planos copiados, de outra instância ou antigos são rejeitados antes da escrita.
- A revisão é global à instância: até alterações em outro ramo invalidam planos,
  favorecendo segurança e simplicidade. Referências fracas evitam reter planos.
- Movimento acrescenta a review ao fim dos filhos do destino e conserva a ordem
  dos demais nós; reconstruções seguem a ordem dos registros carregados.
- Preparo O(S + H), aplicação O(D) por cópias das listas dos pais; não é O(1)
  global. Contrato completo e integração de sincronização estão no README do core.
- Banco/API/recuperação permanecem na #10; recálculo na #51 e interface na #42.
  Esta implementação não comprova integração dessas entregas.


## Corrigir a origem de uma review — issue #10 — 27/11/2026

Liga a troca estrutural do Bruno (`FlorestaReviews.preparar_troca_origem` e `aplicar_troca_origem`, #49) ao banco, à árvore em memória e à reputação, no contrato que a tela da Cecília (#42) já usa.

- **Rota:** `PATCH /posts/{id}/origem` com `{"origem_id": n}` devolve a review atualizada (mesmo formato do feed). Login obrigatório; a tela a detecta pela documentação da API. A troca é **entre origens**: converter uma raiz em derivada ou remover a origem de uma derivada continua decisão adiada, como já estava registrado.
- **Quem e o quê:** só o **autor** troca (`403`). A review precisa ser derivada (`422` para raiz), e a nova origem precisa ser uma review **ativa da mesma música** (`422` se não existe, foi apagada ou é de outra música). Não pode ser a própria review nem uma que veio dela, o que criaria ciclo (`422`, validado pela árvore, inclusive por baixo de reviews apagadas). Trocar para a origem atual é sucesso sem alteração. Corpo inválido ou id acima de 2^63-1 dá `422`. A origem antiga **apagada** pode ser corrigida.
- **Subárvore:** as derivadas da review movida vão junto, com a mesma estrutura. A árvore antiga perde o ramo e a nova o ganha; o feed e a página da review passam a mostrar a origem nova (ela vem do banco).
- **Ordem (nada é mudado antes de tudo estar validado):** valida o banco e a árvore sem mutar; **grava no banco** com atualização condicional; só então aplica a troca na árvore em memória e refaz os pontos. Tudo sob a trava da árvore, então duas trocas ou uma troca e uma publicação não se atropelam.
- **Concorrência:** a gravação é condicional à origem lida (`WHERE id = ? AND origem_id = ?`). Se a review foi apagada ou trocada no meio, nada é gravado e a resposta é `409` ("a review mudou… tente de novo"). Se a árvore em memória estava atrás do banco (dados gravados por fora, como um seed), ela é refeita uma vez a partir do banco; se ainda estiver inconsistente, `503`. Uma origem apagada *depois* da validação e antes da gravação não é detectada (a origem não tem chave estrangeira, de propósito), igual ao que já acontece ao publicar uma derivada.
- **Reputação (recálculo retroativo):** os pontos acompanham a **corrente nova**. Os eventos (curtidas e derivadas) já estão guardados no banco, e o crédito de cada um depende da corrente atual; por isso, depois da troca, **os totais são refeitos a partir dos eventos e da árvore nova**: os créditos antigos saem, os novos entram, pela mesma fórmula 4/2/1 (maior parcela por autor em cada evento). **Mover a origem não cria evento** (não é curtida nem recomendação), e as reviews apagadas continuam na conta. Quem se move **não perde** os próprios pontos; os ancestrais antigos perdem o que vinha dele e os novos ganham.
- **Estratégia e custo:** é um recálculo completo, **O(eventos) por troca**, em vez de um incremental pelos nós afetados que o plano do Bruno também permite. Escolhido por ser simples, determinístico e já provado no reinício do backend (o mesmo código). Serve para o tamanho da demo; numa rede grande valeria o incremental (#51).
- **Recuperação:** o banco é a fonte de verdade. O motor troca os totais só se a carga inteira for válida. Se o recálculo falhar, a árvore é refeita a partir do banco e ele tenta de novo; se ainda falhar, fica o aviso no log e o **reinício refaz os totais corretos**. Uma queda entre a gravação e o recálculo também se resolve no reinício. Não há transação única entre banco e memória.
- **Testes:** `test_trocar_origem.py` (20 casos): troca e resposta, subárvore que acompanha, árvore antiga sem o ramo, idempotência, pontos que acompanham a corrente e voltam ao desfazer, nenhum evento novo, reinício com o mesmo resultado, origem apagada corrigida, feed com a origem nova, `403`/`401`/`404`/`422`/ciclo, documentação da API, trocas simultâneas sem `500` e com banco, memória e pontos coerentes, o `409` quando a review é apagada ou trocada no meio da operação e a árvore refeita quando a review foi gravada por fora (seed). Verificado também no navegador, com a demo e a tela da Cecília: mover a review do Daniel da Cecília para o Gustavo tirou 4 pontos da Cecília e 2 do Bruno e deu 4 ao Gustavo.
- Claude Code implementou a rota e os testes sobre o #96 do Bruno. O código ainda precisa ser revisado por outra pessoa do time.

- **Rota:** `GET /descobrir?offset&limit` (login obrigatório; `limit` de 1 a 100, padrão 10; `offset` até 2^63-1, senão `422`). **Separada de `/feed`**: o feed continua só com quem a pessoa segue, em ordem cronológica, e não mudou.
- **Resposta:** `{items: [{review, explicacao}], total, offset, limit, personalizada}`. A `review` tem o mesmo formato do feed (música, nota, curtidas vistas por quem pede, comentários, autor). `personalizada` é falso enquanto a conta **não tem reviews nem curtidas**: nesse caso a lista é só uma amostra de reviews recentes da comunidade, não um ranking de afinidade. Ele vem **dos sinais da própria conta** (review própria, ou curtida na review de outra pessoa; auto-curtida não conta) e não do ranking: quem já avaliou todo o catálogo continua personalizado, com a lista vazia ("Nenhuma sugestão por enquanto" na tela).
- **O que entra:** uma review por gravação ainda **não avaliada** pela pessoa (a mais curtida, depois a mais recente), em ordem de afinidade; sem afinidade ela vem depois, com diversidade por artista. Quem já avaliou uma música não a recebe de volta; curtir a review de outra pessoa **não** impede sugerir essa música.
- **Sinais (já decididos com o Bruno):** só as interações **de quem pede** formam o perfil (review própria pesa 3, curtida em review alheia pesa 1, auto-curtida não conta). Curtir, descurtir, avaliar e apagar a própria review mudam o resultado **na próxima chamada**: não há cache de perfil, o ranking é refeito a cada consulta.
- **Privacidade:** a resposta traz só a explicação em texto e a review pública. **Nunca** score, termos ou perfil de gosto de outra conta. As curtidas dos outros entram apenas na contagem que escolhe a review mais curtida de cada música. Não há bibliotecas privadas no produto, então nada disso entra.
- **Explicação:** em português, a partir do motivo do recomendador: "Combina com o que você avaliou ou curtiu. Em comum: gênero indie, tag guitarra." (até 3 termos, só artista, gênero e tag, **com a grafia do catálogo**, e não a normalizada que o recomendador compara; nada de característica acústica), "Não tem nada em comum…" ou, sem sinais, "Você ainda não avaliou nem curtiu nada, então esta é uma review recente da comunidade.".
- **Paginação depois do ranking:** o `total` é o do ranking inteiro e a ordem é determinística (mesmas entradas, mesma ordem). Se alguém curtir ou avaliar entre duas páginas, itens podem mudar de lugar, como o recomendador já avisa.
- **Snapshot:** todas as reviews (só existem as ativas, apagar remove a linha) e as curtidas **dessas reviews**, filtradas em conjunto: uma review criada ou apagada entre as duas leituras não derruba a rota. Se o recomendador recusar a entrada, a rota responde `503` com mensagem simples e deixa um aviso no log.
- **Índice:** depende só do catálogo e é **refeito quando o catálogo muda** (comparação do conteúdo a cada chamada, barata), nunca editado no lugar.
- **Limites:** o custo por chamada é o do recomendador, **O(reviews + curtidas)**, aceitável para o tamanho da demo e não para uma rede grande; é um processo só, sem cache entre processos.
- **Testes:** `test_descobrir.py` (25 casos): login, formato, ausência de score e perfil, conta sem sinais, afinidade e explicação (com a grafia do catálogo), curtir e descurtir como sinal, apagar a própria review, review apagada de outra pessoa, uma review por música, isolamento entre contas, paginação estável, parâmetros inválidos, feed intacto, quem avaliou tudo continua personalizado e o `503` quando o recomendador recusa a entrada.
- Claude Code implementou a API e os testes. O código ainda precisa ser revisado por outra pessoa do time.

## Auditoria e recuperação do recálculo — #51 — 26/11/2026

- A reconstrução completa entregue pelo #97 atende ao algoritmo da #51: usa a árvore atual, recalcula os eventos da subárvore junto com os demais e substitui contribuições/totais deterministicamente. Não há exigência de atualização incremental nos critérios da issue. Mantido esse caminho, sem índice adicional nem alteração da fórmula 4/2/1.
- A auditoria encontrou uma lacuna: depois de confirmar a origem no banco, a falha das tentativas de recálculo podia responder sucesso e continuar expondo totais antigos. Agora o serviço guarda disponibilidade global sob `arvores.TRAVA`, inicialmente falsa. Falha preserva o snapshot anterior internamente, mas não o publica. Uma aplicação/remoção parcial durante a pendência não libera esse snapshot.
- `PATCH /posts/{id}/origem` mantém a resposta de review e acrescenta `reputacao_disponivel: bool`. Origem salva responde `200` inclusive com `false`: a tela mostra a origem nova e “Origem corrigida. Reputação temporariamente indisponível.” Isso distingue alteração gravada de troca recusada; não afirma que os pontos foram atualizados. Erros anteriores ao commit mantêm os contratos existentes.
- `GET /usuarios/{username}` mantém o perfil disponível, com `reputacao: null` em falha; zero continua sendo total válido. O cliente oculta totais anteriores após falha de atualização e oferece “Tentar atualizar reputação”. Servidores antigos que omitem o campo continuam suportados. A mudança para nullable exige os ajustes de frontend incluídos nesta entrega.
- Uma consulta ao perfil ou repetição da origem atual tenta recuperar a pendência. Reconstrução da árvore deve ter sucesso antes de calcular os créditos; falha de árvore nunca autoriza usar a floresta anterior. São no máximo duas tentativas de cálculo por recuperação, com reconstrução prévia da árvore. Falha de leitura SQL faz rollback da transação de leitura, preservando o commit anterior da origem. Não há tarefa periódica, promessa de recuperação de dados corrompidos nem necessidade de reinício para recuperar falha transitória.
- Startup usa a mesma recuperação. Novas curtidas/derivadas e descurtidas persistem pelos contratos atuais; se o acumulador está indisponível, tentam reconstrução completa em vez de aplicar um evento isolado. Eventos de referências apagadas continuam preservados; descurtidas removem os fatos ativos pelo contrato existente. Tipo de evento desconhecido é rejeitado em vez de interpretado como derivação.
- Custo real: ler/processar E eventos é O(E), além da ordenação por ID feita pelo banco (dependente do plano SQL); a recuperação também reconstrói N referências, com ordenação O(N log N) e validação da floresta. Memória adicional O(N + E + U), para U autores, além do snapshot anterior até a substituição. Não se apresenta esta solução como incremental ou O(tamanho da subárvore).
- Mantidos banco como fonte de verdade, ausência de transação única banco/memória e funcionamento em um processo. Outras instâncias não compartilham a trava nem o estado de disponibilidade. O aviso de indisponibilidade é global ao acumulador, pois ainda não há isolamento por autor.
- Aceite: testes com banco descartável comparam totais e contribuições por evento com oráculo independente dos registros do banco: troca entre árvores, ancestrais compartilhados, autor repetido, auto-curtida, descendente apagado com curtida preservada, descurtida, repetição, retorno e reinício. Injeção de falhas cobre cálculo, árvore, SQL, startup, recuperação transitória e interações durante pendência. Testes focados de interface verificam aviso da troca salva, ocultação e botão de recuperação em desktop e 360 px, com respostas simuladas; não equivalem a navegador com backend real para os caminhos de falha.
- Revisão independente permanece pendente; validação automatizada não é revisão de outra pessoa. Não há migração ou alteração de dados existentes.

## Bibliotecas e privacidade — issue #12 (parte das bibliotecas) — 27/11/2026

Entrega só a **API das bibliotecas**. **Reescutas** (aviso "Ouvi novamente", limite de 24 horas, avisos no feed) e a integração com Spotify e Deezer **não fazem parte desta entrega**, e as telas são da Cecília (#45). O Bruno não deixou código de bibliotecas (só texto no seed e a regra do recomendador de não usar biblioteca privada), então o backend inteiro é novo.

- **Duas listas por pessoa, calculadas e não guardadas:** as **descobertas** são as músicas que ela conheceu por outra review (as reviews **derivadas**, com a origem); as **recomendações** são as que indicou por conta própria (as **independentes**). Como saem das reviews vivas, ficam coerentes sozinhas: apagar uma review a tira da lista, corrigir a origem (#97) muda a origem mostrada, e **curtir, comentar ou visitar não registram nada**. Uma música aparece uma vez só (há uma review ativa por pessoa e música), da mais nova para a mais antiga.
- **Privacidade (já aprovada):** descobertas **privadas** e recomendações **públicas** por padrão; **só a dona muda** (`PATCH /usuarios/eu/biblioteca`), e cada lista é independente da outra. A dona sempre abre as duas.
- **Lista privada para um terceiro:** `403` com só `{"detail": "esta lista é privada"}`, **mesmo se a lista estiver vazia**, para a resposta não revelar se há itens, quantos nem de onde vieram. No resumo, a lista restrita traz `acessivel: false` e `total: null`. **As reviews continuam públicas** no perfil e no feed: a lista privada esconde a coleção, não as reviews.
- **Rotas (todas com login):** `GET /usuarios/{username}/biblioteca` (resumo das duas listas: `visibilidade`, `acessivel`, `total`), `GET /usuarios/{username}/biblioteca/{lista}?offset&limit` (`lista` = `descobertas` ou `recomendacoes`; cada item é a **review no formato do feed**, com música e origem; `limit` de 1 a 100, `offset` até 2^63-1, senão `422`) e `PATCH /usuarios/eu/biblioteca` com `{"descobertas": "privada|publica", "recomendacoes": "privada|publica"}` (ao menos um; repetir o mesmo valor não muda nada). Pessoa ou lista inexistente (inclusive um nome antigo como `favoritas`) dá `404`.
- **Persistência:** só a visibilidade é guardada, na tabela nova `visibilidades_biblioteca` (uma linha por pessoa, criada na **primeira mudança**; sem linha valem os padrões). Como é tabela nova, **bancos antigos a ganham sozinhos** na subida, sem migração. A primeira mudança simultânea da mesma pessoa não dá `500` (a segunda tentativa encontra a linha).
- **Origem apagada:** a descoberta continua na lista, com `origem_id` e `origem: null`, como no feed.
- **Para a Cecília (#45):** a tela precisa do resumo (para mostrar "acesso restrito" sem contagem), da lista paginada e do controle de visibilidade; a navegação lateral ainda diz "Minha biblioteca (em breve)".
- **Limites:** sem duplicação por escuta porque **reescuta não existe ainda**; sem janela de 24 horas; uma biblioteca é só das reviews publicadas, não um histórico de escuta (a rede não tem histórico e a tela não deve sugerir que tem).
- **Testes:** `test_biblioteca.py` (23 casos): padrões, as duas listas, formato do item, uma música uma vez e ordem, curtir/comentar/visitar sem efeito, pessoa sem músicas, terceiro com lista pública e privada sem vazamento (inclusive lista vazia), as **quatro combinações** de visibilidade, reviews públicas no perfil, independência entre pessoas, mudança parcial e idempotente, login e valores inválidos, linha só depois da primeira mudança, concorrência, exclusão, origem apagada, correção de origem, nova derivada, `404`, `401`, paginação e curtidas vistas por quem pede. Verificado também com a demo do Bruno.
- Claude Code implementou a API e os testes. O código ainda precisa ser revisado por outra pessoa do time.

## Ajustes finais do front (27/11/2026)

- A página Pessoas passou a usar o visual da rede, com paginação. Saiu o formulário do modelo inicial que criava usuário sem senha; contas são criadas em `/registro`. As rotas do backend não mudaram.
- No celular, o título e o artista da review deixam de se espremer ao lado da capa.
- Testes que supunham a falta de Descobrir e da correção de origem agora simulam essa falta.
- Claude Code fez os ajustes e os testes. Não houve revisão por outra pessoa.

## Telas das bibliotecas — #45 (27/11/2026)

- `/usuarios/{username}/biblioteca` mostra Descobertas e Recomendações, com o cartão de review do feed. O acesso fica no perfil e em "Minha biblioteca".
- Só a dona vê o controle de visibilidade, por lista; a tela muda depois da confirmação do servidor. Lista restrita mostra acesso restrito, sem itens, contagem ou origem.
- Depende do backend do PR #100. Sem ele, a página avisa que as bibliotecas não estão disponíveis.
- "Ouvi novamente" e os avisos no feed continuam fora: não há backend. A #45 permanece aberta.
- Claude Code fez as telas e os testes. Não houve revisão por outra pessoa.

## Reescutas — issue #12 (parte das reescutas) — 27/11/2026

Completa a #12 no backend (as bibliotecas já estão na `main`). **A integração com Spotify e Deezer (#21 e #22) continua fora**: o aviso é sempre manual, sem sugestão externa.

- **O que é:** o aviso "ouvi novamente" de uma pessoa sobre uma música que ela já avaliou, com comentário opcional. **Não é review: não cria review, nó da árvore, música nem pontos**, e não conta nas "mais avaliadas". A curtida continua sendo uma só, na review original, e as ações dos avisos apontam para ela.
- **Quem e quando:** só o **autor da review** avisa (`403` para outra pessoa, inclusive quem a segue; `404` se a review não existe). O comentário é opcional, de até **500 caracteres** (`422` acima disso; só espaços valem como vazio). Qualquer review do autor serve, raiz ou derivada.
- **Limite de 24 horas:** no máximo **um aviso por pessoa e música a cada 24 horas**, em **janela móvel contada do aviso mais recente**. Um segundo antes de completar 24 horas ainda é bloqueado; **exatamente 24 horas depois libera**. O bloqueio responde `429` com o cabeçalho `Retry-After` (segundos) e uma mensagem com o tempo que falta ("tente de novo em 12 h e 30 min"). Um aviso recusado não grava nada nem gasta a janela. O limite é por pessoa **e** por música: outra música da mesma pessoa, ou a mesma música de outra pessoa, não é afetada.
- **Concorrência:** a checagem e a gravação são **um único comando do banco** (`INSERT ... SELECT ... WHERE NOT EXISTS`), que o SQLite executa de uma vez; assim duas requisições simultâneas **não passam as duas**. Verificado com 16 requisições ao mesmo tempo: exatamente uma `201`, as outras `429`, nunca `500`. Num banco com leitura concorrente (como o Postgres) seria preciso uma trava ou isolamento serializável.
- **Edição e exclusão:** editar a review depois **não muda a data nem o comentário do aviso**, e a `review` que o aviso traz é a de agora; editar também não reabre a janela. **Apagar a review apaga os avisos dela**; se a pessoa publicar de novo a mesma música, a janela recomeça (limite conhecido, a decisão aprovada é que a exclusão remove os avisos).
- **Rotas (todas com login):** `POST /posts/{id}/reescutas` (`{"comentario": "..."}`, opcional), `GET /posts/{id}/reescutas?offset&limit` (os avisos de uma review) e `GET /feed/reescutas?offset&limit` (os avisos de **quem a pessoa segue**, sem os próprios, do mais novo para o mais antigo). Cada item traz `id`, `comentario`, `created_at` (os do aviso) e a `review` no formato do feed, vista por quem pede. `limit` de 1 a 100 e `offset` até 2^63-1, senão `422`.
- **Os avisos ficam numa rota própria, e não dentro de `/feed`,** de propósito: o contrato do feed cronológico (só reviews, só de quem se segue) **não mudou**, e a tela o intercala pela data (`created_at` do aviso e `created_at` da review). Para a Cecília: mostrar o aviso como um cartão separado ("Ouvi novamente", com o comentário e a data do aviso) apontando para a review atual, e tratar o `429` mostrando o tempo que falta.
- **Persistência:** tabela nova `reescutas` (autor, música, review, comentário, data), com índice por autor, música e data para a janela. Como é tabela nova, **bancos antigos a ganham sozinhos** na subida, sem migração.
- **Testes:** `test_reescutas.py` (19 casos), com um relógio controlado para testar **antes e exatamente depois de 24 horas**, janela móvel, bloqueio com `Retry-After`, independência por pessoa e música, recusa que não gasta a janela, **concorrência**, review alheia, edição posterior, exclusão, nenhuma review, nó, evento de reputação nem mudança em árvore, ranking e feed, curtida única, leitura paginada, só os seguidos no feed e login.
- Claude Code implementou a API e os testes. O código ainda precisa ser revisado por outra pessoa do time.

## Nome e marca: scuta (27/11/2026)

- Cecília informou que a rede se chama **scuta** e forneceu o kit de logo. Substitui “MeetMusic” (provisório) e o título “Descoberta musical”.
- O ícone (balão de conversa com uma nota) aparece na barra, na página inicial e como ícone da aba; o nome usa a Merriweather já adotada.
- A disponibilidade do nome e do domínio não foi verificada.
- Claude Code aplicou a marca no site.

## Ouvi novamente e avisos no feed — #45 (27/11/2026)

- "Ouvi novamente" aparece na própria review e quando o servidor recusa uma segunda review da mesma gravação, ao lado do acesso para editar. O comentário é opcional, até 500 caracteres, e fica no campo em caso de falha; no bloqueio de 24 horas a tela mostra o tempo informado pelo servidor.
- Os avisos ficam em um bloco separado no alto do feed, com data e comentário próprios; não são intercalados com as reviews por data. Curtir e derivar continuam na review original.
- A tela usa as rotas do backend das reescutas (#12): `POST /posts/{id}/reescutas` e `GET /feed/reescutas`. O servidor não informa se a review foi editada depois do aviso, então a tela não indica isso.
- Spotify e Deezer não fazem parte.
- Claude Code fez as telas e os testes. Não houve revisão por outra pessoa.

## Parecer técnico do backend: grupos, mensagens diretas, Spotify e Deezer — issue #21 — 27/11/2026

É um **parecer, não uma implementação**: nada aqui foi construído, nada aprova um recurso, e a escolha de implementar continua sendo do trio. Ele completa o parecer de experiência da Cecília (#53, `docs/funcionalidades-opcionais.md`) com o que a #21 pede do backend: contratos, modelos, permissões, dependências e estimativa. As issues #14, #15 e #22 foram absorvidas pela #21, e o encerramento delas foi reorganização, não implementação. O `CONTRATO.md` traz contratos-modelo de grupos e de mensagens, mas é sugestão ("não é obrigatório"); onde divergem do produto, vale o que está aqui.

**Recomendação de prioridade (a mesma do parecer da Cecília):** nenhuma das quatro entra em 27/11, porque o diferencial a mostrar é a corrente de descobertas. Depois da entrega: 1º **grupos**, 2º **mensagens diretas** (só com bloqueio e denúncia antes), 3º **Spotify** como teste restrito, 4º **Deezer** só com acesso oficial confirmado.

| Item | Esforço no backend | Principal bloqueio |
|---|---|---|
| Grupos e semana musical | Médio a grande (3 tabelas, 7 rotas, ~30 testes) | Nenhum técnico; falta decisão de produto |
| Mensagens diretas | Grande (4 tabelas, 8 rotas, ~40 testes, moderação) | A rede não tem bloqueio nem denúncia |
| Spotify | Médio, com limite de acesso | Acesso oficial não comprovado (Premium, 5 usuários) |
| Deezer | Não estimado | Viabilidade não comprovada |

### Grupos de amigos e semana musical
- **Contrato proposto:** `POST /grupos` (nome; quem cria vira administrador), `GET /grupos` (só os de que a pessoa participa; **sem busca pública** na primeira versão), `POST /grupos/{id}/convites` (a administração gera um código com validade), `POST /grupos/entrar` (com o código; idempotente), `DELETE /grupos/{id}/membros/eu` (sair), `GET /grupos/{id}/membros` e `GET /grupos/{id}/semana?inicio=&offset&limit` (as reviews dos membros publicadas de segunda a domingo, no formato do feed). **Diverge do `CONTRATO.md`**: o grupo não tem posts próprios; o conteúdo são as reviews que os membros já publicam, como propõe a Cecília.
- **Modelos (tabelas novas, criadas sozinhas na subida, sem migração):** `Grupo` (nome, criação), `Membro` (grupo, pessoa, papel, entrada; chave composta) e `Convite` (grupo, código único, validade, revogado).
- **Permissões:** só membros veem membros e a semana, e quem não é membro recebe `404` (não `403`, para não revelar que o grupo existe); só a administração gera ou revoga convite; se a administradora sai, o papel passa ao membro mais antigo; se o último sai, o grupo deixa de existir e **as reviews não são apagadas**.
- **Alternativas de visibilidade:** (a) **privado por convite**, recomendada; (b) público e listável, que exige busca, moderação e denúncia, e fica para depois; (c) público por link, que na prática é (a) com convite sem validade. A semana **reaproveita** `listar_reviews` (autor entre os membros e data no intervalo), então o feed pessoal **não muda**.
- **Publicação não é escuta:** a semana musical mostra reviews **publicadas**, e não o que a pessoa ouviu; a tela não deve dizer "ouviu". Uma "escuta verificada" só existiria com um serviço conectado (abaixo) e seria um tipo de evidência à parte, nunca misturada com a review nem com o aviso manual "ouvi novamente".
- **A decidir:** o fuso das fronteiras da semana (o banco guarda UTC, e uma semana de Brasília começa 3 horas depois) e o tamanho máximo do grupo.
- **Dependências já atendidas:** autenticação, reviews e `listar_reviews`.

### Mensagens diretas
- **Contrato proposto:** `POST /mensagens/{username}` (`{"texto", "review_id"?}`), `GET /conversas` (da mais recente, com contagem de não lidas), `GET /conversas/{username}?antes=&limit` (**cursor** pelo id, e não por `offset`, porque numa conversa viva um `offset` repete ou pula mensagens) e `POST /conversas/{username}/lidas`. A regra da Cecília vale: **só quem se segue mutuamente inicia conversa**; deixar de seguir impede novas mensagens e mantém o histórico para as duas. Mensagem para si mesmo dá `422`.
- **Modelos:** `Conversa` (o par ordenado de pessoas, único), `Mensagem` (conversa, autor, texto de até 2.000 caracteres, `review_id` opcional, chave de envio, data), `LeituraConversa` (até onde cada pessoa leu) e `Bloqueio`, que **a rede ainda não tem**.
- **Permissões (o ponto de segurança):** toda consulta filtra pela pessoa logada ser participante, e **terceiro tentando ler conversa alheia recebe `404`**, igual a uma conversa que não existe; a regra de seguir mutuamente é conferida **no envio**. O anexo guarda só o `review_id`: se a review for apagada, o cartão mostra "review apagada", sem o conteúdo. Receber mensagem **não cria origem nem pontua**.
- **Envio duplicado:** uma chave enviada pela tela, única por conversa e autor; repetir o envio devolve a mesma mensagem, sem duplicar.
- **Ordem e paginação:** estável por data e id. **Sem tempo real**: a conversa atualiza ao abrir; WebSocket fica fora.
- **Pré-requisitos que não existem:** bloqueio, denúncia e uma política de retenção e exclusão de mensagens (são dados pessoais privados). Sem isso, **não recomendo lançar**.

### Spotify e Deezer
- **Estado: acesso oficial NÃO comprovado, integração pendente, nada entregue nem testado com conta ou chave reais.** Pela regra da issue, o desfecho é este bloqueio documentado. A consulta às páginas oficiais foi feita em 26/11/2026, e deve ser refeita antes de qualquer decisão, porque essas regras mudam.
- **Bloqueios concretos:** (1) o time **não tem aplicativo registrado nem credenciais**; (2) **Spotify**: em modo de desenvolvimento o dono precisa de Premium e só 5 pessoas usam a integração, e o modo estendido só aceita organizações (com pelo menos 250 mil usuários ativos por mês), então **não atende o público da rede**; a leitura das músicas tocadas recentemente exige a permissão `user-read-recently-played`; (3) **Deezer**: as páginas pedem login e não informam se há criação de novos aplicativos, e a viabilidade é **não comprovada**.
- **Para destravar, a evidência necessária:** criar um aplicativo no painel de cada serviço com uma conta de verdade (no Spotify, com Premium), cadastrar contas de teste, executar o fluxo real de autorização e registrar data e captura. É uma ação de uma pessoa do time, e **não dá para fazer só com código**.
- **Desenho técnico, se destravar:** autorização OAuth 2.0 com as permissões mínimas e tela de consentimento; tabela `conexoes_musicais` (pessoa, serviço, tokens **cifrados em repouso** com chave em variável de ambiente, nunca em log, validade, permissões); renovação, expiração, **revogação** (a pessoa desconecta, e o `401` do serviço também desconecta) e desconexão que apaga os tokens; a consulta é oficial e sob demanda, **sem scraping**; as sugestões ficam numa fila privada (pessoa, música, data da reprodução, id do evento **único**, para um evento repetido não duplicar) e **nunca se tornam públicas**.
- **Ligação com o catálogo:** uma faixa só vira sugestão se **casar com uma música do catálogo e a pessoa já tiver review dela**; faixa desconhecida é ignorada (o catálogo é curado, e ninguém adiciona música), e o histórico vazio não atrapalha o fluxo manual. **Achado importante:** as chaves do catálogo guardam o ID do Spotify **em minúsculas** (`spotify-4ra6zuylxk69bf3dpvpggo`), mas os IDs do serviço diferenciam maiúsculas (`4ra6zuyLXk69bF3dPVpGGO`), então **a chave não serve para consultar a API**. É preciso um campo próprio de ID externo, na grafia original (`servico` e `id_externo`), preenchido para as 20 músicas a partir da tabela de links do `docs/demo-issue-13.md`. Equivalência **entre** serviços continua exigindo confirmação manual, como já decidido; o código ISRC, que os serviços costumam expor, serviria como evidência a confirmar, nunca como prova.
- **O destino da confirmação já existe:** a pessoa confirma e a tela chama `POST /posts/{id}/reescutas` (#105), com o limite de 24 horas e sem criar review, nó nem pontos. **Nada é publicado sozinho.** Se for implementado, a validação exigida é: consentimento negado, token expirado ou revogado, desconexão, evento repetido e ausência de publicação automática.

**O que já está pronto para receber qualquer um deles:** autenticação, `listar_reviews`, a tabela de seguidores, as bibliotecas (#100), as reescutas (#105) e a criação automática de tabelas novas sem migração.

Claude Code redigiu este parecer; a revisão por outra pessoa do time continua pendente.

## Publicação persistente do Scuta — 27/11/2026

O frontend público estava compilado com localhost e a API não estava hospedada.
A correção publica FastAPI no Render Free e PostgreSQL 16 no Neon Free, mantendo
o domínio da Vercel. Banco novo com catálogo, sem importar contas locais nem
executar seed de demonstração; dados ficam fora do disco efêmero do Render.
SQLite local e seu atualizador legado continuam disponíveis. O esquema inicial
PostgreSQL é criado pelos modelos; futuras mudanças exigem migração explícita.

Uma instância/worker preserva o modelo atual de estruturas em memória. TLS na
conexão remota, DEBUG=false, CORS com origens explícitas e /health com consulta
ao banco. O build público exige uma URL HTTPS da API, sem localhost. Previews
não recebem automaticamente a API/banco de produção. A integração Git da Vercel
foi reconectada ao fork novo, preservando projeto e domínios.

O plano adotado foi explicitamente somente gratuito. Aceitam-se as cotas e o
início a frio; nenhum upgrade pago foi contratado. Deploys do Render permanecem
manuais após validação. Procedimentos, evidências e limites estão no guia 08.
Implementação e validação assistidas pelo Codex; testes automatizados e a
jornada real não equivalem a revisão humana independente.

## Demonstração pública ativada — 27/11/2026

Bruno autorizou preservar as contas atuais e acrescentar a demonstração do PR #5. A configuração anterior de banco sem seed foi atualizada por essa decisão: permanecem o mesmo banco Neon e todos os dados anteriores; acrescentaram-se 25 contas, 50 reviews, 20 seguidas e 30 curtidas pela API. O catálogo público de 50 músicas foi somado às 6 músicas de teste existentes. Sem exclusões ou troca de banco. Senha privada da demonstração armazenada apenas no ambiente do Render, sob SCUTA_DEMO_PASSWORD. A carga não roda no boot; republicações importam apenas o catálogo idempotente e preservam as contas. Validação e limites em docs/popular-demonstracao-publica.md.
