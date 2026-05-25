# Integracao

Cada modulo publica `OPENAPI.yaml`. No baseline, o gateway devera autenticar
JWT/API key e repassar `X-Actor-User-Id` somente apos validar escopos.

## Convencoes

- UUID em identificadores e `user_id` sempre associado ao All-in-One ID.
- Eventos no exchange `all-in-one.domain`; consumidores idempotentes.
- Valores BRL com quatro casas; NEX com oito casas.
- Webhooks devem ser assinados e aceitar retry com idempotency key.
- Integracoes nunca recebem biometria bruta nem prontuario sem base legal.
