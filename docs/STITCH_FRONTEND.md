# Google Stitch Para Front-End

## Estrategia

O planejamento visual e automatizado a partir de `config/module_catalog.json`.
Cada um dos 25 microservicos recebe um projeto isolado no Stitch, com telas
para visao geral, entidades operacionais, auditoria/permissoes e jornadas
especificas quando necessarias. Jobs inclui curriculo com procedencia,
importacao CTPS, busca de vagas e revisao Business auditada.

`config/stitch/screen_manifest.json` e o contrato compacto e deterministico de
projetos, contagens e telas especializadas; as telas por entidade sao
expandidas pelo orquestrador a partir do catalogo. `config/stitch/sync_state.json`
preserva IDs remotos retornados pelo Stitch para evitar duplicacao.

## Seguranca Da Autenticacao

O servidor MCP Stitch e obrigatorio e persistente neste workspace. A entrada
canonica fica em `~/.codex/config.toml`, mantendo o mesmo endpoint da
documentacao oficial do Stitch MCP e substituindo o header literal por
`env_http_headers` para nao persistir segredo em texto:

```toml
[mcp_servers.stitch]
url = 'https://stitch.googleapis.com/mcp'
http_headers = { Accept = 'application/json' }
env_http_headers = { 'X-Goog-Api-Key' = 'STITCH_API_KEY' }
```

Credenciais nunca entram em commits, manifestos ou prompts. Configure
`STITCH_API_KEY` somente via secret local/CI apos rotacao de qualquer chave
exposta em mensagem, log ou captura. A politica versionada fica em
`config/autonomy/stitch_mcp_policy.json`.

## Operacao

```bash
python scripts/stitch_orchestrator.py plan
python scripts/validate_stitch_mcp_config.py
python scripts/stitch_orchestrator.py discover
python scripts/stitch_orchestrator.py sync
```

`plan` nao acessa a rede e materializa o contrato. `validate_stitch_mcp_config`
confirma a politica versionada e a configuracao persistente sem exigir segredo.
`discover` autentica no MCP e lista as ferramentas anunciadas pelo Stitch.
`sync` cria projetos/telas ausentes e atualiza o estado local sem recriar o que
ja possui identificador.

Para uma validacao online, exporte `STITCH_API_KEY` no ambiente e rode:

```bash
python scripts/validate_stitch_mcp_config.py --require-secret
python scripts/stitch_orchestrator.py discover
```

Os prompts proíbem dados sensiveis, documentos brutos e segredos em mockups.
Antes da implementacao web/mobile, os designs gerados devem ser revisados
contra contratos dos modulos e regras de LGPD.
