# All-in-One

SuperApp modular com identidade unica para consumidores, empresas, riders,
prestadores, mobilidade, saude e operacoes empresariais. Este repositorio
inicializa o baseline arquitetural e executavel definido no documento mestre:
microservicos FastAPI, contratos OpenAPI, persistencia PostgreSQL/MongoDB,
eventos, controles de seguranca, infraestrutura e gates de CI.

## Baseline implementado

- Seis superficies de aplicacao em `apps/`, todas dependentes do All-in-One ID.
- Vinte e quatro microservicos em `modules/`, cada um com runtime funcional,
  contrato, OpenAPI, Dockerfile, documentacao de dominio e quatro testes.
- PostgreSQL com 29 schemas, identidade, business/KYB, RBAC/ABAC, wallet,
  ledger, escrow, operacoes e verticais; ledger/auditoria sao append-only.
- MongoDB validado para memoria IA consentida, social, metricas de influencer
  e telemetria.
- RabbitMQ como contrato inicial de eventos; Redis para suporte a cache/rate
  limit; Docker Compose e manifests Kubernetes.
- CI para scaffold, contratos, testes, banco, OpenAPI, seguranca e automacao
  controlada de branches.

## Identidade e integridade

`identity.users.id` e o vinculo central dos recursos de dominio. Wallets,
cartoes NFC/LED, perfis Rider e escrows usam foreign keys compostas para
impedir que uma operacao referencie a wallet de outro usuario. Recursos
financeiros e logs de auditoria rejeitam `UPDATE` e `DELETE`.

## Execucao local

```bash
python -m pip install -r requirements-dev.txt
python scripts/scaffold_modules.py --check
python scripts/validate_repository.py
python -m pytest --import-mode=importlib
docker compose -f infra/docker/docker-compose.yml up --build
```

Exemplo isolado:

```bash
cd modules/identity
pip install -r requirements.txt
uvicorn main:app --port 8000
```

## Organizacao

| Caminho | Conteudo |
| --- | --- |
| `apps/` | Contratos das seis experiencias cliente |
| `modules/` | Microservicos funcionais e testes |
| `contracts/` | Contratos de dominio espelhados e versionaveis |
| `database/` | Migracoes PostgreSQL e validacoes MongoDB |
| `docs/` | Arquitetura, seguranca, eventos, operacao e roadmap |
| `infra/` | Docker, Kubernetes e Terraform inicial |
| `.github/workflows/` | Gates e automacoes de entrega |

## Estado

O baseline torna todos os modulos inicializaveis e testaveis. Integracoes
reguladas ou externas (Pix/cartoes, fiscal oficial, biometria, assinatura,
OCR, IA produtiva, hospitais, GPS de concessionarias) permanecem bloqueadas
para producao ate credenciais, homologacao, DPIA/LGPD e testes E2E
documentados em [docs/ROADMAP.md](docs/ROADMAP.md).
