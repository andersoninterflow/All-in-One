from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "config" / "module_catalog.json"

OFFER_TYPES = {"food", "product", "service"}
OFFER_TYPE_ALIASES = {
    "alimento": "food",
    "comida": "food",
    "food": "food",
    "produto": "product",
    "product": "product",
    "servico": "service",
    "serviço": "service",
    "service": "service",
}
LOCAL_AREAS = {"local", "regional"}
GLOBAL_AREAS = {"online", "national"}

CATEGORY_DEFINITIONS: dict[str, dict[str, Any]] = {
    "Comida e Mercado": {
        "offer_types": ("food", "product"),
        "modules": ("delivery", "marketplace", "stock"),
        "keywords": ("food", "alimento", "comida", "restaurante", "marmita", "mercado", "delivery"),
    },
    "Compras e Produtos": {
        "offer_types": ("product",),
        "modules": ("marketplace", "stock"),
        "keywords": ("produto", "catalogo", "loja", "assinatura", "curso", "digital"),
    },
    "Saude e Bem-estar": {
        "offer_types": ("service",),
        "modules": ("health", "services"),
        "keywords": ("saude", "medico", "medicina", "psicologo", "dentista", "consulta", "telemedicina"),
    },
    "Casa, Reparos e Imoveis": {
        "offer_types": ("service", "product"),
        "modules": ("services", "property", "marketplace"),
        "keywords": ("reparo", "eletricista", "pedreiro", "marceneiro", "imovel", "manutencao", "casa"),
    },
    "Mobilidade, Entregas e Logistica": {
        "offer_types": ("service",),
        "modules": ("mobility", "delivery", "riders", "tms"),
        "keywords": ("corrida", "entrega", "frete", "transporte", "logistica", "rider"),
    },
    "Negocios e Profissionais": {
        "offer_types": ("service",),
        "modules": ("legal", "erp", "crm", "bi", "bpm", "document", "hr", "jobs"),
        "keywords": ("advogado", "contador", "recrutamento", "consultoria", "documento", "profissional"),
    },
    "Beneficios, Wallet e Recompensas": {
        "offer_types": ("service", "product"),
        "modules": ("finance", "marketplace", "stock"),
        "keywords": ("pepitas", "gold", "wallet", "desconto", "beneficio", "fidelidade", "recompensa"),
    },
    "Tecnologia, Seguranca e IA": {
        "offer_types": ("service",),
        "modules": ("vision", "ai_core", "api_hub", "permissions"),
        "keywords": ("camera", "ia", "api", "integracao", "permissao", "seguranca", "automacao"),
    },
}

RESOURCE_OFFER_TYPES = {
    "catalog_products": "product",
    "products": "product",
    "providers": "service",
    "service_contracts": "service",
    "delivery_requests": "food",
    "rides": "service",
    "tickets": "service",
    "job_postings": "service",
    "properties": "service",
    "appointments": "service",
    "valley_gold_ledger_entries": "service",
    "discount_quotes": "product",
}

PUBLIC_RESOURCE_TYPES = {
    "marketplace": ("products",),
    "stock": ("catalog_products", "discount_quotes"),
    "services": ("providers", "service_contracts"),
    "health": ("appointments",),
    "delivery": ("delivery_requests",),
    "mobility": ("rides", "tickets"),
    "jobs": ("job_postings",),
    "property": ("properties",),
    "finance": ("valley_gold_ledger_entries",),
}


def load_module_catalog() -> dict[str, Any]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def valley_categories() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "offer_types": list(definition["offer_types"]),
            "source_modules": list(definition["modules"]),
            "keywords": list(definition["keywords"]),
        }
        for name, definition in CATEGORY_DEFINITIONS.items()
    ]


def valley_modules() -> list[dict[str, Any]]:
    catalog = load_module_catalog()
    return [
        {
            "source_module": module["slug"],
            "technical_title": module["title"],
            "consumer_category": infer_category(module["slug"], "records", module["title"], module["description"]),
            "consumer_title": friendly_module_title(module["slug"], module["title"]),
            "description": module["description"],
            "availability_status": "coming_soon",
        }
        for module in catalog["modules"]
    ]


def build_valley_offers(module_name: str, store: Any | None = None) -> list[dict[str, Any]]:
    offers = module_fallback_offers()
    if store is None:
        return offers
    for resource_type in PUBLIC_RESOURCE_TYPES.get(module_name, ()):
        try:
            rows = store.list(resource_type, None)
        except Exception:
            continue
        for row in rows:
            offer = offer_from_resource(module_name, resource_type, row)
            if offer:
                offers.append(offer)
    return deduplicate_offers(offers)


