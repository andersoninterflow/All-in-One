from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_MATRIX = ROOT / "config" / "integrations" / "provider_matrix.json"
OUTPUT = ROOT / "config" / "autonomy" / "paid_services_pending.json"

COST_HINTS = {
    "identity_kyc_kyb": "Variavel por validacao (normalmente por consulta/documento)",
    "finance_pix_psp": "Variavel por transacao (taxa por pagamento, saque ou split)",
    "fiscal_nfse_nfe": "Variavel por documento fiscal emitido",
    "jobs_ctps_official": "Sob consulta com integrador autorizado",
    "maps_routing_tracking": "Variavel por rota, geocoding e tracking",
    "health_telemedicine_prescription": "Variavel por assinatura/consulta/documento",
    "api_hub_oauth_webhooks": "Plano por tenant ou por MAU/requisicao",
    "stock_supplier_catalog": "Sob contrato com fornecedor/hub parceiro",
    "ai_agent_superdesign": "Variavel por token/chamada de modelo"
}

PRIORITY_HINTS = {
    "finance_pix_psp": "alta",
    "identity_kyc_kyb": "alta",
    "api_hub_oauth_webhooks": "alta",
    "maps_routing_tracking": "media",
    "fiscal_nfse_nfe": "media",
    "jobs_ctps_official": "media",
    "health_telemedicine_prescription": "media",
    "stock_supplier_catalog": "baixa",
    "ai_agent_superdesign": "media"
}


def _recommendation(integration: dict) -> str:
    return (
        "Manter adapter sandbox local ativo, feature flag desligada por padrao e "
        "habilitar em ambiente pago apenas apos homologacao, previsibilidade de custo e compliance."
    )


def _impact(integration: dict) -> str:
    return (
        "Sem contratacao, o projeto segue funcional em modo sandbox/local; "
        "a limitacao fica na homologacao/producao desta capacidade."
    )


def build_items(matrix: dict) -> list[dict]:
    items: list[dict] = []
    for integration in matrix.get("integrations", []):
        key = integration["key"]
        purpose = integration.get("capability", "capacidade externa")
        providers = integration.get("primary_candidates", [])
        service_name = providers[0] if providers else key
        item = {
            "integration_key": key,
            "nome_servico": service_name,
            "finalidade": purpose,
            "custo_estimado": COST_HINTS.get(key, "Sob consulta com fornecedor"),
            "beneficios": "Permite evolucao de sandbox para homologacao/producao com fornecedor real.",
            "impacto_da_nao_utilizacao": _impact(integration),
            "prioridade": PRIORITY_HINTS.get(key, "media"),
            "recomendacao_tecnica": _recommendation(integration),
            "status": "Status: Implementacao futura (Servico Pago)",
            "alternativa_gratuita_ou_local": integration.get("zero_cost_entry", "Adapter local sandbox"),
        }
        items.append(item)
    return items


def main() -> int:
    matrix = json.loads(PROVIDER_MATRIX.read_text(encoding="utf-8"))
    payload = {
        "version": "2026-07-22",
        "language": "pt-BR",
        "generated_at": datetime.now(UTC).isoformat(),
        "source": "config/integrations/provider_matrix.json",
        "items": build_items(matrix),
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Pendencias de servicos pagos sincronizadas: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
