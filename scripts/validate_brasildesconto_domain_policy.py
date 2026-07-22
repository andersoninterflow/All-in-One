from __future__ import annotations

import json
from pathlib import Path


REQUIRED_DNS_TYPES = {"A", "AAAA", "CNAME", "TXT", "MX", "SRV", "CAA", "NS", "PTR"}
REQUIRED_PRINCIPLES = {
    "infraestrutura_como_codigo",
    "automacao",
    "reprodutibilidade",
    "idempotencia",
    "seguranca",
    "documentacao_automatica",
}
REQUIRED_VALIDATION_CHECKS = {
    "dns_resolution",
    "https",
    "certificates",
    "apis",
    "redirects",
    "cors",
    "security_headers",
    "cache",
    "application_health",
    "logs",
    "monitoring",
}
REQUIRED_DOCS = {
    "README.md",
    "docs/DEPLOYMENT.md",
    "docs/OPERATIONS.md",
    "CHANGELOG.md",
}


def validate_brasildesconto_domain_policy(root: Path) -> list[str]:
    errors: list[str] = []
    policy_path = root / "config" / "autonomy" / "brasildesconto_domain_policy.json"

    if not policy_path.is_file():
        return ["Politica obrigatoria do dominio brasildesconto.com.br ausente."]

    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    if policy.get("enabled") is not True:
        errors.append("Politica do dominio brasildesconto.com.br deve estar habilitada.")
    if policy.get("domain") != "brasildesconto.com.br":
        errors.append("Politica do dominio deve declarar domain=brasildesconto.com.br.")
    if set(policy.get("principles", [])) != REQUIRED_PRINCIPLES:
        errors.append("Politica do dominio deve declarar todos os principios obrigatorios.")

    terraform = policy.get("terraform", {})
    for field in [
        "required",
        "import_existing_resources",
        "prevent_orphan_resources",
        "prevent_drift",
        "validate_before_apply",
    ]:
        if terraform.get(field) is not True:
            errors.append(f"Politica do dominio deve manter terraform.{field}=true.")

    cloudflare = policy.get("cloudflare", {})
    if cloudflare.get("required") is not True:
        errors.append("Politica do dominio deve manter cloudflare.required=true.")
    dns_types = set(cloudflare.get("dns_record_types", []))
    if dns_types != REQUIRED_DNS_TYPES:
        errors.append("Politica do dominio deve manter a lista completa de tipos DNS Cloudflare.")
    for field in [
        "validate_proxy_mode",
        "validate_ssl_mode",
        "validate_certificates",
        "validate_cache_rules",
        "validate_waf",
        "validate_zero_trust_when_enabled",
        "validate_pages_when_enabled",
        "validate_workers_when_enabled",
        "validate_r2_when_enabled",
        "validate_turnstile_when_enabled",
    ]:
        if cloudflare.get(field) is not True:
            errors.append(f"Politica do dominio deve manter cloudflare.{field}=true.")

    development_environment = policy.get("development_environment", {})
    for field in [
        "configure_primary_domain",
        "configure_subdomains",
        "configure_api_urls",
        "configure_oauth_callbacks",
        "configure_cors",
        "configure_environment_variables",
        "configure_certificates_when_applicable",
        "update_documentation",
    ]:
        if development_environment.get(field) is not True:
            errors.append(f"Politica do dominio deve manter development_environment.{field}=true.")

    validation_checks = set(policy.get("validation", {}).get("required_checks", []))
    if validation_checks != REQUIRED_VALIDATION_CHECKS:
        errors.append("Politica do dominio deve manter todos os checks obrigatorios de validacao.")

    security = policy.get("security", {})
    for field in ["forbid_plaintext_secrets", "forbid_secret_files_in_git"]:
        if security.get(field) is not True:
            errors.append(f"Politica do dominio deve manter security.{field}=true.")

    approved_secret_stores = set(security.get("approved_secret_stores", []))
    if approved_secret_stores != {"github_actions_secrets", "protected_ci_cd_variables", "external_vault"}:
        errors.append("Politica do dominio deve manter os armazenamentos de segredo aprovados.")

    required_docs = set(policy.get("required_docs", []))
    if required_docs != REQUIRED_DOCS:
        errors.append("Politica do dominio deve manter a lista oficial de documentacao obrigatoria.")
    else:
        for relative in required_docs:
            if not (root / relative).is_file():
                errors.append(f"Documento obrigatorio da politica ausente no repositorio: {relative}")

    terraform_dns_types_line = (
        root / "infra" / "terraform" / "variables.tf"
    ).read_text(encoding="utf-8")
    if "A\", \"AAAA\", \"CNAME\", \"TXT\", \"MX\", \"NS\", \"CAA\", \"SRV\", \"PTR" not in terraform_dns_types_line:
        errors.append("Terraform deve manter suporte aos tipos DNS obrigatorios na validacao de dns_records.")

    return errors
