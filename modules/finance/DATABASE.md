        # Database: Finance Pay Billing Fiscal

        Schema relacional principal: `finance`.

        ## Entidades planejadas

        - `finance.wallets`
- `finance.ledger_entries`
- `finance.escrows`
- `finance.splits`
- `finance.invoices`

        Todo registro operacional inclui UUID, `user_id`, status, timestamps,
        atores de criacao/atualizacao e `metadata JSONB`. A implementacao inicial
        esta nas migracoes em `database/postgres/migrations/`; novas tabelas
        preservam a FK para `identity.users(id)`.
