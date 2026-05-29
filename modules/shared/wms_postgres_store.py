from __future__ import annotations

from typing import Any
from psycopg import Connection
from psycopg.types.json import Jsonb
from .postgres_store import BasePostgresStore

class WmsPostgresStore(BasePostgresStore):
    """Production Wms adapter backed by typed PostgreSQL relations and central audit/outbox."""

    module = "wms"
    backend = "postgres_wms_typed_store"
    tables = {
        "warehouses": "wms.warehouses",
        "bins": "wms.bins",
        "inventory": "wms.inventory",
        "picking_waves": "wms.picking_waves",
        "shipments": "wms.shipments",
    }
    soft_deletable = frozenset(['warehouses', 'bins', 'inventory', 'picking_waves', 'shipments'])

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
        metadata = self._metadata(payload)
        # Fallback para insert generico se nao houver colunas mapeadas
        # Como estamos em fase de expansao, usamos o metadata como store principal
        # e as colunas base do PostgreSQL.
        table = self._table(resource_type)
        
        # Heuristica: se houver company_id ou business_id no payload, usamos
        entity_col = "company_id" if "company_id" in payload else ("business_id" if "business_id" in payload else None)
        
        cols = ["id", "user_id", "status", "metadata", "created_by", "updated_by", "idempotency_key"]
        vals = [resource_id, user_id, status, metadata, actor, actor, idempotency_key]
        
        if entity_col:
            cols.insert(2, entity_col)
            vals.insert(2, payload[entity_col])
            
        query = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(vals))}) RETURNING *"
        return connection.execute(query, tuple(vals)).fetchone()

    def _update(
        self, connection: Connection, resource_type: str, resource_id: str, payload: dict[str, Any], status: str, actor: str
    ) -> dict[str, Any]:
        metadata = self._metadata(payload)
        table = self._table(resource_type)
        return connection.execute(
            f"UPDATE {table} SET status = %s, metadata = %s, updated_by = %s, updated_at = NOW() WHERE id = %s RETURNING *",
            (status, metadata, actor, resource_id),
        ).fetchone()
