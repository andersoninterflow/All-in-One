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
| Runtime FastAPI modular | 85% | Runtime comum, autorizacao, auditoria, outbox e carregamento dinamico por DSN validado em containers | Base local estabilizada; falta ampliar testes E2E por jornada. |
| Mensageria/outbox | 75% | RabbitMQ, dispatcher e testes criticos ja validados | Precisa ampliar cobertura para eventos de todos os modulos. |
| MongoDB/NoSQL | 55% | Script inicial para AI/social/telemetria | Precisa validacao de colecoes, indices e uso real. |
| Docker local | 95% | Postgres, RabbitMQ, MongoDB, Redis, outbox e 13 APIs FastAPI healthy | Falta gate CI para impedir regressao de compose. |
| Apps/frontend | 42% | 6 apps catalogados, plano Stitch com 25 projetos/177 telas e 2 jornadas contratuais locais por pytest | Ainda falta app funcional real e Playwright E2E. |
| Integracoes externas | 20% | Contratos e pontos de extensao existem | KYC/KYB, Pix/PSP, fiscal, CTPS oficial, Stitch remoto e provedores dependem de credenciais/homologacao. |
| Producao/compliance | 20% | Docs e politicas iniciais | Faltam LGPD/DPIA, pentest, carga, DR, backup/restore e observabilidade produtiva. |

## 2. Ordem mandataria de execucao

### Fase 0 - Higiene operacional continua

Objetivo: impedir regressao enquanto o projeto avanca.

Status: 98%

Entregas esperadas:
- Manter `main` limpo e sincronizado com `origin` e `fork`.
- Executar `git add`, `git commit` e `git push` ao concluir cada atividade.
- Atualizar `STATUS.md` e este plano quando a realidade mudar.
- Selecionar automaticamente a opcao `2` em prompts interativos durante este processo.

Pendencias:
- Executar o gate de divergencia em ambiente com PowerShell Core disponivel e
  credenciais remotas configuradas.
- Adicionar gate que falhe se existirem artefatos gerados nao commitados.

Proximos passos naturais:
1. Rodar `scripts/check_git_sync.ps1` no fechamento de cada incremento.
2. Corrigir credenciais locais de push para `origin` ou `fork`.
3. Adicionar verificacao de artefatos gerados nao commitados.

### Fase 1 - Estabilizacao Docker e runtime local

Objetivo: todos os servicos essenciais precisam subir de forma previsivel.

Status: 100%

Entregas ja existentes:
- `postgres`, `rabbitmq`, `mongodb` e `redis` sobem.
- Migrations rodam via servico `migrations`.
- 13 microservicos FastAPI sobem no compose com healthcheck HTTP.
- `api-hub`, `identity`, `finance`, `jobs` e `outbox-dispatcher` permanecem ativos.
- `depends_on` padronizado para aguardar migrations em modulos PostgreSQL.
- `ALL_IN_ONE_*_POSTGRES_DSN` injetado no compose para stores PostgreSQL tipados.
- `/health` validado em `localhost:8100` a `localhost:8112` com stores PostgreSQL.

Pendencias:
- Reduzir tempo de rebuild dos containers Python.
- Acompanhar primeira execucao do workflow `compose-health.yml` no GitHub.

Proximos passos naturais:
1. Executar compose em banco limpo e validar migrations 001-013.
2. Otimizar Dockerfiles com cache de dependencias.
3. Registrar evidencias por execucao em `STATUS.md`.

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

Status: 42%

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
- Criar Playwright E2E por jornada; as jornadas contratuais locais
  `identity -> wallet -> marketplace order` e `business -> jobs -> candidate access`
  ja estao cobertas por pytest.
- Sincronizar design Stitch remoto com credencial rotacionada.

Proximos passos naturais:
1. Corrigir/validar plano Stitch local.
2. Definir shell frontend por app.
3. Expandir jornadas contratuais para delivery, riders, services, health e mobility.
4. Levar as jornadas `identity -> wallet -> marketplace order` e `business -> jobs -> candidate access` para Playwright desktop/mobile quando houver shell frontend.
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
| `identity` | 86% | Contrato, runtime, PostgreSQL especializado, cadastro/login/KYC/MFA E2E e container healthy | KYC/KYB/liveness reais | Homologar provedor KYC/KYB e ampliar testes negativos |
| `business` | 77% | Companies, memberships, idempotencia, store tipado e criacao/aprovacao de empresa coberta na jornada Jobs | Fluxo KYB real e convite operacional de usuarios | Testar convite de usuario e homologar KYB |
| `permissions` | 64% | RBAC/ABAC modelado e store gerado | Enforcement profundo em todos endpoints | Criar matriz de permissoes e testes negativos |
| `finance` | 72% | Wallet, ledger, escrow e store tipado | PSP/Pix/split/fiscal reais | Testar ledger append-only e reconciliacao sandbox |
| `marketplace` | 68% | Catalogo, pedidos e store tipado | Checkout, pagamento e fulfillment | Jornada produto -> carrinho -> pedido -> pagamento |
| `stock` | 62% | Dropshipping e fornecedores modelados | Integracoes reais de fornecedores | Adapter inicial de fornecedor sandbox |
| `delivery` | 68% | Entregas, riders e veiculos com store tipado | Tracking, matching e POD | Jornada pedido -> cotacao -> rider -> entrega |
| `riders` | 62% | Candidatura, documentos e veiculos modelados | Aprovacao e ganhos reais | Fluxo de onboarding rider |
| `services` | 68% | Prestadores e contratos com store tipado | Anti-burla e escrow | Jornada visita -> orcamento -> contrato |
| `mobility` | 68% | Rides, tickets e fare rules com store tipado | ETA, QR/NFC e tarifas reais | Jornada corrida e ticket |
| `jobs` | 87% | Mais maduro: CTPS/cofre/outbox/testes e jornada candidato -> vaga -> recrutador coberta por pytest | Homologacao CTPS oficial e Playwright E2E | Expandir fluxo para triagem, entrevista e notificacoes |
| `api_hub` | 82% | API keys/webhooks, SQL refinado, rotas gateway de API key/webhook e testes de rate limit | OAuth2 real e testes de proxy com servicos vivos | Testar OAuth2 real, assinatura de webhooks de saida e rate limit com Redis real |
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
- Pelo menos 6 jornadas E2E passam, uma por app; 2 jornadas contratuais locais ja passam por pytest.
- API Hub funciona com API key, webhook assinado e rate limit.
- Identity tem login/MFA/KYC sandbox.
- Finance tem pagamento/escrow/refund sandbox.
- Observabilidade basica registra logs, metricas e erros.
- CI bloqueia regressao de OpenAPI, testes, migrations e seguranca.

## 5. Primeira sprint de execucao

Sequencia recomendada:

1. Criar teste matriz de stores PostgreSQL.
2. Corrigir stores gerados que falharem contra Postgres.
3. Rodar migrations e testes em ambiente limpo.
4. Implementar gate CI de compose/healthcheck.
5. Testar OAuth2 real, webhooks de saida e rate limit Redis no API Hub.
6. Implementar jornada E2E `business -> jobs -> candidate access`. Concluido em 2026-05-30.
7. Expandir jornadas E2E para delivery, riders, services, health e mobility.
8. Atualizar `STATUS.md`.
9. Sincronizar Git.