def module_fallback_offers() -> list[dict[str, Any]]:
    catalog = load_module_catalog()
    return [
        {
            "offer_id": f"module:{module['slug']}",
            "offer_type": infer_offer_type(module["slug"], "records", module["title"], module["description"]),
            "consumer_category": infer_category(module["slug"], "records", module["title"], module["description"]),
            "title": friendly_module_title(module["slug"], module["title"]),
            "description": module["description"],
            "source_module": module["slug"],
            "source_resource_type": "module",
            "availability_status": "coming_soon",
            "price_brl": None,
            "benefits": [],
            "rewards": [],
            "service_origin": None,
            "service_radius_km": None,
            "distance_km": None,
            "region_label": "Disponibilidade em expansao",
            "service_area": "national",
            "consumer_action": "coming_soon",
            "media": [],
        }
        for module in catalog["modules"]
    ]


def offer_from_resource(module_name: str, resource_type: str, row: dict[str, Any]) -> dict[str, Any] | None:
    payload = row.get("payload") or {}
    title = first_text(
        payload,
        ("public_title", "name", "title", "headline", "category", "service_type", "route_code", "property_type"),
        fallback=friendly_module_title(module_name, module_name),
    )
    description = first_text(payload, ("public_description", "description", "summary"), fallback=title)
    offer_type = normalize_offer_type(payload.get("offer_type")) or infer_offer_type(module_name, resource_type, title, description)
    consumer_category = str(payload.get("consumer_category") or infer_category(module_name, resource_type, title, description))
    service_area = str(payload.get("service_area") or default_service_area(module_name, resource_type)).casefold()
    origin = public_origin(payload)
    radius = number_or_none(payload.get("service_radius_km"))
    return {
        "offer_id": f"{module_name}:{resource_type}:{row['id']}",
        "offer_type": offer_type,
        "consumer_category": consumer_category,
        "title": title,
        "description": description,
        "source_module": module_name,
        "source_resource_type": resource_type,
        "availability_status": availability_for(row.get("status")),
        "price_brl": price_for(payload),
        "benefits": list_or_empty(payload.get("benefits")),
        "rewards": list_or_empty(payload.get("rewards")),
        "service_origin": origin,
        "service_radius_km": radius,
        "distance_km": None,
        "region_label": str(payload.get("region_label") or default_region_label(service_area)),
        "service_area": service_area,
        "consumer_action": consumer_action_for(module_name, resource_type),
        "media": list_or_empty(payload.get("media")),
    }


def search_valley_offers(
    offers: list[dict[str, Any]],
    *,
    q: str | None = None,
    category: str | None = None,
    offer_type: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
) -> list[dict[str, Any]]:
    normalized_type = normalize_offer_type(offer_type) if offer_type else None
    terms = (q or "").strip().casefold()
    selected_category = (category or "").strip().casefold()
    results: list[dict[str, Any]] = []
    for offer in offers:
        if normalized_type and offer["offer_type"] != normalized_type:
            continue
        if selected_category and selected_category not in str(offer["consumer_category"]).casefold():
            continue
        if terms:
            material = " ".join(
                str(offer.get(key) or "")
                for key in ("title", "description", "consumer_category", "source_module", "source_resource_type")
            ).casefold()
            if terms not in material:
                continue
        localized = with_distance(offer, lat, lng)
        if lat is not None and lng is not None and not visible_for_location(localized):
            continue
        results.append(localized)
    return sorted(results, key=offer_sort_key)


def with_distance(offer: dict[str, Any], lat: float | None, lng: float | None) -> dict[str, Any]:
    copy = dict(offer)
    if lat is None or lng is None or not offer.get("service_origin"):
        return copy
    origin = offer["service_origin"]
    distance = haversine_km(lat, lng, float(origin["latitude"]), float(origin["longitude"]))
    copy["distance_km"] = round(distance, 3)
    radius = offer.get("service_radius_km")
    if offer.get("service_area") in LOCAL_AREAS and radius is not None and distance > float(radius):
        copy["availability_status"] = "unavailable_for_location"
    return copy


def visible_for_location(offer: dict[str, Any]) -> bool:
    if offer.get("availability_status") == "coming_soon":
        return True
    if offer.get("service_area") in GLOBAL_AREAS:
        return True
    if offer.get("service_area") not in LOCAL_AREAS:
        return True
    if offer.get("availability_status") == "unavailable_for_location":
        return False
    return offer.get("distance_km") is not None and offer.get("service_radius_km") is not None


def offer_sort_key(offer: dict[str, Any]) -> tuple[int, float, str]:
    area = offer.get("service_area")
    status = offer.get("availability_status")
    if status in {"available", "limited"} and offer.get("distance_km") is not None:
        tier = 0
    elif area in GLOBAL_AREAS:
        tier = 1
    elif status == "coming_soon":
        tier = 3
    else:
        tier = 2
    distance = float(offer["distance_km"]) if offer.get("distance_km") is not None else 999999.0
    return (tier, distance, str(offer.get("title", "")))


