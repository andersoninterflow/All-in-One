import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "autonomy" / "paid_services_policy.json"
PENDING_PATH = ROOT / "config" / "autonomy" / "paid_services_pending.json"
SYNC_SCRIPT = ROOT / "scripts" / "sync_paid_services_pending.py"


REQUIRED_PENDING_FIELDS = {
    "integration_key",
    "nome_servico",
    "finalidade",
    "custo_estimado",
    "beneficios",
    "impacto_da_nao_utilizacao",
    "prioridade",
    "recomendacao_tecnica",
    "status",
    "alternativa_gratuita_ou_local",
}


def test_paid_services_policy_contract_and_pending_registry() -> None:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    pending = json.loads(PENDING_PATH.read_text(encoding="utf-8"))

    assert policy["enabled"] is True
    assert policy["implementation_contract"]["default_mode"] == "optional_off_by_default"
    assert set(policy["implementation_contract"]["required_status_labels"]) == {
        "Status: Revisao futura",
        "Status: Implementacao futura (Servico Pago)",
    }
    assert policy["implementation_contract"]["technical_backlog_file"] == "config/autonomy/paid_services_pending.json"
    assert policy["approval_criteria"]["pr_cannot_fail_only_for_missing_paid_service"] is True

    assert pending["source"] == "config/integrations/provider_matrix.json"
    assert pending["items"]
    for item in pending["items"]:
        assert REQUIRED_PENDING_FIELDS <= set(item)
        assert item["prioridade"] in {"alta", "media", "baixa"}
        assert item["status"] in {
            "Status: Revisao futura",
            "Status: Implementacao futura (Servico Pago)",
        }


def test_sync_paid_services_pending_script_is_reproducible() -> None:
    before = PENDING_PATH.read_text(encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, str(SYNC_SCRIPT)],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr

    after_payload = json.loads(PENDING_PATH.read_text(encoding="utf-8"))
    before_payload = json.loads(before)

    assert before_payload["version"] == after_payload["version"]
    assert before_payload["source"] == after_payload["source"]
    assert before_payload["items"] == after_payload["items"]
