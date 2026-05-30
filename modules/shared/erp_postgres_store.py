from __future__ import annotations

from typing import Any
from psycopg import Connection
from psycopg.types.json import Jsonb
from .postgres_store import BasePostgresStore

class ErpPostgresStore(BasePostgresStore):
    """Production Erp adapter backed by typed PostgreSQL relations and central audit/outbox."""

    module = "erp"
    backend = "postgres_erp_typed_store"
    tables = {
        "accounts": "erp.accounts",
        "payables": "erp.payables",
        "receivables": "erp.receivables",
        "cost_centers": "erp.cost_centers",
        "fiscal_documents": "erp.fiscal_documents",
    }
    soft_deletable = frozenset(['accounts', 'payables', 'receivables', 'cost_centers', 'fiscal_documents'])

    def _insert(
        self,
        connection: Connection,
        resource_type: str,
        resource_id: str,
        user_id: str,
        entity_id: str | None,
        status: str,
        payload: dict[str, Any],
        actor: str,
        idempotency_key: str | None,
    ) -> dict[str, Any]:
        return self._insert_generic(
            connection, resource_type, resource_id, user_id, entity_id, status, payload, actor, idempotency_key
        )

    def _update(
        self, connection: Connection, resource_type: str, resource_id: str, payload: dict[str, Any], status: str, actor: str
    ) -> dict[str, Any]:
        return self._update_generic(connection, resource_type, resource_id, payload, status, actor)
