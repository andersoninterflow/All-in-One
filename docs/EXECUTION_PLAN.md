# Plano de Execucao Ordenada - All-in-One

Data-base: 2026-05-29  
Branch operacional: `main`  
Meta: transformar o MVP backend/data atual em beta operacional validado, com infraestrutura estavel, PostgreSQL real por modulo, jornadas E2E e integracoes externas homologadas.

## 1. Estado consolidado

| Area | Conclusao | Evidencia atual | Leitura operacional |
| --- | ---: | --- | --- |
| Git e sincronizacao remota | 100% | `local main`, `origin/main` e `fork/main` alinhados | Fluxo de entrega remoto esta operacional. |
| Contratos de microservicos | 100% | 25 modulos com OpenAPI, contratos, Dockerfile, docs e testes base | Superficie contratual completa para evoluir. |
| PostgreSQL estrutural | 80% | 12 migrations SQL e stores para 25 modulos | Schema amplo existe; falta prova real por modulo. |
| Runtime FastAPI modular | 70% | Runtime comum, autorizacao, auditoria, outbox e carregamento dinamico por DSN | Base pronta; falta estabilizar todos os containers e DSNs. |
| Mensageria/outbox | 75% | RabbitMQ, dispatcher e testes criticos ja validados | Precisa ampliar cobertura para eventos de todos os modulos. |
| MongoDB/NoSQL | 55% | Script inicial para AI/social/telemetria | Precisa validacao de colecoes, indices e uso real. |
| Docker local | 70% | Postgres, RabbitMQ, MongoDB, Redis e varios servicos sobem | `api-hub` reiniciando; alguns servicos essenciais nao estavam ativos no ultimo `ps`. |
| Apps/frontend | 35% | 6 apps catalogados e plano Stitch com 25 projetos/177 telas | Ainda falta app funcional real e testes E2E. |
| Integracoes externas | 20% | Contratos e pontos de extensao existem | KYC/KYB, Pix/PSP, fiscal, CTPS oficial, Stitch remoto e provedores dependem de credenciais/homologacao. |
| Producao/compliance | 20% | Docs e politicas iniciais | Faltam LGPD/DPIA, pentest, carga, DR, backup/restore e observabilidade produtiva. |

## 2. Ordem mandataria de execucao

### Fase 0 - Higiene operacional continua

Objetivo: impedir regressao enquanto o projeto avanca.

Status: 90%

Entregas esperadas:
- Manter `main` limpo e sincronizado com `origin` e `fork`.
- Executar `git add`, `git commit` e `git push` ao concluir cada atividade.
- Atualizar `STATUS.md` e este plano quando a realidade mudar.
- Selecionar automaticamente a opcao `2` em prompts interativos durante este processo.

Pendencias:
- Automatizar verificacao de divergencia entre `origin/main`, `fork/main` e local no CI.
- Adicionar gate que falhe se existirem artefatos gerados nao commitados.

Proximos passos naturais:
1. Criar script `scripts/check_git_sync.ps1`.
2. Rodar o script no fechamento de cada incremento.
3. Incluir o gate em workflow CI.

### Fase 1 - Estabilizacao Docker e runtime local

Objetivo: todos os servicos essenciais precisam subir de forma previsivel.

Status: 70%

Entregas ja existentes:
- `postgres`, `rabbitmq`, `mongodb` e `redis` sobem.
- Migrations rodam via servico `migrations`.
- Varios microservicos FastAPI sobem no compose.

Pendencias:
- Corrigir `api-hub`, que estava em estado `Restarting`.
- Fazer `identity`, `finance`, `jobs` e `outbox-dispatcher` aparecerem ativos e saudaveis no `docker compose ps`.
- Adicionar healthcheck HTTP para cada microservico.
- Padronizar `depends_on` para aguardar `migrations` quando o modulo usar PostgreSQL.
- Injetar `ALL_IN_ONE_*_POSTGRES_DSN` no compose para todos os modulos que ja possuem store PostgreSQL.

Proximos passos naturais:
1. Coletar logs de `api-hub`.
2. Corrigir import, dependency, env ou migration que estiver causando restart.
3. Atualizar `infra/docker/docker-compose.yml` com DSNs por modulo.
4. Subir compose limpo.
5. Validar `/health` ou endpoint equivalente de todos os servicos.
6. Registrar evidencias em `STATUS.md`.

### Fase 2 - Banco de dados e stores PostgreSQL

Objetivo: trocar o contrato local por persistencia PostgreSQL real, auditavel e testada.

Status: 80%

Entregas ja existentes:
- 12 migrations PostgreSQL.
- `BasePostgresStore` compartilhado.
- Stores especializados para `jobs`, `identity`, `finance`, `api_hub`, `business`, `marketplace`, `delivery`, `services` e `mobility`.
- Stores gerados para os demais modulos.
- Idempotencia espalhada nas principais tabelas.

