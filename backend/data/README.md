# Catálogo e identidade musical — issue #39

`musicas.json` contém **seis faixas e artistas fictícios**, usados para testar homônimos e versões. `musicas_demo.json` contém **20 gravações reais** para demonstração. Ambos seguem o mesmo contrato. O módulo de dados não abre banco nem integra formulários; a aplicação já importa o catálogo e vincula reviews por ID interno.

## Validar sem iniciar a aplicação

Na raiz do repositório, com as dependências do backend já instaladas:

```bash
backend/.venv/bin/python backend/scripts/validar_catalogo.py
backend/.venv/bin/python backend/scripts/validar_catalogo.py /caminho/para/outro-catalogo.json
backend/.venv/bin/python -m pytest backend/tests_dados -q
```

Também é possível executar de `backend/` com `uv run python scripts/validar_catalogo.py` e `uv run pytest tests_dados -q`. O catálogo padrão é resolvido pelo local do módulo, independentemente da pasta atual. A ferramenta devolve código 0 no sucesso e 1 em erro de leitura ou validação, indicando entrada (contagem a partir de 1) e campo quando aplicável. Ela não altera o JSON nem grava dados.

Os testes ficam em `tests_dados/`, separados de `tests/`, cujo `conftest.py` prepara a infraestrutura de API/banco. Execute o comando específico acima; o `make test` atual continua cobrindo a suíte existente do time.

## Contrato dos registros

O arquivo é um array JSON UTF-8 não vazio. Os campos abaixo são obrigatórios, exceto `capa_url`; campos extras continuam recusados.

| Campo | Regra |
|---|---|
| `chave_catalogo` | Única no arquivo, estável, 1–100 caracteres, somente `a-z`, `0-9`, `_` e `-`. Não é normalizada. |
| `titulo`, `artista` | 1–200 caracteres após limpar espaços excedentes. Preservam caixa e acentos. |
| `tipo_versao` | `original`, `remix`, `ao_vivo` ou `remaster`. |
| `descricao_versao` | Até 200 caracteres após limpar espaços; não pode ficar vazia para remix, ao vivo ou remaster. Na original pode ser vazia. |
| `capa_url` | Opcional, omitida ou `null` quando não houver capa. Quando preenchida, URL absoluta HTTP/HTTPS de até 2048 caracteres; não aceita texto vazio, caminho local ou esquemas como `data:` e `javascript:`. |
| `generos`, `tags` | Listas não vazias de textos; cada termo tem 1–80 caracteres após limpeza. Espaços são normalizados, aplica-se `casefold` e repetições são removidas, preservando a primeira ordem. |

A normalização produz novos registros em memória. O arquivo de origem e suas chaves não são reescritos. Não há remoção automática de acentos, classificação por IA ou vocabulário fechado: mantenha os termos consistentes com o catálogo existente e revise novos sinônimos manualmente.

## Curadoria de identidades e versões

1. Antes de adicionar uma faixa, confirme manualmente se a gravação/edição já está no catálogo. Se existir, reutilize sua chave nas referências; não duplique o registro.
2. Outra gravação ou edição recebe uma chave nova e permanente. Original, remix, ao vivo e remaster são itens distintos; descreva a versão específica, por exemplo nome do remix, apresentação ou edição/ano. Duas apresentações ao vivo diferentes também precisam de chaves e descrições diferentes.
3. Título/artista não são identificadores. O mesmo título com outro artista é permitido; metadados iguais não autorizam fundir gravações. A ferramenta valida a estrutura e a unicidade das chaves, mas não decide equivalência musical.
4. Para corrigir grafia, descrição, gênero ou tags da mesma entrada, mantenha a chave. Não reutilize uma chave antiga para outra gravação e não renomeie chaves para acompanhar mudanças de título.
5. Valide o conjunto inteiro antes de entregar. Se qualquer entrada falhar, o carregador lança erro e não retorna uma lista parcial.

Os exemplos cobrem uma original com remix, ao vivo e remaster, outro artista com o mesmo título e uma faixa adicional. A expansão adicional do catálogo real e o matching externo ficam para outra entrega combinada.

## Consumo pelo backend e seed

A partir de `backend/`:

```python
from catalogo_musical import carregar_catalogo

registros = carregar_catalogo()  # list[dict], todos validados e normalizados
# Ou carregar_catalogo(caminho) para um catálogo específico.
```

`validar_catalogo(conteudo)` também aceita o array já lido. Falhas levantam `ErroCatalogo` (subclasse de `ValueError`). As funções não importam `app`, não abrem banco e não fazem chamadas externas.

A `chave_catalogo` identifica a entrada curada; o **ID interno do banco é atribuído e preservado pelo backend**, cuja importação idempotente reutiliza a mesma chave sem duplicar identidades. Os registros desta entrega não incluem `id` de banco. Spotify/Deezer só poderão ser associados ao mesmo item após confirmar a gravação; título/artista ou serviço diferente não bastam. Esta entrega não adiciona IDs externos, autenticação com provedores ou matching.

