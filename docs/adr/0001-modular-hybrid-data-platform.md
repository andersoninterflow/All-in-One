# ADR 0001: Plataforma Modular Com Persistencia Hibrida

- Status: Accepted
- Data: 2026-05-25

## Decisao

Adotar microservicos FastAPI padronizados, PostgreSQL para identidade,
dinheiro, contratos e auditoria, MongoDB para memoria IA/social/telemetria,
e RabbitMQ para eventos. `identity.users` e a raiz obrigatoria dos recursos.

## Consequencias

O baseline e executavel e testavel sem fingir integracoes reguladas. Novas
features devem preservar FKs de propriedade, logs append-only, contratos
versionados, aprovacoes manuais e validacao de compliance.