Pendencias:
- Validar migrations 001-012 em banco limpo e banco ja populado.
- Criar testes CRUD reais para cada store PostgreSQL.
- Confirmar audit log append-only em todos os fluxos sensiveis.
- Confirmar outbox para eventos de todos os modulos.
- Substituir stores genericos por mapeamentos tipados nos modulos de maior risco.

Prioridade de tipagem por risco:
1. `finance`
2. `identity`
3. `business`
4. `api_hub`
5. `marketplace`
6. `delivery`
7. `services`
8. `mobility`
9. `jobs`
10. Demais modulos operacionais

Proximos passos naturais:
1. Criar suite `tests/test_postgres_stores_matrix.py`.
2. Testar create/get/list/update/soft_delete/idempotency por modulo.
3. Testar audit/outbox por modulo.
4. Corrigir cada store gerado que tentar gravar colunas inexistentes.
5. Atualizar docs de DSN e operacao.

### Fase 3 - Eventos, RabbitMQ e observabilidade

Objetivo: garantir comunicacao assincroma confiavel e rastreavel.

Status: 75%

Entregas ja existentes:
- `audit.domain_events`.
- Worker `outbox-dispatcher`.
- Testes de integracao com RabbitMQ para fluxo critico.

Pendencias:
- Validar eventos de todos os modulos.
- Garantir `correlation_id` em chamadas e eventos.
- Criar retry/backoff observavel por falha.
- Dashboards e alertas de outbox parada, fila acumulada e erro de publish.

Proximos passos naturais:
1. Criar fixtures de evento por modulo.
2. Rodar dispatcher contra eventos reais de cada dominio.
3. Adicionar metricas Prometheus/OpenTelemetry.
4. Criar runbook de incidentes de fila.

### Fase 4 - Jornadas E2E por app

Objetivo: transformar microservicos em jornadas de produto.

Status: 35%

Apps e prioridades:
- `all-in-one-user`: cadastro, wallet, busca, compra, delivery, jobs.
- `all-in-one-business`: empresa, aprovacao, usuarios, jobs, ERP, relatorios.
- `all-in-one-riders`: candidatura, documento, veiculo, entrega/corrida, ganhos.
- `all-in-one-services`: prestador, visita, orcamento, contrato, evidencia.
- `all-in-one-health`: paciente, agenda, prontuario, consulta.
- `all-in-one-mobility`: corrida, ticket, QR/NFC, historico.

Pendencias:
- Implementar interfaces funcionais reais.
- Ligar cada app aos endpoints FastAPI.
- Criar Playwright E2E por jornada.
- Sincronizar design Stitch remoto com credencial rotacionada.

Proximos passos naturais:
1. Corrigir/validar plano Stitch local.
2. Definir shell frontend por app.
3. Implementar jornada `identity -> wallet -> marketplace order` primeiro.
4. Implementar jornada `business -> jobs -> candidate access` depois.
5. Rodar testes E2E desktop/mobile.

### Fase 5 - Integracoes externas homologadas

Objetivo: substituir mocks/contratos por provedores reais.

Status: 20%

Pendencias por area:
- Identity: OIDC, MFA real, KYC/KYB, liveness, biometria e consentimento LGPD.
- Finance: PSP/Pix, split, escrow, refund, conciliacao, antifraude e fiscal.
- Jobs: verificador oficial CTPS Digital ou integrador autorizado.
- Marketplace/Stock: fornecedores homologados, catalogo, preco, pedido e tracking.
- Delivery/Mobility: mapas, ETA, tracking, roteirizacao, comprovante e antifraude.
- Health: governanca de prontuario, prescricao, telemedicina e consentimento.
- API Hub: OAuth2, API keys, webhooks assinados, sandbox e rate limits reais.

Proximos passos naturais:
1. Criar matriz de provedores e segredos em `docs/INTEGRATION.md`.
2. Separar sandbox/producao.
3. Implementar adapters por provider com testes de contrato.
4. Registrar evidencias de homologacao.

### Fase 6 - Seguranca, compliance e producao

Objetivo: sair de beta tecnica para producao auditavel.

Status: 20%

Pendencias:
- LGPD/DPIA e politica de retencao.
- Pentest e SAST/DAST.
- Testes de carga.
- Backup/restore e disaster recovery.
- Observabilidade completa.
- Runbooks de incidentes.
- Revisao de permissoes para dados sensiveis de saude, identidade, financeiro e trabalho.

Proximos passos naturais:
1. Criar `docs/COMPLIANCE.md`.
2. Criar matriz de dados sensiveis por modulo.
3. Adicionar scans obrigatorios no CI.
4. Testar restore de Postgres/Mongo.
5. Definir SLOs e alertas.

## 3. Matriz por modulo

