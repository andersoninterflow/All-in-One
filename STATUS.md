# Status Operacional

## STATUS OPERACIONAL - 2026-05-25 Baseline inicial

### Concluido neste ciclo

- Repositorio inicializado a partir do documento mestre All-in-One.
- Catalogo de seis apps e 24 microservicos com contratos e runtimes FastAPI.
- Migracoes PostgreSQL e validadores MongoDB para os dominios centrais.
- Controles de identidade unica, aprovacao manual, escrow, anti-burla e audit.
- Infraestrutura e workflows de CI/CD definidos.

### Validacoes executadas

- `python scripts/scaffold_modules.py --check`: 444 artefatos sincronizados.
- `python scripts/validate_repository.py`: 24 modulos e 6 apps validados.
- `python scripts/validate_openapi.py`: contratos dos 24 modulos validos.
- `python -m pytest --import-mode=importlib`: 96 testes aprovados.
- `pip-audit --local` e `bandit`: nenhuma vulnerabilidade conhecida/achado.
- Migracoes PostgreSQL aplicadas em container efemero; triggers append-only
  confirmados.
- MongoDB executado em container efemero; quatro colecoes e indices
  geoespacial/TTL confirmados.

### Pendencias rastreadas

- Integracoes de pagamento/fiscal e validadores KYC/KYB reais dependem de
  provedores homologados e segredos externos.
- Apps possuem contrato de integracao; interfaces finais entram nas entregas
  incrementais do roadmap.
- Testes de carga, seguranca dinamica e E2E com provedores serao bloqueadores
  antes de producao.
- O build Docker local excedeu o timeout do Docker Desktop; o gate foi mantido
  em `.github/workflows/ci.yml` para execucao no runner limpo.

### Git

- Branch inicial: `main`
- Branches de dominio: preparadas para publicacao apos o commit baseline.
