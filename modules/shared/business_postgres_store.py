from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator
from uuid import uuid4

import psycopg
from psycopg import Connection, sql
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from .correlation import get_correlation_id
from .store import DuplicateValueError
                    "UPDATE {} SET deleted_at = NOW(), updated_by = %s, updated_at = NOW() WHERE id = %s"
                ).format(self._table(item["resource_type"])),
                (actor, item["id"]),
            )
            self._audit(connection, actor, "soft_delete", item["resource_type"], item["id"], item, None, item["user_id"], item["entity_id"])

    def audit_external(self, actor: str, action: str, resource_type: str, resource_id: str, data: dict[str, Any]) -> dict[str, Any]:
        with self.transaction() as connection:
            return self._audit(connection, actor, action, resource_type, resource_id, None, data, data.get("user_id"), data.get("company_id"))

    def _audit(
        self,
        connection: Connection,
        actor: str,
        action: str,
        resource_type: str,
        resource_id: str,
        before: Any,
        after: Any,
        user_id: str | None,
        entity_id: str | None,
    ) -> dict[str, Any]:
        evidence = connection.execute(
            """INSERT INTO audit.logs
               (user_id, actor_user_id, actor_entity_id, action, module, resource_type, resource_id,
                before_data, after_data, created_by)
               VALUES (%s, %s, %s, %s, 'business', %s, %s, %s, %s, %s) RETURNING *""",
            (user_id, actor, entity_id, action, resource_type, resource_id, Jsonb(before) if before else None, Jsonb(after), actor),
        ).fetchone()
        return dict(evidence)

    def _event(self, connection: Connection, routing_key: str, actor: str, item: dict[str, Any]) -> None:
        connection.execute(
            """INSERT INTO audit.domain_events
               (user_id, actor_user_id, entity_id, routing_key, aggregate_type, aggregate_id, correlation_id, payload, created_by)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                item["user_id"],
                actor,
                item["entity_id"],
                routing_key,
                item["resource_type"],
                item["id"],
                get_correlation_id(),
                Jsonb(item["payload"]),
                actor,
            ),
        )

    def audit_log(self) -> list[dict[str, Any]]:
        return [dict(row) for row in self.connection.execute(
            "SELECT * FROM audit.logs WHERE module = 'business' ORDER BY created_at DESC"
        ).fetchall()]

    def outbox(self) -> list[dict[str, Any]]:
        return [dict(row) for row in self.connection.execute(
            "SELECT * FROM audit.domain_events WHERE routing_key LIKE 'business.%' ORDER BY created_at DESC"
        ).fetchall()]

    def metrics(self) -> tuple[int, int, int]:
        records = sum(
            self.connection.execute(
                sql.SQL("SELECT COUNT(*) AS count FROM {}").format(self._table(resource_type))
            ).fetchone()["count"]
            for resource_type in TABLES
        )
        audits = self.connection.execute("SELECT COUNT(*) AS count FROM audit.logs WHERE module = 'business'").fetchone()["count"]
        events = self.connection.execute(
            "SELECT COUNT(*) AS count FROM audit.domain_events WHERE routing_key LIKE 'business.%'"
        ).fetchone()["count"]
        return records, audits, events
