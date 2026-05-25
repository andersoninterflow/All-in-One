        # Events: AI Core

        Exchange: `all-in-one.domain`; routing keys:

        - `ai.moderation.completed`
- `ai.memory.updated`

        Eventos carregam `event_id`, `occurred_at`, `actor_user_id`, `user_id`,
        `entity_id`, `correlation_id`, `schema_version` e payload minimizado.
        Consumidores devem ser idempotentes.
