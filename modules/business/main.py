import os
import sys
from pathlib import Path
from typing import Literal, Any
from uuid import UUID

from fastapi import Depends, HTTPException
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shared.runtime import create_module_app
from shared.security import Actor, extract_actor
from shared.business_postgres_store import BusinessPostgresStore

app = create_module_app("business")

STORE = BusinessPostgresStore(os.getenv("ALL_IN_ONE_DB_DSN", "postgresql://postgres:postgres@localhost:5432/allinone"))

class CatalogOfferPayload(BaseModel):
    company_id: UUID | None = None
    source_module: str = Field(min_length=2, max_length=60)
    source_entity_id: UUID | None = None
    offer_type: Literal["product", "service", "appointment", "job", "course", "legal", "health", "property", "delivery", "finance", "document", "government"]
    title: str = Field(min_length=3, max_length=240)
    short_description: str | None = None
    category_id: UUID | None = None
    business_category: str | None = None
    business_type: str | None = None
    activity_branch: str | None = None
    price_type: Literal["fixed", "variable", "quote", "free", "subscription"] = "fixed"
    price_amount: float | None = None
    currency: str = "BRL"
    location_type: Literal["local", "regional", "national", "online", "hybrid"] = "online"
    availability_type: Literal["stock", "schedule", "quote", "immediate", "manual"] = "immediate"
    trust_badges: list[str] = []
    media: list[str] = []
    payment_methods: list[str] = []
    fulfillment_policy: dict[str, Any] = {}
    cancellation_policy: dict[str, Any] = {}
    refund_policy: dict[str, Any] = {}
    idempotency_key: str | None = None

class PublishRequest(BaseModel):
    status: Literal["draft", "pending_review", "published", "paused", "rejected", "archived"]

@app.post("/valley/catalog/offers")
def create_offer(
    payload: CatalogOfferPayload,
    actor: Actor = Depends(extract_actor)
):
    try:
        offer = STORE.create(
            resource_type="catalog_offers",
            user_id=actor.user_id,
            entity_id=str(payload.company_id) if payload.company_id else None,
            status="draft",
            payload=payload.model_dump(exclude={"idempotency_key"}),
            actor=actor.user_id,
            unique_fields=(),
            event="business.offer.created",
            idempotency_key=payload.idempotency_key
        )
        return {"id": offer["id"], "status": "draft"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/valley/catalog/offers/{offer_id}/status")
def update_offer_status(
    offer_id: str,
    req: PublishRequest,
    actor: Actor = Depends(extract_actor)
):
    offer = STORE.get("catalog_offers", offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    if str(offer["user_id"]) != actor.user_id and not actor.is_system:
        raise HTTPException(status_code=403, detail="Forbidden")

    updated = STORE.update(
        item=offer,
        payload=offer["payload"],
        status=req.status,
        actor=actor.user_id,
        action="update_status",
        event="business.offer.updated"
    )
    if req.status == "published":
        STORE.update(
            item=updated,
            payload=updated["payload"],
            status="published",
            actor=actor.user_id,
            action="publish_offer",
            event="marketplace.offer.published"
        )
        
    return {"id": updated["id"], "status": updated["status"]}

@app.get("/valley/catalog/offers")
def list_offers(
    user_id: str | None = None,
    status: str | None = None
):
    offers = STORE.list("catalog_offers", user_id=user_id)
    if status:
        offers = [o for o in offers if o["status"] == status]
        
    formatted_offers = []
    for o in offers:
        payload = o.get("payload", {})
        formatted_offers.append({
            "offer_id": o["id"],
            "title": payload.get("title", "Sem titulo"),
            "short_description": payload.get("short_description", ""),
            "price_amount": payload.get("price_amount"),
            "price_type": payload.get("price_type", "fixed"),
            "offer_type": payload.get("offer_type", "product"),
            "source_module": payload.get("source_module", "business"),
            "consumer_category": payload.get("business_category", "Outros"),
            "consumer_action": "buy" if payload.get("offer_type") == "product" else "book",
            "primary_action_label": "Comprar" if payload.get("offer_type") == "product" else "Agendar",
            "verified_seller": True,
            "provider_label": "Parceiro Verificado",
            "region_label": payload.get("location_type", "online")
        })

    return {
        "data": formatted_offers,
        "total": len(formatted_offers),
        "partial": False,
        "facets": {
            "company_types": [],
            "company_categories": [],
            "business_activities": []
        }
    }