def haversine_km(lat_a: float, lng_a: float, lat_b: float, lng_b: float) -> float:
    earth_km = 6371.0
    delta_lat = math.radians(lat_b - lat_a)
    delta_lng = math.radians(lng_b - lng_a)
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(math.radians(lat_a)) * math.cos(math.radians(lat_b)) * math.sin(delta_lng / 2) ** 2
    )
    return earth_km * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def infer_offer_type(module_name: str, resource_type: str, title: str, description: str) -> str:
    material = f"{module_name} {resource_type} {title} {description}".casefold()
    if any(keyword in material for keyword in CATEGORY_DEFINITIONS["Comida e Mercado"]["keywords"]):
        return "food"
    if RESOURCE_OFFER_TYPES.get(resource_type):
        return RESOURCE_OFFER_TYPES[resource_type]
    if module_name in {"marketplace", "stock"}:
        return "product"
    return "service"


def infer_category(module_name: str, resource_type: str, title: str, description: str) -> str:
    material = f"{module_name} {resource_type} {title} {description}".casefold()
    for name, definition in CATEGORY_DEFINITIONS.items():
        if module_name in definition["modules"]:
            return name
        if any(keyword in material for keyword in definition["keywords"]):
            return name
    return "Negocios e Profissionais"


def normalize_offer_type(value: Any) -> str | None:
    if value is None:
        return None
    return OFFER_TYPE_ALIASES.get(str(value).strip().casefold())


def public_origin(payload: dict[str, Any]) -> dict[str, float] | None:
    origin = payload.get("service_origin")
    if isinstance(origin, dict):
        latitude = number_or_none(origin.get("latitude"))
        longitude = number_or_none(origin.get("longitude"))
    else:
        latitude = number_or_none(payload.get("latitude"))
        longitude = number_or_none(payload.get("longitude"))
    if latitude is None or longitude is None:
        return None
    return {"latitude": latitude, "longitude": longitude}


def number_or_none(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def price_for(payload: dict[str, Any]) -> str | None:
    for key in ("price_brl", "list_price_brl", "visit_price_brl", "fare_brl", "amount_brl", "contracted_price_brl"):
        if payload.get(key) not in (None, ""):
            return str(payload[key])
    return None


def first_text(payload: dict[str, Any], keys: tuple[str, ...], fallback: str) -> str:
    for key in keys:
        value = payload.get(key)
        if value not in (None, ""):
            return str(value)
    return fallback


def list_or_empty(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return []


def availability_for(status: Any) -> str:
    normalized = str(status or "").casefold()
    if normalized in {"active", "approved", "published", "available", "posted", "quoted", "completed"}:
        return "available"
    if normalized in {"draft", "pending_validation", "pending_review", "created", "requested"}:
        return "limited"
    if normalized in {"cancelled", "rejected", "blocked", "suspended", "archived"}:
        return "unavailable"
    return "limited"


def consumer_action_for(module_name: str, resource_type: str) -> str:
    if module_name in {"marketplace", "stock"} and resource_type in {"products", "catalog_products", "discount_quotes"}:
        return "buy"
    if module_name in {"health", "services"}:
        return "book" if resource_type == "appointments" else "hire"
    if module_name == "jobs":
        return "apply"
    if module_name in {"delivery", "mobility", "property"}:
        return "request"
    return "view"


def default_service_area(module_name: str, resource_type: str) -> str:
    if module_name in {"stock", "finance", "api_hub", "ai_core", "document", "bi"}:
        return "online"
    if resource_type in {"job_postings", "catalog_products", "discount_quotes"}:
        return "national"
    return "local"


def default_region_label(service_area: str) -> str:
    if service_area == "online":
        return "Online"
    if service_area == "national":
        return "Brasil"
    return "Regiao cadastrada"


def friendly_module_title(slug: str, title: str) -> str:
    overrides = {
        "identity": "Cadastro e acesso",
        "business": "Empresas participantes",
        "permissions": "Perfis e permissoes",
        "finance": "Wallet, Gold e Pepitas",
        "marketplace": "Lojas e produtos locais",
        "stock": "Produtos com beneficios",
        "delivery": "Comida, entregas e coletas",
        "riders": "Entregadores e motoristas",
        "services": "Servicos profissionais",
        "mobility": "Corridas e transporte",
        "jobs": "Vagas e oportunidades",
        "erp": "Gestao e contabilidade",
        "wms": "Estoque e armazem",
        "tms": "Fretes e logistica",
        "crm": "Atendimento e relacionamento",
        "bpm": "Processos e automacao",
        "document": "Documentos e assinaturas",
        "hr": "Pessoas, cursos e RH",
        "health": "Saude e bem-estar",
        "vision": "Cameras e seguranca",
        "legal": "Advocacia e juridico",
        "property": "Imoveis e manutencao",
        "bi": "Indicadores e relatorios",
        "ai_core": "Inteligencia artificial",
        "api_hub": "Integracoes digitais",
    }
    return overrides.get(slug, title)


def deduplicate_offers(offers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result = []
    for offer in offers:
        if offer["offer_id"] in seen:
            continue
        seen.add(offer["offer_id"])
        result.append(offer)
    return result
