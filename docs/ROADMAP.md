# Roadmap

## Entregue: baseline 0.1.0

- Estrutura dos apps e de 24 dominios.
- Runtimes FastAPI funcionais com endpoints minimos e testes.
- PostgreSQL/MongoDB, identidade, RBAC, wallet, escrow, auditoria e eventos.
- Docker, Kubernetes inicial, CI/CD e documentacao operacional.

## Proximos incrementos bloqueadores para beta

1. Implementar persistencia real dos endpoints por modulo com migrations e
   repositorios transacionais.
2. Integrar Identity/API Hub com OIDC, MFA, KMS, KYC/KYB e liveness aprovados.
3. Integrar payment provider, fiscal brasileiro e conciliacao em sandbox.
4. Implementar jornadas web/mobile dos seis apps e testes E2E.
5. Entregar moderacao OCR/IA, storage privado, notificacoes e observabilidade.

## Bloqueadores para producao

1. Homologacao regulatoria, LGPD/DPIA, politicas de retencao e consentimento.
2. Pentest, carga, disaster recovery, backup/restore e resposta a incidente.
3. Homologacao de parceiros financeiros, fiscais, transporte e saude.
