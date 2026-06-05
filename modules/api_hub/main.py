import os
import sys
import httpx
import hashlib
import hmac
from pathlib import Path
from fastapi import Request, HTTPException, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from starlette.background import BackgroundTask
import time

try:
    import redis.asyncio as redis
except ModuleNotFoundError:  # Ambiente de teste local sem extras do gateway.
    redis = None

try:
    import jwt
except ModuleNotFoundError:  # Rotas sem JWT continuam carregando em testes locais.
    jwt = None

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shared.runtime import create_module_app
from shared.security import Actor

app = create_module_app("api_hub")

# Configurações
MODULES = [
    "ai_core", "bi", "bpm", "business", "crm", "delivery", "document", "erp",
    "finance", "health", "hr", "identity", "jobs", "legal", "marketplace",
    "mobility", "permissions", "property", "riders", "services", "stock",
    "tms", "vision", "wms"
]

SERVICES = {
    mod: os.getenv(f"{mod.upper()}_SERVICE_URL", f"http://{mod}:8000")
    for mod in MODULES
}
JWT_SECRET = os.getenv("ALL_IN_ONE_JWT_SECRET", "local-secret-key-change-in-production")
REDIS_URL = os.getenv("ALL_IN_ONE_REDIS_URL", "redis://redis:6379/0")
WEBHOOK_SECRET = os.getenv("ALL_IN_ONE_WEBHOOK_SECRET", "local-webhook-secret-change-in-production")

# Clientes
client = httpx.AsyncClient()
redis_client = redis.from_url(REDIS_URL, decode_responses=True) if redis else None

def _configured_api_keys() -> dict[str, dict[str, object]]:
    """Parse API keys from ALL_IN_ONE_API_KEYS.

    Format: key:client_id:scope_a,scope_b;other:client:*
    """
    raw = os.getenv("ALL_IN_ONE_API_KEYS", "local-api-key:local-client:*")
    configured: dict[str, dict[str, object]] = {}
    for chunk in raw.split(";"):
        if not chunk.strip():
            continue
        parts = chunk.split(":", 2)
        if len(parts) != 3:
            continue
        key, client_id, scopes = (part.strip() for part in parts)
        if not key or not client_id:
            continue
        configured[key] = {
            "client_id": client_id,
            "scopes": {scope.strip() for scope in scopes.split(",") if scope.strip()},
        }
    return configured


def _verify_webhook_signature(body: bytes, signature: str | None) -> bool:
    if not signature or not signature.startswith("sha256="):
        return False
    digest = hmac.new(WEBHOOK_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, f"sha256={digest}")

async def rate_limiter(request: Request):
    """Rate limiting por IP usando Redis."""
    if redis_client is None:
        return None
    ip = request.client.host
    key = f"rate_limit:{ip}"
    limit = 100 # requisições
    window = 60 # segundos
    
    current = await redis_client.get(key)
    if current and int(current) >= limit:
        raise HTTPException(status_code=429, detail="Too many requests. Tente novamente em um minuto.")
    
    pipe = redis_client.pipeline()
    await pipe.incr(key).expire(key, window).execute()


async def validate_api_key_edge(request: Request):
    """Valida API key para clientes de integracao e retorna contexto minimo."""
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="API key ausente.")

    key_info = _configured_api_keys().get(api_key)
    if key_info is None:
        raise HTTPException(status_code=401, detail="API key invalida.")

    scopes = key_info["scopes"]
    if "*" not in scopes and "gateway:read" not in scopes:
        raise HTTPException(status_code=403, detail="API key sem escopo gateway:read.")
    return key_info

async def validate_jwt_edge(request: Request):
    """Valida o JWT na borda para rotas protegidas."""
    if request.url.path.startswith(("/auth/", "/registrations", "/health", "/gateway")):
        return None
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou invalido.")
    
    token = auth_header.split(" ")[1]
    if jwt is None:
        raise HTTPException(status_code=503, detail="Validador JWT indisponivel.")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido.")

