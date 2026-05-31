from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "config" / "module_catalog.json").read_text(encoding="utf-8"))
STITCH_MANIFEST = ROOT / "config" / "stitch" / "screen_manifest.json"
COMPLIANCE_MATRIX = ROOT / "config" / "compliance" / "data_classification.json"
VSCODE_SETTINGS = ROOT / ".vscode" / "settings.json"
VSCODE_TASKS = ROOT / ".vscode" / "tasks.json"
REQUIRED_MODULE_FILES = {
    "README.md",
    "main.py",
    "requirements.txt",
    "CONTRACT.md",
    "STATUS.md",
    "OPENAPI.yaml",
    "DATABASE.md",
    "EVENTS.md",
    "SECURITY.md",
    "MONETIZATION.md",
    "TESTS.md",
    "Dockerfile",
    "tests/test_health.py",
    "tests/test_contract.py",
    "tests/test_permissions.py",
    "tests/test_create_flow.py",
}
REQUIRED_SCHEMAS = {
    "identity", "business", "permissions", "marketplace", "stock", "delivery",
    "services", "mobility", "erp", "wms", "tms", "crm", "bpm", "document",
    "finance", "billing", "fiscal", "hr", "health", "vision", "legal",
    "property", "audit", "compliance", "notifications", "api_hub",
    "insurance", "bi", "ai_core", "jobs",
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    modules = CATALOG["modules"]
    slugs = {module["slug"] for module in modules}
    if len(slugs) != 25:
        fail(f"Esperados 25 modulos; catalogo possui {len(slugs)}.", errors)
    for module in modules:
        base = ROOT / "modules" / module["slug"]
        for relative in REQUIRED_MODULE_FILES:
            if not (base / relative).is_file():
                fail(f"Ausente: modules/{module['slug']}/{relative}", errors)
        if not (ROOT / "contracts" / f"{module['slug']}.md").is_file():
            fail(f"Contrato ausente: {module['slug']}", errors)
    for app in CATALOG["apps"]:
        if not (ROOT / "apps" / app["slug"] / "README.md").is_file():
            fail(f"App ausente: {app['slug']}", errors)
    migrations = "\n".join(
        item.read_text(encoding="utf-8")
        for item in sorted((ROOT / "database" / "postgres" / "migrations").glob("*.sql"))
    )
    for schema in REQUIRED_SCHEMAS:
        if f"CREATE SCHEMA IF NOT EXISTS {schema}" not in migrations:
            fail(f"Schema PostgreSQL nao declarado: {schema}", errors)
    for needle in [
        "identity.users",
        "finance.wallets",
        "NUMERIC(18, 4)",
        "NUMERIC(18, 8)",
        "reject_immutable_change",
        "audit.logs",
        "jobs.resumes",
        "employment_provenance_integrity",
        "immutable_jobs_resume_access_logs",
        "storage_encryption",
        "idx_jobs_documents_idempotency",
    ]:
        if needle not in migrations:
            fail(f"Controle SQL ausente: {needle}", errors)
    for workflow in [
        "ci.yml",
        "security.yml",
        "database.yml",
        "openapi.yml",
        "autocommit.yml",
        "automerge.yml",
        "compose-health.yml",
        "git-sync.yml",
    ]:
        if not (ROOT / ".github" / "workflows" / workflow).is_file():
            fail(f"Workflow ausente: {workflow}", errors)
    for script in ["check_git_sync.ps1", "validate_compose_health.ps1", "check_generated_artifacts.ps1"]:
        if not (ROOT / "scripts" / script).is_file():
            fail(f"Gate operacional ausente: {script}", errors)
    if not (ROOT / "pytest.ini").is_file():
        fail("Configuracao pytest.ini ausente.", errors)
    else:
        pytest_ini = (ROOT / "pytest.ini").read_text(encoding="utf-8")
        if "--import-mode=importlib" not in pytest_ini or "--basetemp=.pytest_tmp" not in pytest_ini:
            fail("pytest.ini deve centralizar importlib e basetemp local .pytest_tmp.", errors)
    if not VSCODE_SETTINGS.is_file():
        fail("Configuracao VS Code ausente: .vscode/settings.json", errors)
    else:
        settings = json.loads(VSCODE_SETTINGS.read_text(encoding="utf-8"))
        expected_python = "${workspaceFolder}/.venv/Scripts/python.exe"
        if settings.get("python.defaultInterpreterPath") != expected_python:
            fail(f"python.defaultInterpreterPath deve ser {expected_python}.", errors)
        if settings.get("python.testing.pytestArgs") not in ([], None):
            fail("python.testing.pytestArgs deve ficar vazio; pytest.ini e a fonte obrigatoria.", errors)
    if not VSCODE_TASKS.is_file():
        fail("Configuracao VS Code ausente: .vscode/tasks.json", errors)
    else:
        tasks = json.loads(VSCODE_TASKS.read_text(encoding="utf-8"))
        pytest_tasks = [task for task in tasks.get("tasks", []) if task.get("label") == "test: pytest completo"]
        if not pytest_tasks:
            fail("Task VS Code test: pytest completo ausente.", errors)
        elif pytest_tasks[0].get("command") != "${config:python.defaultInterpreterPath}":
            fail("Task pytest deve usar ${config:python.defaultInterpreterPath}.", errors)
    if not (ROOT / "workers" / "outbox_dispatcher" / "main.py").is_file():
        fail("Worker da outbox RabbitMQ ausente.", errors)
    if not STITCH_MANIFEST.is_file():
        fail("Manifesto de telas Stitch ausente.", errors)
    else:
        stitch = json.loads(STITCH_MANIFEST.read_text(encoding="utf-8"))
        projects = stitch.get("projects", [])
        if stitch.get("project_count") != len(modules) or len(projects) != len(modules):
            fail("Stitch deve declarar um projeto por modulo.", errors)
        if not all(project.get("screen_count", 0) > 0 for project in projects):
            fail("Todo projeto Stitch deve declarar telas.", errors)
    if not (ROOT / "docs" / "COMPLIANCE.md").is_file():
        fail("Documento de compliance ausente: docs/COMPLIANCE.md", errors)
    if not COMPLIANCE_MATRIX.is_file():
        fail("Matriz de dados sensiveis ausente: config/compliance/data_classification.json", errors)
    else:
        compliance = json.loads(COMPLIANCE_MATRIX.read_text(encoding="utf-8"))
        if set(compliance.get("modules", {})) != slugs:
            fail("Matriz de compliance deve cobrir exatamente os 25 modulos do catalogo.", errors)
        for slug, entry in compliance.get("modules", {}).items():
            for field in ["risk_level", "data_domains", "sensitive_categories", "legal_basis", "retention_policy", "production_gate"]:
                if not entry.get(field):
                    fail(f"Matriz de compliance incompleta em {slug}.{field}.", errors)
    if errors:
        print("Validacao falhou:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Baseline valido: {len(slugs)} modulos, {len(CATALOG['apps'])} apps e controles centrais presentes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
