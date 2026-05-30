# Status Operacional

## STATUS OPERACIONAL - 2026-05-30 Estabilizacao Docker Runtime Validada

### Concluido neste ciclo

- Docker Compose local estabilizado para os 13 servicos FastAPI principais: `api-hub`, `identity`, `finance`, `marketplace`, `delivery`, `services`, `mobility`, `erp`, `wms`, `tms`, `crm`, `health` e `jobs`.
- `api-hub` corrigido para carregar dependencias e variaveis de runtime sem restart.
- `identity` e `finance` corrigidos para copiar o modulo completo no Dockerfile, preservando imports locais.
- `modules/shared/runtime.py` ajustado para resolver stores PostgreSQL dinamicamente dentro e fora dos containers.
- `infra/docker/docker-compose.yml` padronizado com healthcheck HTTP, dependencia de migrations e DSNs PostgreSQL para os modulos com store tipado.
- Requirements dos microservicos padronizados com `psycopg[binary]==3.3.4` para evitar falha de import em stores PostgreSQL.
- Fluxo Identity E2E estabilizado: cadastro, login JWT, submissao KYC e MFA setup passam contra container real.
- Store Identity tipado corrigido para cadastro com ID fornecido pelo payload, normalizacao `document_cpf`/`cpf_document`, audit/outbox com usuario correto e alias `kyc_records`.
- Telemetria Identity ajustada para nao bloquear operacoes transacionais quando Mongo estiver indisponivel ou lento.
- Suporte local de testes corrigido em `platform_test_support.py` para importar modulos com dependencias locais.

### Validacoes executadas

- `docker compose -f infra/docker/docker-compose.yml ps`: 13 servicos FastAPI healthy, alem de PostgreSQL e RabbitMQ healthy.
- `/health` em `localhost:8100` a `localhost:8112`: todos retornaram `ok` com stores PostgreSQL tipados.
- `python scripts/validate_repository.py`: aprovado.
- `python scripts/validate_openapi.py`: aprovado.
- `python -m pytest --import-mode=importlib -q`: 112 testes aprovados, 3 ignorados.

### Pendencias rastreadas

- Ampliar matriz de testes PostgreSQL para create/get/list/update/soft_delete/idempotencia/audit/outbox em todos os modulos.
- Tipar stores de menor maturidade alem dos modulos prioritarios ja especializados.
- Implementar provedores reais para KYC/KYB, Pix/PSP, fiscal, CTPS oficial, mapas/tracking e IA.
- Criar gates CI para divergencia Git, artefatos nao commitados, migrations, testes, OpenAPI e seguranca.

### Git

- Incremento pronto para sincronizacao em `main` apos registro deste status.

## STATUS OPERACIONAL - 2026-05-29 Expansao PostgreSQL e Integracao Validada

### Concluido neste ciclo

- Adapter PostgreSQL expandido para todos os 25 microservicos da plataforma.
- Implementacao de `BasePostgresStore` em `modules/shared/` para unificar a logica de transacoes, auditoria append-only, outbox RabbitMQ e idempotencia.
- Stores especializados (`Jobs`, `Identity`, `Finance`, `ApiHub`, `Business`, `Marketplace`, `Delivery`, `Services`, `Mobility`) refatorados para usar a classe base, preservando o mapeamento tipado de colunas.
- Scaffold automatico gerado para os 16 microservicos restantes, garantindo suporte imediato a PostgreSQL via metadados JSONB.
- Runtime (`modules/shared/runtime.py`) atualizado para carregamento dinamico de stores PostgreSQL baseado em variaveis de ambiente (`ALL_IN_ONE_*_POSTGRES_DSN`).
- Infraestrutura local Docker Compose estabilizada; RabbitMQ, PostgreSQL e MongoDB operacionais.
- Migracoes PostgreSQL (008 a 012) aplicadas com sucesso, incluindo colunas de idempotencia e refinamento do schema `api_hub` e `business`.
- Fluxo de ponta a ponta `PostgreSQL -> Outbox -> RabbitMQ` validado localmente com sucesso via testes de integracao.

### Validacoes executadas

- `docker compose -f infra/docker/docker-compose.yml up -d`: Ambiente de infraestrutura completo subido com sucesso.
- `python -m pytest tests/test_outbox_rabbitmq_integration.py tests/test_jobs_postgres_integration.py -v`: 3 testes de integracao críticos aprovados em ambiente real (PostgreSQL + RabbitMQ).
- `python scripts/scaffold_postgres_stores.py`: Geração bem-sucedida de 16 novos adapters para cobertura total da plataforma.
- `python scripts/stitch_orchestrator.py plan`: Plano de design materializado para 25 projetos e 177 telas.
- Verificacao de logs do container de migracoes: 12 arquivos SQL aplicados sem erros.

### Validacoes Do Incremento Em Andamento

- Sincronizacao remota do Stitch aguardando credenciais de ambiente produtivo ou automacao via ferramentas MCP.
- Expansao de testes de integracao especificos para os novos adapters (Marketplace, Delivery, etc.).

### Pendencias rastreadas

- Integracoes de pagamento/fiscal e validadores KYC/KYB/CTPS oficiais dependem de provedores homologados.
- Testes de carga e seguranca dinamica serao bloqueadores antes de producao.
- Sincronizacao do Stitch requer segredos rotacionados para ambiente remoto.

### Git

- Branch principal: `main`.
- Todos os adapters PostgreSQL e refatoracao de store mesclados localmente para preparacao do proximo incremento.