| Modulo | Conclusao | Estado | Pendencia principal | Proximo passo |
| --- | ---: | --- | --- | --- |
| `identity` | 78% | Contrato, runtime, PostgreSQL especializado e KYC/MFA modelado | KYC/KYB/liveness reais | Teste E2E de cadastro, sessao, consentimento e verificacao |
| `business` | 74% | Companies, memberships, idempotencia e store tipado | Fluxo KYB e aprovacao operacional | Testar onboarding empresa e convite de usuario |
| `permissions` | 64% | RBAC/ABAC modelado e store gerado | Enforcement profundo em todos endpoints | Criar matriz de permissoes e testes negativos |
| `finance` | 72% | Wallet, ledger, escrow e store tipado | PSP/Pix/split/fiscal reais | Testar ledger append-only e reconciliacao sandbox |
| `marketplace` | 68% | Catalogo, pedidos e store tipado | Checkout, pagamento e fulfillment | Jornada produto -> carrinho -> pedido -> pagamento |
| `stock` | 62% | Dropshipping e fornecedores modelados | Integracoes reais de fornecedores | Adapter inicial de fornecedor sandbox |
| `delivery` | 68% | Entregas, riders e veiculos com store tipado | Tracking, matching e POD | Jornada pedido -> cotacao -> rider -> entrega |
| `riders` | 62% | Candidatura, documentos e veiculos modelados | Aprovacao e ganhos reais | Fluxo de onboarding rider |
| `services` | 68% | Prestadores e contratos com store tipado | Anti-burla e escrow | Jornada visita -> orcamento -> contrato |
| `mobility` | 68% | Rides, tickets e fare rules com store tipado | ETA, QR/NFC e tarifas reais | Jornada corrida e ticket |
| `jobs` | 84% | Mais maduro: CTPS/cofre/outbox/testes | Homologacao CTPS oficial e E2E amplo | Fluxo candidato -> vaga -> recrutador |
| `api_hub` | 70% | API keys/webhooks e SQL refinado | Container reiniciando, OAuth2 real | Corrigir restart e testar API key/webhook |
| `erp` | 60% | Fiscal/accounting modelado e store gerado | Fluxos contabeis reais | Tipar store ERP e testar payables/receivables |
| `wms` | 60% | Armazem/inventario modelados | Operacao real de estoque | Tipar store WMS e testar recebimento/picking |
| `tms` | 60% | Fretes/transportadoras modelados | Torre de controle e POD | Tipar store TMS e testar frete |
| `crm` | 60% | Leads/oportunidades modelados | Pipeline e campanhas reais | Tipar store CRM e testar lead -> oportunidade |
| `bpm` | 58% | Processos/workflows modelados | Engine real de workflow | Implementar timers/SLA/escalonamento |
| `document` | 58% | GED/OCR/assinatura modelados | Storage, OCR e assinatura reais | Tipar store e implementar upload/versionamento |
| `hr` | 58% | HCM/ATS/LMS modelado | Folha, ponto e LMS reais | Fluxo colaborador -> folha -> treinamento |
| `health` | 60% | Pacientes/agenda/prontuario modelados | Consentimento e telemedicina reais | Tipar store Health e testar agendamento |
| `vision` | 55% | Dispositivos/streams/alertas modelados | Ingestao de video e IA | Prova de stream e alerta |
| `legal` | 55% | Casos/prazos/audiencias modelados | Integracoes tribunal/calendario | Fluxo caso -> prazo -> alerta |
| `property` | 55% | Imoveis/unidades/locacoes modelados | Condominio e manutencao reais | Fluxo locacao/manutencao |
| `bi` | 55% | Datasets/dashboards modelados | ETL e permissao analitica | Primeiro dashboard auditavel |
| `ai_core` | 55% | Memoria/moderacao/model runs modelados | Providers IA e governanca | Adapter de provider e custo por execucao |

## 4. Criterios de beta

O projeto entra em beta quando todos os itens abaixo estiverem verdes:

- Docker Compose sobe todos os servicos essenciais sem restart.
- Migrations PostgreSQL 001-012 aplicam em banco limpo.
- Stores PostgreSQL passam CRUD/idempotencia/audit/outbox em todos os modulos prioritarios.
- Pelo menos 6 jornadas E2E passam, uma por app.
- API Hub funciona com API key, webhook assinado e rate limit.
- Identity tem login/MFA/KYC sandbox.
- Finance tem pagamento/escrow/refund sandbox.
- Observabilidade basica registra logs, metricas e erros.
- CI bloqueia regressao de OpenAPI, testes, migrations e seguranca.

## 5. Primeira sprint de execucao

Sequencia recomendada:

1. Corrigir Docker e `api-hub`.
2. Ativar `identity`, `finance`, `jobs` e `outbox-dispatcher` no compose.
3. Adicionar DSNs para todos os stores PostgreSQL.
4. Criar teste matriz de stores PostgreSQL.
5. Corrigir stores gerados que falharem contra Postgres.
6. Rodar migrations e testes em ambiente limpo.
7. Atualizar `STATUS.md`.
8. Sincronizar Git.

