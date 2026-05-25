        # Events: Vision

        Exchange: `all-in-one.domain`; routing keys:

        - `vision.motion.detected`
- `vision.incident.created`

        Eventos carregam `event_id`, `occurred_at`, `actor_user_id`, `user_id`,
        `entity_id`, `correlation_id`, `schema_version` e payload minimizado.
        Consumidores devem ser idempotentes.
