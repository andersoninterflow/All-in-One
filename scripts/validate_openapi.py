from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "config" / "module_catalog.json").read_text(encoding="utf-8"))
REQUIRED_OPERATIONS = {
    ("/health", "get"),
    ("/version", "get"),
    ("/status", "get"),
    ("/metrics", "get"),
    ("/create", "post"),
    ("/list", "get"),
    ("/{id}", "get"),
    ("/{id}", "patch"),
    ("/{id}", "delete"),
    ("/approve", "post"),
    ("/reject", "post"),
    ("/audit", "post"),
}


def main() -> int:
    errors: list[str] = []
    for module in CATALOG["modules"]:
        slug = module["slug"]
        source = ROOT / "modules" / slug / "OPENAPI.yaml"
        try:
            contract = yaml.safe_load(source.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"{slug}: YAML invalido: {exc}")
            continue
        if contract.get("openapi") != "3.1.0":
            errors.append(f"{slug}: versao OpenAPI deve ser 3.1.0")
        paths = contract.get("paths", {})
        for path, operation in REQUIRED_OPERATIONS:
            if operation not in paths.get(path, {}):
                errors.append(f"{slug}: operacao ausente {operation.upper()} {path}")
        schemes = contract.get("components", {}).get("securitySchemes", {})
        if "bearerAuth" not in schemes:
            errors.append(f"{slug}: bearerAuth ausente")
        for operation in ["/create", "/approve", "/reject", "/audit"]:
            if "requestBody" not in paths.get(operation, {}).get("post", {}):
                errors.append(f"{slug}: requestBody ausente em POST {operation}")
    if errors:
        print("OpenAPI invalido:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"OpenAPI valido para {len(CATALOG['modules'])} modulos e todas as operacoes minimas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
