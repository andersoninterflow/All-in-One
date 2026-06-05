from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from scripts import multi_agent_sync_guard as guard


def test_lock_blocks_a_second_agent(monkeypatch, tmp_path: Path) -> None:
    path = tmp_path / "agent.lock"
    monkeypatch.setattr(guard, "lock_path", lambda: path)

    acquired = guard.acquire_lock("codex_cli", "catalogo Valley", 120)

    assert acquired["agent"] == "codex_cli"
    with pytest.raises(RuntimeError, match="Workspace em uso"):
        guard.acquire_lock("antigravity", "outra atividade", 120)


def test_stale_lock_can_be_replaced(monkeypatch, tmp_path: Path) -> None:
    path = tmp_path / "agent.lock"
    path.write_text(
        (
            '{"agent":"agente_antigo","pid":1,'
            f'"acquired_at":"{(datetime.now(UTC) - timedelta(hours=3)).isoformat()}"'
            "}"
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(guard, "lock_path", lambda: path)

    acquired = guard.acquire_lock("codex_cli", "retomada segura", 120)

    assert acquired["agent"] == "codex_cli"
    assert guard.read_lock(path)["activity"] == "retomada segura"


def test_release_refuses_another_agent(monkeypatch, tmp_path: Path) -> None:
    path = tmp_path / "agent.lock"
    monkeypatch.setattr(guard, "lock_path", lambda: path)
    guard.acquire_lock("codex_cli", "catalogo Valley", 120)

    with pytest.raises(RuntimeError, match="Lock pertence"):
        guard.release_lock("gemini_code")

    guard.release_lock("codex_cli")
    assert not path.exists()