## Responsabilidades e integração atual

- **Dados (#39):** contrato, curadoria, gêneros, tags e consistência das identidades/versões.
- **Backend (#3):** importação e persistência, consulta e vínculo review/música; já há rotas e validações de identidade compartilhada e review única por pessoa/versão.
- **Frontend (#33):** seleção do catálogo e apresentação em detalhe/feed/perfil; já há integração com a API.

A antiga #9 foi reorganizada; seu encerramento não comprova a implementação de todas as áreas. O aceite de dados é acompanhado na #39 e suas evidências em `docs/evidencias/issue39/README.md`. Troca de música em review existente e funcionalidades de reescuta não fazem parte desta entrega.

## Entrada manual e correspondência entre serviços

Entrada manual significa adicionar uma entrada curada ao arquivo, com chave própria estável; não existe cadastro livre de músicas pela interface/API. A chave é interna ao catálogo, mesmo quando sua grafia inclui `spotify-`; o consumidor deve tratá-la como opaca. O ID numérico do banco não é um ID de provedor.

`referencias_spotify_demo.json` relaciona as 20 chaves da demo aos IDs e URLs Spotify de origem. Não comprova equivalência com Deezer ou outro serviço e não é um mecanismo de matching.

Antes de associar serviços à mesma entrada, o curador precisa confirmar a gravação e edição específicas, conferindo versão, créditos e identificação da fonte; título/artista iguais ou duração semelhante, isoladamente, não bastam. Registre fontes, responsável e justificativa da confirmação nas decisões da entrega que introduzir o vínculo. Sem confirmação, mantenha entradas separadas e não migre reviews. Esta entrega não introduz pares entre serviços, schema de equivalências, OAuth ou chamadas externas.

## Capas — ajuste da revisão do PR #32

Os seis exemplos fictícios usam `capa_url: null`; não foram associadas capas de artistas reais a faixas fictícias. Catálogos anteriores sem o campo continuam válidos. O retorno do carregador inclui `capa_url` como texto ou `None`, e pode ser serializado diretamente em JSON. URLs passam pela normalização padrão de `HttpUrl` (por exemplo, barra final no domínio); parâmetros e caminho são preservados. O limite de 2048 caracteres é aplicado ao valor normalizado.

A validação é estrutural e não testa existência, disponibilidade, formato do arquivo ou permissão de uso da imagem; não realiza acesso à rede. O front pode usar uma capa padrão quando o valor estiver ausente ou a imagem falhar. Persistência e inclusão nas respostas da API ficam com o backend; a URL não participa da identidade nem da deduplicação musical.

## Catálogo selecionado por ambiente

`carregar_catalogo()` e o startup do backend usam `CATALOGO_MUSICAL_PATH` quando definida. Caminho relativo é resolvido a partir de `backend/`, independentemente do diretório de execução. Exemplo: `CATALOGO_MUSICAL_PATH=data/musicas_demo.json`. Um argumento explícito a `carregar_catalogo(caminho)` tem precedência; sem variável, o padrão continua `data/musicas.json` (seis fictícias). Configuração vazia/inválida falha, sem retornar silenciosamente ao padrão.

O validador de linha de comando também usa a configuração quando não recebe arquivo explícito. Essa seleção não baixa músicas nem altera IDs. Na demonstração, iniciar seed e aplicação com a mesma variável para não importar outro catálogo ao reiniciar.

## Capas do catálogo público — 27/11/2026

As 50 músicas reais de `musicas_publico.json` têm `capa_url` HTTPS. As 20 compartilhadas com `musicas_demo.json` usam as mesmas imagens. As seis faixas fictícias continuam sem capa. Só o campo visual foi alterado: chaves, títulos, artistas, versões e reviews foram preservados.

`referencias_capas_publico.json` registra páginas de origem, álbum/edição quando disponível, critério e data da conferência. Para as 20 referências Spotify existentes, a miniatura vem do oEmbed do mesmo link. Nas outras 30, selecionamos uma referência visual de lançamento contendo a música do artista na Apple Music. Algumas capas são de compilações/reedições, inclusive remasterizações: as entradas não identificam uma edição específica, e a escolha visual não comprova equivalência de gravações nem altera a identidade musical. Aquarela do Brasil referencia uma compilação de Ary Barroso, evitando um resultado com capa de Rosa Passos.

As URLs foram acessadas e as imagens decodificadas na validação. Não há buscas no runtime nem necessidade de credenciais. A importação idempotente atualiza as músicas existentes sem recriar o banco; imagens indisponíveis usam o fallback musical da interface.

Fontes técnicas: [Spotify oEmbed](https://developer.spotify.com/documentation/embeds/reference/oembed) e [iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/UnderstandingSearchResults.html).
