# Operacao

## Gates por release

Execute scaffold check, validador de repositorio, testes Python, migrations em
banco limpo, validacao OpenAPI, scans de dependencia e imagem. Publique apenas
apos aprovacao manual das alteracoes financeiras, de identidade ou saude.

## Gates automatizados

- `scripts/check_git_sync.ps1`: valida merge/rebase em andamento, arvore local e
  divergencia entre a branch local e os remotos configurados.
- `scripts/validate_compose_health.ps1`: valida `docker compose config`, sobe o
  ambiente local e confirma `/health` nas 13 APIs FastAPI principais.
- `.github/workflows/git-sync.yml`: executa a verificacao de sincronizacao da
  `main` em eventos de push e sob demanda.
- `.github/workflows/compose-health.yml`: executa o healthcheck Docker Compose
  quando runtime, migrations, workers ou compose forem alterados.

## Evidencias

Auditoria critica e ledger sao append-only. Eventos devem manter
`correlation_id`; logs de aplicacao nao devem expor dados sensiveis.

## Incidentes

Revogue sessoes/API keys, preserve trilha imutavel, suspenda publicacao ou
pagamento afetado, notifique compliance e registre decisao e recuperacao.