async def proxy_request(service_url: str, request: Request, actor_payload: dict | None = None):
    """Proxy com injeção de contexto de ator."""
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    target_url = f"{service_url}{url.path}"
    if url.query:
        target_url += f"?{url.query}"

    headers = dict(request.headers)
    headers.pop("host", None)
    
    # Injeta o X-Actor-User-Id se o JWT foi validado na borda
    if actor_payload:
        headers["X-Actor-User-Id"] = actor_payload.get("sub")

    req = client.build_request(
        method=request.method,
        url=target_url,
        headers=headers,
        content=await request.body()
    )
    
    try:
        resp = await client.send(req, stream=True)
        return StreamingResponse(
            resp.aiter_raw(),
            status_code=resp.status_code,
            headers=dict(resp.headers),
            background=BackgroundTask(resp.aclose)
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Erro de comunicacao com microservico: {exc}")

# Roteamento Protegido Dinâmico para Módulos
def create_proxy_route(service_name: str):
    @app.api_route(
        f"/{service_name}/{{path:path}}", 
        methods=["GET", "POST", "PATCH", "DELETE", "PUT"],
        dependencies=[Depends(rate_limiter)]
    )
    async def route_proxy(path: str, request: Request, actor=Depends(validate_jwt_edge)):
        return await proxy_request(SERVICES[service_name], request, actor)

for service in SERVICES.keys():
    if service != "identity":
        create_proxy_route(service)

# Roteamento Aberto (Apenas Rate Limit) - Identity
@app.api_route(
    "/identity/{path:path}", 
    methods=["GET", "POST", "PATCH", "DELETE", "PUT"],
    dependencies=[Depends(rate_limiter)]
)
async def identity_proxy(path: str, request: Request, actor=Depends(validate_jwt_edge)):
    return await proxy_request(SERVICES["identity"], request, actor)

@app.post("/auth/{path:path}", dependencies=[Depends(rate_limiter)])
async def auth_proxy(path: str, request: Request):
    return await proxy_request(SERVICES["identity"], request)

@app.post("/registrations", dependencies=[Depends(rate_limiter)])
async def registrations_proxy(request: Request):
    return await proxy_request(SERVICES["identity"], request)

import asyncio

@app.get("/gateway/catalog/offers", dependencies=[Depends(rate_limiter)])
async def aggregate_catalog_offers(limit: int = 50, offset: int = 0):
    """Agregação Multi-Serviço das ofertas vivas do Valley Marketplace"""
    async def fetch_module(mod_name):
        try:
            url = f"{SERVICES[mod_name]}/catalog_offers?limit={limit}"
            resp = await client.get(url, timeout=2.0)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, dict) and "data" in data:
                    for item in data["data"]: item["_source_module"] = mod_name
                    return data["data"]
                elif isinstance(data, list):
                    for item in data: item["_source_module"] = mod_name
                    return data
            return []
        except Exception:
            return []

    target_modules = ["business", "marketplace", "services", "health", "property", "jobs", "mobility", "delivery", "tms"]
    tasks = [fetch_module(m) for m in target_modules]
    results = await asyncio.gather(*tasks)
    
    aggregated = []
    for r in results:
        aggregated.extend(r)
        
    return {"data": aggregated[:limit], "total": len(aggregated)}

@app.get("/gateway/telemetry/outbox")
async def outbox_telemetry(limit: int = 100):
    """Monitoramento unificado de Outbox Parada e Eventos em Backoff"""
    from modules.shared.outbox_dispatcher import OutboxDispatcher, OutboxSettings
    
    def fetch_metrics():
        settings = OutboxSettings.from_environment()
        dispatcher = OutboxDispatcher(settings)
        try:
            return dispatcher.collect_metrics()
        finally:
            dispatcher.close()

    try:
        metrics = await asyncio.to_thread(fetch_metrics)
        return {
            "status": "healthy",
            "pending": metrics.pending,
            "due": metrics.due,
            "published": metrics.published,
            "failed_retryable": metrics.failed_retryable,
            "max_retry_count": metrics.max_retry_count,
            "oldest_pending_age_seconds": metrics.oldest_pending_age_seconds,
        }
    except Exception as exc:
        return {
            "status": "unhealthy",
            "error": str(exc),
            "pending": 0,
            "due": 0,
            "published": 0,
            "failed_retryable": 0,
            "max_retry_count": 0,
            "oldest_pending_age_seconds": 0,
        }


@app.get("/gateway/status")
async def gateway_status():
    return {
        "service": "API Hub Gateway",
        "status": "active",
        "security": "JWT_EDGE_VALIDATION_ENABLED",
        "rate_limit": "REDIS_IP_BASED_ENABLED",
        "routes": list(SERVICES.keys())
    }


@app.get("/gateway/api-key/check", dependencies=[Depends(rate_limiter)])
async def gateway_api_key_check(key_info: dict = Depends(validate_api_key_edge)):
    return {
        "status": "valid",
        "client_id": key_info["client_id"],
        "scopes": sorted(key_info["scopes"]),
    }


@app.post("/gateway/webhooks/verify")
async def gateway_webhook_verify(request: Request):
    body = await request.body()
    signature = request.headers.get("X-All-In-One-Signature")
    if not _verify_webhook_signature(body, signature):
        raise HTTPException(status_code=401, detail="Assinatura de webhook invalida.")
    return {"status": "valid", "algorithm": "hmac-sha256"}
