from __future__ import annotations
import os
from fastapi import FastAPI, Header, HTTPException, Depends
from typing import Any, Optional
from pydantic import BaseModel
from modules.shared.erp_postgres_store import ErpPostgresStore
from modules.shared.runtime import get_erp_store
from modules.shared.integration_sandbox import local_fiscal_document_simulator

app = FastAPI(title="All-in-One ERP API")

class InvoiceItemSchema(BaseModel):
    description: str
    quantity: float = 1.0
    unit_price_brl: str
    total_price_brl: str
    tax_amount_brl: str = "0.00"

class BillingRequest(BaseModel):
    document_number: Optional[str] = None
    amount_brl: str
    tax_amount_brl: str
    document_type: str = "nfe"
    items: list[InvoiceItemSchema]
    pepitas_reward: Optional[int] = None  # Gamificação Valley: 1, 10, 100

class CancelRequest(BaseModel):
    reason: str

@app.get("/health")
def health():
    return {"status": "ok", "module": "erp"}

@app.get("/erp/billing/{document_id}")
async def get_billing(
    document_id: str,
    store: ErpPostgresStore = Depends(get_erp_store)
):
    doc = store.get_billing_detail(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento fiscal não encontrado.")

    # O status fiscal e autorizações já estão contidos no payload ou metadados do documento
    return doc

@app.post("/erp/billing")
async def create_billing(
    request: BillingRequest,
    x_actor_user_id: str = Header(...),
    x_actor_company_id: str = Header(...),
    x_idempotency_key: Optional[str] = Header(None),
    store: ErpPostgresStore = Depends(get_erp_store)
):
    try:
        payload = request.dict(exclude={"items"})
        items = [item.dict() for item in request.items]

        # Validação de Gamificação Valley
        if request.pepitas_reward and request.pepitas_reward not in {1, 10, 100}:
            raise HTTPException(status_code=422, detail="Gamificação inválida. Escolha 1, 10 ou 100 Pepitas.")

        # Persistência local atômica
        doc = store.create_billing_document(
            user_id=x_actor_user_id,
            company_id=x_actor_company_id,
            payload=payload,
            items=items,
            idempotency_key=x_idempotency_key
        )

        # Conexão com Sandbox Fiscal (Fase 5)
        if os.getenv("ALL_IN_ONE_ERP_FISCAL_SANDBOX", "true").lower() == "true":
            sandbox_result = local_fiscal_document_simulator(
                document_id=doc["id"],
                amount_brl=doc["payload"]["amount_brl"],
                company_id=x_actor_company_id
            )
            doc["fiscal_authorization"] = sandbox_result

        return doc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/erp/billing/{document_id}/cancel")
async def cancel_billing(
    document_id: str,
    request: CancelRequest,
    x_actor_user_id: str = Header(...),
    store: ErpPostgresStore = Depends(get_erp_store)
):
    try:
        doc = store.cancel_billing_document(
            document_id=document_id,
            user_id=x_actor_user_id,
            reason=request.reason
        )

        # Conexão com Sandbox Fiscal (Fase 5) - Cancelamento
        if os.getenv("ALL_IN_ONE_ERP_FISCAL_SANDBOX", "true").lower() == "true":
            sandbox_result = local_fiscal_document_simulator(
                document_id=document_id,
                action="cancel",
                reason=request.reason,
                company_id=doc.get("company_id") or doc.get("entity_id")
            )
            doc["fiscal_cancellation"] = sandbox_result

        return doc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))