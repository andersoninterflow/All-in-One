# Status Operacional

## STATUS OPERACIONAL - 2026-06-02 Sincronizacao Remota Stitch Persistente

### Concluido neste ciclo

- Catálogo Valley/Marketplace expandido conforme `docs/ORIENTACAO_CODEX_SYNC_MARKETPLACE_VALLEY.md`, com regra Business -> Marketplace -> Valley para ofertas reais.
- Ofertas reais agora exigem `publish_to_valley = true`, `publication_status` aprovado/publicado e `visible_to_consumer` ativo para aparecer no Valley.
- Payload público do catálogo passou a incluir rastreabilidade (`source_entity_id`, `business_id`, `seller_user_id`), tipo/categoria de empresa, ramo de atividade, status de publicação, descrição curta, ação principal simples e filtros comerciais.
- Criados endpoints `GET /valley/catalog`, `GET /valley/catalog/business-activities` e `GET /valley/catalog/offers/{offer_id}`.
- Busca Valley aceita filtros por `company_type`, `company_category`, `business_activity`, preço, disponibilidade e `verified_only`, preservando regionalização por raio.
- Transições de publicação de ofertas comerciais passaram a emitir `valley.catalog.offer.synced` via outbox seguro.
- `docs/VALLEY_CATALOG.md` e `docs/ORIENTACAO_CODEX_SYNC_MARKETPLACE_VALLEY.md` documentam a regra operacional e linguagem simples do usuário final.
- Ciclo remoto Stitch concluiu os módulos `mobility` e `jobs`, conectando deslocamento, transporte e oportunidades profissionais ao catálogo Valley por categoria de empresa e ramo de atividade.
- Logomarcas oficiais incorporadas ao repo em `assets/brand/all-in-one-logo-official.png`, `assets/brand/all-in-one-logo-light-official.png` e `assets/brand/valley-logo-official.png`.
- Criado contrato mandatorio `config/branding/brand_identity.json`, com All-in-One como marca guarda-chuva e Valley obrigatorio para `valley`, `valley-business` e `valley-rider`.
- `README.md` passou a exibir a imagem oficial All-in-One no topo para apresentacao do projeto no GitHub.
- Prompts Stitch agora instruem uso padronizado das logos oficiais, proibindo redesenho, distorcao, corte, rotacao ou recoloracao.
- Criado `scripts/stitch_auto_sync.py` para executar plano, validacao de politica, sync remoto e conferência de completude do estado Stitch.
- `scripts/stitch_orchestrator.py` ganhou comando `status` e resumo comparando `screen_manifest.json` com `sync_state.json`.
- Criado workflow `.github/workflows/stitch-sync.yml` com execucao manual, agendada a cada 6 horas e por push em artefatos Stitch.
- O workflow usa somente `secrets.STITCH_API_KEY`, executa `python scripts/stitch_auto_sync.py --require-remote` e commita `config/stitch/sync_state.json` quando o MCP remoto retorna IDs.
- `tests/test_stitch_orchestrator.py` e `scripts/validate_repository.py` agora bloqueiam remocao da automacao persistente e do uso de secret.
- Corrigido helper `get_erp_store()` para manter os endpoints ERP customizados importaveis.
- `modules/erp/main.py` passou a ser preservado pelo scaffold por ser entrypoint especializado.

### Estado atual da sincronia

- Manifesto local: 25 projetos Stitch planejados.
- Estado remoto local versionado: 19 projetos e 139 telas registrados em `config/stitch/sync_state.json`.
- Branding remoto: `branding_pending` zerado para todas as telas existentes; todas as 139 telas registradas carregam `branding_version` 2026-06-01.
- Modulos remotos completos neste estado: `identity`, `business`, `permissions`, `finance`, `marketplace`, `stock`, `delivery`, `riders`, `services`, `mobility`, `jobs` e `erp`.
- Modulo `jobs`: concluido com telas de vagas, candidatura, curriculo, documentos, CTPS, auditoria e revisao por recrutador.
- Modulo `erp`: concluido com visao geral, contas, contas a pagar, contas a receber, centros de custo, documentos fiscais e auditoria/permissoes.
- Modulo `wms`: concluido com visao geral, armazens, enderecos/bin, inventario, ondas de separacao, remessas e auditoria/permissoes.
- Modulo `tms`: concluido com visao geral, transportadoras, fretes, rotas, comprovantes de entrega, auditoria de fretes e auditoria/permissoes.
- Modulo `crm`: concluido com visao geral, leads, oportunidades, atividades, campanhas e auditoria/permissoes.
- Modulo `bpm`: concluido com visao geral, processos, instancias de workflow, tarefas, politicas de SLA e auditoria/permissoes.
- Modulo `document`: concluido com visao geral, pastas, documentos, versoes, politicas de retencao e auditoria/permissoes.
- Modulo `hr`: concluido com visao geral, colaboradores, folha, candidatos, cursos, registros ocupacionais e auditoria/permissoes.
- Modulo `health`: projeto criado com telas iniciais `overview`, `entity_patients` e `entity_appointments`; ainda faltam `audit_permissions`, `entity_beds`, `entity_medical_records` e `entity_prescriptions`.
- Proximo passo natural Stitch: concluir telas pendentes de `health` e seguir para `vision`, conectando relacionamento comercial, processos, documentos, pessoas, saude, bem-estar, dispositivos e monitoramento inteligente ao ecossistema Valley.
- Sync remoto real: validado com `STITCH_API_KEY` no Windows e automatizado no GitHub Actions quando `secrets.STITCH_API_KEY` existir.

### Validacoes executadas

- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, registrando 5 projetos Stitch.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 6"`: sucesso, concluindo telas pendentes de `marketplace`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `stock` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, concluindo telas pendentes de `stock`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `delivery` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, concluindo telas pendentes de `delivery`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `riders` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 3"`: sucesso, concluindo telas pendentes de `riders`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `services` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, concluindo telas pendentes de `services`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `mobility` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: progresso parcial em `mobility`; Stitch retornou credencial remota ausente em `entity_tickets`, com estado local preservado.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py tools"`: sucesso, tools Stitch listadas apos falha remota.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 1"`: sucesso, retomando `mobility` tela a tela apos falha de credencial.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 1"`: sucesso, concluindo telas pendentes de `mobility`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `jobs` e registrando 4 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\validate_stitch_mcp_config.py --require-secret && .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 5"`: sucesso, concluindo as telas pendentes de `jobs`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `erp` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 1"`: sucesso, registrando `erp/entity_receivables` apos falha remota transitoria de credencial OAuth.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 1"`: sucesso, registrando `erp/entity_cost_centers`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 1"`: sucesso, registrando `erp/entity_fiscal_documents`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 1"`: sucesso, registrando `erp/audit_permissions` e concluindo `erp`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `wms` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: progresso parcial em `wms`, registrando inventario, ondas de separacao e remessas; Stitch retornou credencial remota ausente em `audit_permissions`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 1"`: sucesso, registrando `wms/audit_permissions` e concluindo `wms`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `tms` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, registrando rotas, comprovantes de entrega, auditoria de fretes e auditoria/permissoes, concluindo `tms`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `crm` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 3"`: sucesso, registrando atividades, campanhas e auditoria/permissoes, concluindo `crm`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `bpm` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 3"`: sucesso, registrando tarefas, politicas de SLA e auditoria/permissoes, concluindo `bpm`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `document` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 3"`: sucesso, registrando versoes, politicas de retencao e auditoria/permissoes, concluindo `document`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `hr` e registrando 3 telas iniciais.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, registrando candidatos, cursos, registros ocupacionais e auditoria/permissoes, concluindo `hr`.
- `cmd.exe /C "... .venv\Scripts\python.exe scripts\stitch_orchestrator.py sync --max-operations 4"`: sucesso, criando projeto `health` e registrando 3 telas iniciais.
- `.venv/Scripts/python.exe -m pytest -q tests/test_stitch_orchestrator.py tests/test_branding_assets.py tests/test_valley_catalog.py`: sucesso, 17 testes aprovados.
- `.venv/Scripts/python.exe -m pytest -q tests/test_valley_catalog.py tests/test_outbox_dispatcher_unit.py`: sucesso, 15 testes aprovados.
- `.venv/Scripts/python.exe -m pytest -q tests/test_stitch_orchestrator.py tests/test_branding_assets.py`: sucesso, 12 testes aprovados.
- `python3 scripts/validate_repository.py`: sucesso.
- `python3 scripts/validate_stitch_mcp_config.py --require-secret` via Windows: sucesso.
- `python3 scripts/stitch_orchestrator.py discover` via Windows: sucesso, com tools oficiais Stitch listadas.
- `python3 scripts/stitch_orchestrator.py sync --max-operations 1` via Windows: sucesso, aplicando branding oficial em tela remota existente.
- `python3 scripts/stitch_orchestrator.py sync --max-operations 5` via Windows: sucesso, reduzindo `branding_pending` de 14 para 9.
- `python3 scripts/stitch_orchestrator.py sync --max-operations 5` via Windows: sucesso, reduzindo `branding_pending` de 9 para 4.
- `python3 scripts/stitch_orchestrator.py sync --max-operations 4` via Windows: sucesso, zerando `branding_pending`.
- `python3 scripts/stitch_orchestrator.py sync --max-operations 3` via Windows: sucesso, criando 3 novas telas Business com branding oficial.
- `python3 scripts/stitch_orchestrator.py sync --max-operations 2` via Windows: sucesso, concluindo as 2 telas restantes de Business.
- `python3 scripts/stitch_orchestrator.py sync --max-operations 4` via Windows: sucesso, criando projeto Permissions e 3 telas iniciais.
- `python3 scripts/stitch_orchestrator.py sync --max-operations 4` via Windows: sucesso, concluindo as 4 telas restantes de Permissions.
- `python3 scripts/stitch_orchestrator.py sync --max-operations 4` via Windows: sucesso, criando projeto Finance e 3 telas iniciais.
- `python3 scripts/stitch_orchestrator.py sync --max-operations 5` via Windows: sucesso, concluindo as 5 telas restantes de Finance.
- `.venv/Scripts/python.exe -m pytest -q`: sucesso, 195 testes aprovados e 29 pulados.
- `.venv/Scripts/python.exe -m pytest -q tests/test_stitch_orchestrator.py tests/test_branding_assets.py`: sucesso, 12 testes aprovados.
- `python3 scripts/scaffold_modules.py --check`: sucesso.
- `python3 scripts/validate_repository.py`: sucesso.
- `python3 scripts/validate_openapi.py`: sucesso.

## STATUS OPERACIONAL - 2026-06-01 PrometheusRule Retencao LGPD

### Concluido neste ciclo

- `infra/kubernetes/base/retention-alerting.yaml` criado com `PrometheusRule` para os 5 alertas de retencao LGPD.
- O mesmo manifesto inclui `AlertmanagerConfig` com rota para `compliance-oncall` e severidade critica tambem para `platform-oncall`.
- `scripts/validate_repository.py` passou a exigir a materializacao Kubernetes de cada alerta e a equivalencia das expressoes Prometheus com `config/observability/retention_alerts.json`.
- `tests/test_retention_alerts.py` expandido para validar `PrometheusRule`, `AlertmanagerConfig`, severidade, janela e runbook.
- `docs/COMPLIANCE.md`, `docs/OPERATIONS.md`, `docs/REQUIREMENTS_TRACEABILITY.md` e `docs/EXECUTION_PLAN.md` atualizados; Producao/compliance avanca para 59%.

### Validacoes executadas

- Pendente neste ciclo: testes focados, validadores e suite completa.

### Pendencias rastreadas

- Aplicar manifests de monitoramento no cluster real e validar disparo controlado dos alertas.
- Aplicar mutacoes finais nos stores de dominio apos homologacao de dry-run por modulo.
- Registrar DPIA assinada para modulos criticos.
- Adicionar scans SAST/SCA/DAST obrigatorios no CI.

### Git

- Incremento em preparacao para commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-06-01 Componente CheckoutModal UI

### Concluído neste ciclo

- Desenvolvido `checkout_modal_1.html` em `.superdesign/design_iterations/`.
- Implementada lógica visual de Pepitas (1, 10, 100) e regra de descontos `BR-STO-009`.
- Estética Neo-brutalista aplicada com variáveis de marca Valley.
- Sinalização de imutabilidade e proteção de Ledger adicionada ao rodapé da interface.

## STATUS OPERACIONAL - 2026-06-01 Componente LedgerTransactionList UI

### Concluído neste ciclo

- Desenvolvido componente `LedgerTransactionList.tsx` para visualização de extrato imutável.
- Aplicada estética Neo-brutalista e sinalização de imutabilidade (append-only).
- Integrado ao sistema de cores Valley (Success para créditos, Error para débitos).

## STATUS OPERACIONAL - 2026-06-01 Componente CalculatorWidget UI

### Concluído neste ciclo

- Desenvolvido componente `CalculatorWidget.tsx` com lógica de cálculo funcional.
- Aplicada estética Neo-brutalista integrada ao `valley_design_system.css`.
- Layout otimizado para dashboard ERP do Valley Business.

## STATUS OPERACIONAL - 2026-06-01 Componente PepitaWidget UI

### Concluído neste ciclo

- Desenvolvido componente `PepitaWidget.tsx` em React.
- Aplicada estética Neo-brutalista com feedback visual de estado ativo/selecionado.
- Integrado ao sistema de cores Valley (Cyan para seleção, Lavender para ocioso).
- Componente pronto para visualização no Superdesign Canvas.

## STATUS OPERACIONAL - 2026-06-01 Governança Valley Integrada

### Concluído neste ciclo

- Implementada regra `BR-STO-009` em `modules/shared/valley_logic.py`.
- Adicionado suporte a Gamificação (1, 10, 100 Pepitas) no endpoint `/erp/billing`.
- Design de UI "Billing Detail" mapeado conforme padrão Stitch/Superdesign.
- Reforçada política `append-only` para tabelas de saldo e auditoria.

## STATUS OPERACIONAL - 2026-06-01 Consulta Detalhada ERP

### Concluído neste ciclo

- Implementado método `get_billing_detail` no `ErpPostgresStore` com suporte a itens.
- Adicionado endpoint `GET /erp/billing/{document_id}` no módulo ERP.
- Validada a recuperação de faturamentos com joins lógicos de itens no PostgreSQL.

## STATUS OPERACIONAL - 2026-06-01 Cancelamento de Faturamento ERP

### Concluído neste ciclo

- Implementada lógica de cancelamento imutável no `ErpPostgresStore`.
- Criada suíte de testes de integração `modules/erp/tests/test_cancel_billing_integration.py`.
- Adicionado endpoint `POST /erp/billing/{document_id}/cancel` no módulo ERP com motivo obrigatório.
- Conectado o cancelamento ao `local_fiscal_document_simulator` para simulação de cancelamento fiscal.
- Configurado disparo do evento `erp.invoice.cancelled` para auditoria e outbox.
- Atualizada integridade do store com importação do `uuid4`.

### Validações executadas

- `.venv/Scripts/python.exe -m pytest modules/erp/tests/test_cancel_billing_integration.py`: Sucesso (2 testes aprovados), confirmando a integração com o sandbox fiscal de cancelamento.

## STATUS OPERACIONAL - 2026-06-01 Integração Sandbox ERP

### Concluído neste ciclo

- Conectado `POST /erp/billing` ao `local_fiscal_document_simulator` em `modules/erp/main.py`.
- Criada suíte de testes de integração `modules/erp/tests/test_billing_integration.py`.
- Atualizada `provider_matrix.json` com a variável `ALL_IN_ONE_ERP_FISCAL_SANDBOX`.
- Validada a persistência atômica de Documento + Itens via store especializado.

## STATUS OPERACIONAL - 2026-06-01 Expansão ERP e Itens de Fatura

### Concluído neste ciclo

- Criada Migration 017: Tabela `erp.invoice_items` e índice de performance.
- Atualizado `ErpPostgresStore` para suportar transação atômica de faturamento + itens.
- Implementado `modules/erp/main.py` com o endpoint `POST /erp/billing`.
- Validador de repositório atualizado para exigir os novos artefatos fiscais.

## STATUS OPERACIONAL - 2026-06-01 Lógica de Faturamento ERP

### Concluído neste ciclo

- Implementado `ErpPostgresStore` especializado em `modules/shared/erp_postgres_store.py`.
- Integrada lógica de criação de documentos fiscais com validação mandatória de `tax_amount_brl`.
- Otimização de consultas de faturamento utilizando os índices de correlação e auditoria da migration 016.
- Atualizado `scripts/scaffold_postgres_stores.py` para proteger a especialização do ERP.

### Validações executadas

- `.venv/Scripts/python.exe -m pytest tests/test_postgres_stores_matrix.py -k erp`: Sucesso.

## STATUS OPERACIONAL - 2026-05-31 Matriz LGPD E Compliance

### Concluido neste ciclo

- `docs/COMPLIANCE.md` criado com principios LGPD, matriz de grupos de risco, gates de producao e pendencias.
- `config/compliance/data_classification.json` criado cobrindo os 25 modulos com risco, dominios de dados, categorias sensiveis, base legal, retencao e gates de producao.
- `tests/test_compliance_matrix.py` criado para bloquear ausencia de modulo, campo obrigatorio vazio e gate fraco em modulos criticos.
- `scripts/validate_repository.py` passou a exigir `docs/COMPLIANCE.md` e a matriz de dados sensiveis cobrindo exatamente o catalogo.
- `docs/REQUIREMENTS_TRACEABILITY.md` atualizado para apontar compliance como artefato rastreavel.
- `docs/EXECUTION_PLAN.md` atualiza Producao/compliance para 28% e substitui pendencias genericas por proximos passos operacionais.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest -q tests/test_compliance_matrix.py`: 3 testes aprovados.
- `python3 -m json.tool config/compliance/data_classification.json`: aprovado.
- `python3 scripts/validate_repository.py`: aprovado para 25 modulos, 9 apps e controles centrais.
- `python3 scripts/scaffold_modules.py --check`: 456 artefatos verificados e 12 customizados preservados.
- `python3 scripts/validate_openapi.py`: aprovado para 25 modulos e operacoes minimas.
- `python3 -m compileall -q scripts tests/test_compliance_matrix.py`: aprovado.
- `.venv/Scripts/python.exe -m pytest -q`: 151 testes aprovados, 29 ignorados.

### Pendencias rastreadas

- Criar fluxo operacional de direitos do titular.
- Registrar DPIA assinada para modulos criticos.
- Adicionar scans SAST/SCA/DAST obrigatorios no CI.

### Git

- Incremento pronto para commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-05-31 Metricas Prometheus Da Outbox

### Concluido neste ciclo

- Dispatcher da outbox ganhou coleta de metricas operacionais via `collect_metrics()`.
- Worker `workers.outbox_dispatcher.main` agora aceita `--metrics` e imprime Prometheus text.
- Metricas expostas: pendentes, pendentes prontos para retry, publicados, tentativas `failed_retryable`, maior `retry_count` e idade do pendente mais antigo.
- `docs/EVENTS.md` e `docs/OPERATIONS.md` documentam coleta e sinais de alerta.
- `docs/EXECUTION_PLAN.md` atualiza Mensageria/outbox para 86% e troca a pendencia generica de metricas por dashboards/alertas reais.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest -q tests/test_outbox_dispatcher_unit.py tests/test_outbox_rabbitmq_integration.py`: 9 testes aprovados, 2 ignorados por dependerem de DSN PostgreSQL/RabbitMQ de integracao.
- `python3 -m compileall -q modules/shared/outbox_dispatcher.py workers/outbox_dispatcher/main.py tests/test_outbox_dispatcher_unit.py`: aprovado.
- `python3 scripts/scaffold_modules.py --check`: 456 artefatos verificados e 12 customizados preservados.
- `python3 scripts/validate_repository.py`: aprovado para 25 modulos, 9 apps e controles centrais.
- `python3 scripts/validate_openapi.py`: aprovado para 25 modulos e operacoes minimas.
- `.venv/Scripts/python.exe -m pytest -q`: 148 testes aprovados, 29 ignorados.

### Pendencias rastreadas

- Conectar as metricas Prometheus text a dashboards/alertas reais por ambiente.
- Validar eventos reais de todos os modulos com dispatcher em PostgreSQL/RabbitMQ vivo.

### Git

- Incremento pronto para commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-05-31 Retry Observavel Da Outbox

### Concluido neste ciclo

- Dispatcher da outbox passou a filtrar eventos `pending` por `next_retry_at`, evitando republicacao antes da janela de backoff.
- Falhas de publicacao continuam registrando entrega append-only `failed_retryable`.
- Evento original permanece `pending` e recebe em `metadata`: `retry_count`, `retry_delay_seconds`, `next_retry_at`, `last_error_type`, `last_error` e `retryable`.
- Backoff exponencial configuravel por `ALL_IN_ONE_OUTBOX_RETRY_BASE_SECONDS` e `ALL_IN_ONE_OUTBOX_RETRY_MAX_SECONDS`.
- `docs/EVENTS.md` e `docs/OPERATIONS.md` documentam o comportamento operacional e os sinais de alerta.
- `docs/EXECUTION_PLAN.md` atualiza Mensageria/outbox para 84% e remove a pendencia de retry/backoff observavel.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest -q tests/test_outbox_dispatcher_unit.py tests/test_outbox_rabbitmq_integration.py`: 8 testes aprovados, 2 ignorados por dependerem de DSN PostgreSQL/RabbitMQ de integracao.
- `python3 -m compileall -q modules/shared/outbox_dispatcher.py tests/test_outbox_dispatcher_unit.py`: aprovado.
- `python3 scripts/scaffold_modules.py --check`: 456 artefatos verificados e 12 customizados preservados.
- `python3 scripts/validate_repository.py`: aprovado para 25 modulos, 9 apps e controles centrais.
- `python3 scripts/validate_openapi.py`: aprovado para 25 modulos e operacoes minimas.
- `.venv/Scripts/python.exe -m pytest -q`: 147 testes aprovados, 29 ignorados.

### Pendencias rastreadas

- Criar dashboards e alertas reais para fila acumulada, eventos com `next_retry_at` vencido e crescimento de `retry_count`.
- Validar eventos reais de todos os modulos com o dispatcher em ambiente PostgreSQL/RabbitMQ vivo.

### Git

- Incremento pronto para commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-05-31 Correlacao De Eventos E Auditoria

### Concluido neste ciclo

- Runtime FastAPI passou a aceitar `X-Correlation-Id` UUID em mutacoes modernas e rotas legadas.
- Quando o cabecalho nao e enviado, o runtime gera um UUID por requisicao antes de gravar auditoria e outbox.
- Cabecalho `X-Correlation-Id` invalido e rejeitado pelo FastAPI com `422`, antes da mutacao.
- Store SQLite contratual grava `correlation_id` em `audit_events` e `domain_events`.
- Stores PostgreSQL principais e `BasePostgresStore` passaram a inserir `correlation_id` explicitamente em `audit.domain_events`.
- `docs/EVENTS.md` documenta a regra de correlacao e rastreabilidade sem expor payload sensivel.
- `docs/EXECUTION_PLAN.md` atualiza Mensageria/outbox de 80% para 82% e remove a pendencia de garantir `correlation_id`.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest -q tests/test_correlation_id.py tests/test_user_marketplace_journey.py tests/test_operational_journeys.py tests/test_outbox_dispatcher_unit.py`: 15 testes aprovados.
- `python3 -m compileall -q modules/shared tests/test_correlation_id.py platform_test_support.py`: aprovado.
- `python3 scripts/scaffold_modules.py --check`: 456 artefatos verificados e 12 customizados preservados.
- `python3 scripts/validate_repository.py`: aprovado para 25 modulos, 9 apps e controles centrais.
- `python3 scripts/validate_openapi.py`: aprovado para 25 modulos e operacoes minimas.
- `.venv/Scripts/python.exe -m pytest -q`: 145 testes aprovados, 29 ignorados.

### Pendencias rastreadas

- Ampliar cobertura de eventos reais por todos os modulos e criar dashboards/alertas de outbox parada, fila acumulada e erro de publish.
- Propagar `correlation_id` para chamadas internas entre servicos vivos quando o API Hub proxy operacional estiver ativo.

### Git

- Incremento pronto para validacao completa, commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-05-31 Gate Scaffold E Pytest Mandatorio

### Concluido neste ciclo

- `scripts/scaffold_modules.py --check` corrigido para reconhecer artefatos customizados intencionais, evitando falha falsa no CI quando arquivos especializados substituem o scaffold generico.
- Template de `requirements.txt` do scaffold atualizado para refletir o baseline real com PostgreSQL/`psycopg` nos modulos.
- Dependencias especiais de Identity, Jobs e API Hub preservadas no scaffold sem apagar os extras necessarios.
- Gate de scaffold agora relata e valida artefatos customizados preservados em secao propria, separando especializacoes intencionais de drift real.
- Configuracao mandatoria de pytest e interpretador Python verificada pelo reposititorio: `pytest.ini` centraliza `--import-mode=importlib` e `--basetemp=.pytest_tmp`; VS Code aponta para `.venv/Scripts/python.exe`.
- O comando simples `.venv/Scripts/python.exe -m pytest -q` passou sem o aviso ambiental de `pytest-current`.

### Validacoes executadas

- `python3 scripts/scaffold_modules.py --check`: 456 artefatos verificados e 12 customizados preservados.
- `python3 scripts/validate_repository.py`: aprovado para 25 modulos, 9 apps e controles centrais.
- `python3 scripts/validate_openapi.py`: aprovado para 25 modulos e operacoes minimas.
- `python3 -m compileall -q modules scripts platform_test_support.py`: aprovado.
- `.venv/Scripts/python.exe -m pytest -q`: 142 testes aprovados, 29 ignorados, sem `PermissionError` no cleanup.

### Pendencias rastreadas

- Observar a proxima execucao do GitHub Actions para confirmar que o job `CI / python` deixa de falhar em `scaffold_modules.py --check`.
- Nao ha workflow run associado ao commit `7846584` nos remotos consultados ate o fechamento deste ciclo.

### Git

- Incremento `7846584` sincronizado em `origin/main` e `fork/main`; novo incremento do relatorio de customizados em preparacao.

## STATUS OPERACIONAL - 2026-05-31 Catalogo Valley Super App Regionalizado

### Concluido neste ciclo

- Helper `modules/shared/valley_catalog.py` criado para normalizar ofertas Valley em linguagem de consumidor.
- Endpoints `GET /valley/catalog/modules`, `/categories`, `/offers` e `/search` registrados no runtime comum.
- Ofertas agora distinguem `offer_type` entre `food`, `product` e `service`.
- Categorias amigaveis criadas para esconder a complexidade tecnica dos modulos na primeira camada de navegacao.
- Busca regional implementada com Haversine usando `lat`, `lng` do usuario, `service_radius_km` e coordenadas publicas da empresa/prestador.
- Ofertas locais fora do raio ou sem cadastro regional completo deixam de aparecer como disponiveis na busca por localizacao.
- Ofertas `online` e `national` continuam visiveis sem depender de raio regional.
- Fallback `coming_soon` garante visibilidade dos 25 modulos no Super App Valley.
- Outbox recebeu allowlist segura para `valley.catalog.offer.synced`, sem expor custo interno, margem, markup ou endereco sensivel.
- `docs/VALLEY_CATALOG.md` documenta contrato, taxonomia amigavel e regra regional.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_valley_catalog.py tests/test_valley_ecosystem.py tests/test_outbox_dispatcher_unit.py`: 13 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 142 testes aprovados, 29 ignorados.
- `python3 scripts/validate_repository.py`: aprovado para 25 modulos, 9 apps e controles centrais.
- `python3 scripts/validate_openapi.py`: aprovado para 25 modulos e operacoes minimas.
- Observacao ambiental: pytest Windows continua emitindo `PermissionError` no cleanup de `pytest-current` apos a suite verde, sem alterar codigo de saida.

### Pendencias rastreadas

- Centralizar agregacao multi-servico real no API Hub para consultar ofertas vivas de todos os modulos em uma unica chamada.
- Persistir snapshots de catalogo e eventos `valley.catalog.offer.synced` quando houver banco dedicado do agregador Valley.
- Implementar interface visual do app Valley usando as categorias amigaveis e filtros regionais.

### Git

- Incremento pronto para validacao completa, commit e push automatico.

## STATUS OPERACIONAL - 2026-05-31 Ledger Gold Valley Finance

### Concluido neste ciclo

- Finance recebeu a entidade `valley_gold_ledger_entries` para lastrear compra e uso de Gold Valley em ledger separado do ledger financeiro BRL/NEX.
- Migration PostgreSQL `015_valley_gold_ledger.sql` adicionada com tabela append-only, idempotencia unica, checks de credito/debito e trigger contra `UPDATE`/`DELETE`.
- Runtime comum passou a exigir `X-Idempotency-Key` para lancamentos Gold Valley e bloquear automacao de concessao de Pepitas.
- Validacao de dominio Gold Valley criada para aceitar credito positivo de compra, debito negativo por concessao manual de Pepitas e ajuste manual controlado.
- Endpoint `GET /valley/gold/balance` criado no Finance para expor saldo Gold derivado exclusivamente da soma do ledger, sem saldo mutavel como fonte de verdade.
- Dispatcher de outbox recebeu allowlist segura para `valley.gold.ledger.posted`, sem publicar taxa interna, anotacao privada ou payload nao revisado.
- Contratos e docs do modulo Finance atualizados com a nova entidade, evento e regra append-only.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_valley_gold_ledger.py tests/test_outbox_dispatcher_unit.py tests/test_valley_ecosystem.py`: 11 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 138 testes aprovados, 29 ignorados.
- `python3 scripts/validate_repository.py`: aprovado para 25 modulos, 9 apps e controles centrais.
- `python3 scripts/validate_openapi.py`: aprovado para 25 modulos e operacoes minimas.
- Observacao ambiental: pytest Windows continua emitindo `PermissionError` no cleanup de `pytest-current` apos a suite verde, sem alterar codigo de saida.

### Pendencias rastreadas

- Conectar `valley_gold_ledger_entries` a fluxo operacional de compra de Gold com PSP/Pix real.
- Debitar Gold automaticamente somente como consequencia auditada da concessao manual de Pepitas, preservando a decisao humana do lojista.
- Criar telas Valley Business para compra de Gold, historico append-only e concessao manual de Pepitas.

### Git

- Incremento pronto para commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-05-31 Reforco Valley Outbox E ACL Essencial

### Concluido neste ciclo

- Dispatcher de outbox ampliado com allowlist segura para eventos Valley de `pepita_grants` e `discount_quotes`.
- Evento `valley.pepitas.granted` agora publica somente dados operacionais necessarios para notificacao do consumidor, sem expor ledger privado Gold, observacoes internas ou payload nao revisado.
- Evento `valley.stock.discount.quoted` agora publica somente campos seguros da cotacao progressiva de desconto, preservando a regra de nao comunicar custo, margem, preco original sensivel ou markup.
- Jornada Valley de concessao manual de Pepitas reforcada com prova de idempotencia por `X-Idempotency-Key`.
- Regra comercial de Pepitas reforcada para bloquear quantidades fora dos pacotes permitidos `1`, `10` e `100`.
- Plano Valley Business Essencial reforcado para bloquear integracoes externas em loja vinculada a CNPJ unico.
- As regras implementadas continuam alinhadas ao documento mestre Valley: Pepitas concedidas manualmente pelo lojista, desconto Stock progressivo por saldo e Marketplace Business restrito a operacao local.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_valley_ecosystem.py tests/test_outbox_dispatcher_unit.py`: 8 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 135 testes aprovados, 29 ignorados.
- `python3 scripts/validate_repository.py`: aprovado para 25 modulos, 9 apps e controles centrais.
- `python3 scripts/validate_openapi.py`: aprovado para 25 modulos e operacoes minimas.
- Observacao ambiental: pytest Windows continua emitindo `PermissionError` no cleanup de `pytest-current` apos a suite verde, sem alterar codigo de saida.

### Pendencias rastreadas

- Integrar ledger Gold append-only real ao Finance para lastrear compra/uso de Gold sem automatizar concessao de Pepitas.
- Persistir notificacoes ao consumidor em canal operacional real quando RabbitMQ/outbox estiver conectado ao frontend Valley.
- Conectar Valley, Valley Business e Valley Rider a telas funcionais e Playwright desktop/mobile.
- Homologar providers reais sem romper restricoes do Plano Essencial e sem expor dados internos de margem/custo.

### Git

- Incremento pronto para commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-05-31 Endpoints Sandbox De Integracao

### Concluido neste ciclo

- Endpoints administrativos `/integrations/sandbox/*` adicionados ao runtime comum para expor adapters sandbox nos modulos prioritarios.
- Identity, Riders e Services agora expoem KYC pessoa sandbox.
- Business expoe KYB empresa sandbox.
- Finance expoe Pix authorize, escrow create e escrow release sandbox.
- ERP expoe emissao fiscal sandbox.
- Jobs expoe classificacao CTPS hash-only sandbox.
- Delivery, Mobility e TMS expoem rota/distancia/ETA sandbox.
- Health expoe consentimento clinico sandbox.
- API Hub expoe assinatura de webhook e verificacao de API key por hash.
- Stock expoe importacao de produto fornecedor sandbox.
- Rotas exigem papel operacional/compliance por `X-Actor-Roles`, evitando endpoints publicos de simulacao sensivel.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_integration_sandbox_routes.py`: 2 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_integration_sandbox_routes.py tests/test_integration_sandbox_adapters.py tests/test_integration_provider_matrix.py`: 7 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 132 testes aprovados, 29 ignorados.

### Pendencias rastreadas

- Persistir resultados sandbox como recursos/auditoria quando o fluxo de produto exigir historico operacional.
- Separar configuracao de `sandbox`, `homologacao` e `producao`.
- Implementar adapters reais com testes de contrato por provedor.

### Git

- Incremento pronto para validacao completa, commit e push automatico.

## STATUS OPERACIONAL - 2026-05-31 Adapters Sandbox De Integracao

### Concluido neste ciclo

- Camada `modules/shared/integration_sandbox.py` criada para transformar a matriz de integracoes em adapters sandbox executaveis.
- Adapters implementados para KYC/KYB, PSP/Pix/escrow, fiscal, CTPS hash-only, mapas/rotas/ETA, consentimento clinico, API Hub/webhooks/API key e catalogo fornecedor.
- Todos os adapters sao deterministicos, nao fazem chamadas externas e nao exigem segredos reais.
- Dados sensiveis brutos sao reduzidos a hash nos fluxos de identidade, fiscal, API key e CTPS.
- `docs/INTEGRATION.md` atualizado com a secao de adapters sandbox e regras de uso.
- `docs/EXECUTION_PLAN.md` atualizado para refletir integracoes externas em 34%.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_integration_sandbox_adapters.py tests/test_integration_provider_matrix.py`: 5 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_operational_journeys.py tests/test_integration_sandbox_adapters.py tests/test_integration_provider_matrix.py`: 10 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 130 testes aprovados, 29 ignorados.
- `python3 scripts/validate_repository.py`: aprovado.
- `python3 scripts/validate_openapi.py`: aprovado.

### Pendencias rastreadas

- Conectar adapters sandbox aos endpoints/fluxos dos modulos prioritarios.
- Separar `sandbox`, `homologacao` e `producao` por configuracao operacional.
- Implementar adapters reais por provedor quando houver credenciais de sandbox/homologacao.

### Git

- Incremento pronto para validacao completa, commit e push automatico.

## STATUS OPERACIONAL - 2026-05-31 Matriz De Integracoes Externas Sandbox

### Concluido neste ciclo

- Matriz versionada de integracoes criada em `config/integrations/provider_matrix.json`.
- A matriz cobre KYC/KYB, Pix/PSP/split/escrow, fiscal NFS-e/NF-e, CTPS, mapas/rotas/tracking, saude/telemedicina/prescricao, OAuth/webhooks/API Hub e catalogo de fornecedores.
- Cada integracao define modulos consumidores, adapter sandbox local, candidatos primarios/fallback, variaveis de ambiente, eventos, dados sensiveis, entrada de menor custo e gate minimo de producao.
- `docs/INTEGRATION.md` expandido com convencoes, ordem de homologacao e politica de menor custo.
- Teste `tests/test_integration_provider_matrix.py` adicionado para garantir cobertura dos modulos criticos e evitar versionamento de segredos reais.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_integration_provider_matrix.py`: 1 teste aprovado.
- `python3 -m json.tool config/integrations/provider_matrix.json`: aprovado.
- `python3 scripts/validate_repository.py`: aprovado.
- `python3 scripts/validate_openapi.py`: aprovado.

### Pendencias rastreadas

- Implementar adapters sandbox reais para os provedores prioritarios.
- Separar ambientes `sandbox`, `homologacao` e `producao` por modulo.
- Adicionar testes de contrato por provider assim que houver credenciais de sandbox.

### Git

- Incremento pronto para commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-05-31 Jornadas Operacionais Delivery Riders Services Mobility Health

### Concluido neste ciclo

- Suite `tests/test_operational_journeys.py` criada com 5 novas jornadas contratuais locais.
- Jornada Delivery cobre cotacao, criacao de solicitacao transacional, atribuicao de rider, coleta, conclusao e evento `delivery.completed` na outbox.
- Jornada Riders cobre onboarding de perfil, submissao documental, aprovacao com MFA, ativacao e cadastro de veiculo.
- Jornada Services cobre cadastro/aprovacao de prestador, contrato com escrow referenciado, aceite, conclusao e evento `services.contract.completed`.
- Jornada Mobility cobre calculo de tarifa, solicitacao de corrida, aceite com motorista, conclusao, emissao de ticket e uso de QR token.
- Jornada Health cobre cadastro de paciente, bloqueio de acesso indevido a dado sensivel, acesso medico autorizado, agendamento, aprovacao e conclusao de consulta.
- Foram usadas referencias opacas em payloads protegidos para respeitar a politica anti-burla sem enfraquecer validacoes.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_operational_journeys.py -vv`: 5 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_user_marketplace_journey.py tests/test_operational_journeys.py tests/test_business_jobs_journey.py`: 7 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 122 testes aprovados, 29 ignorados.
- `python3 scripts/validate_repository.py`: aprovado.
- `python3 scripts/validate_openapi.py`: aprovado.

### Pendencias rastreadas

- Levar as 7 jornadas contratuais locais para Playwright desktop/mobile quando houver shell frontend funcional.
- Avancar para integracoes externas homologadas e adapters sandbox dos provedores prioritarios.
- Resolver aviso ambiental do pytest Windows no cleanup de `pytest-current`, que ocorre apos a suite verde e nao altera o codigo de saida.

### Git

- Incremento pronto para commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-05-30 Ambiente Dev Persistente

### Concluido neste ciclo

- Configuracao persistente do workspace VS Code criada/expandida com extensoes recomendadas para Python, Pylance, debug, Docker, PowerShell, YAML, GitHub Actions, GitHub PRs, GitLens, WSL e Kubernetes.
- Settings do VS Code adicionados para usar `.venv/Scripts/python.exe`, pytest com `--import-mode=importlib`, validacao YAML, EOL LF e perfis PowerShell/Git Bash.
- Tasks do VS Code adicionadas para bootstrap de ambiente, pytest completo, validacao do repositorio, validacao OpenAPI e healthcheck Docker Compose.
- Script `scripts/bootstrap_dev_environment.ps1` criado para instalar/verificar ferramentas Windows via Winget, instalar extensoes VS Code e reinstalar dependencias Python de todos os `requirements.txt`.
- PATH persistente do usuario atualizado para incluir Git for Windows, PowerShell 7 e Docker Desktop.
- `scripts/git_auto_sync.ps1` endurecido para localizar Git em caminhos padrao do Windows quando `git` nao estiver no PATH do PowerShell.

### Ferramentas verificadas no ambiente Windows

- `git`: `C:\Program Files\Git\cmd\git.exe`.
- `pwsh`: `C:\Program Files\PowerShell\7\pwsh.exe`.
- `docker`: `C:\Program Files\Docker\Docker\resources\bin\docker`.
- `gh`: `C:\Users\ereta\.local\bin\gh`.
- `code`: `C:\Users\ereta\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd`.

### Pendencias rastreadas

- Reabrir terminais antigos para herdarem o PATH persistente atualizado.
- Reexecutar instalacao de extensoes diretamente no VS Code caso o CLI `code` continue bloqueado por sessao remota aberta.

### Git

- Incremento pronto para commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-05-30 Jornada Business Jobs E Isolamento De Testes

### Concluido neste ciclo

- Segunda jornada E2E local de produto criada em `tests/test_business_jobs_journey.py`.
- Jornada cobre criacao de empresa Business, aprovacao KYB operacional, publicacao de vaga Jobs, listagem publica de vagas, criacao de curriculo, candidatura e controle de acesso ao curriculo por recrutador autorizado.
- `platform_test_support.py` recebeu `fresh_client_for`, preservando `client_for` cacheado e permitindo testes de jornada com apps isolados por execucao.
- Jornada `identity -> wallet -> marketplace order` atualizada para usar cliente fresco e evitar interferencia de estado entre a suite completa e os fluxos integrados.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_user_marketplace_journey.py tests/test_business_jobs_journey.py`: 2 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 117 testes aprovados, 29 ignorados.
- `python3 scripts/validate_repository.py`: aprovado.
- `python3 scripts/validate_openapi.py`: aprovado.

### Pendencias rastreadas

- Expandir jornadas E2E para delivery, riders, services, health e mobility.
- Levar as jornadas contratuais para Playwright desktop/mobile quando houver shell frontend funcional.
- Resolver aviso ambiental do pytest Windows no cleanup de `pytest-current`, que ocorre apos a suite verde e nao altera o codigo de saida.

### Git

- Incremento pronto para commit e push automatico em `origin/main` e `fork/main`.

## STATUS OPERACIONAL - 2026-05-30 Resolucao Worktree E Jornada User Marketplace

### Concluido neste ciclo

- Worktree auxiliar `all-in-one-auto-sync` corrigido: ponte `.git` normalizada para caminho WSL valido e merge pendente removido por alinhamento ao `origin/main`.
- Backup do branch auxiliar antigo preservado em `codex/all-in-one-current-sync-backup-20260530` antes do alinhamento.
- Branch auxiliar `codex/all-in-one-current-sync` atualizado para rastrear `origin/main` e sair do estado `unmerged`.
- `main`, `origin/main`, `fork/main` e o worktree auxiliar alinhados no commit `8d0360a`.
- Primeira jornada E2E local de produto criada em `tests/test_user_marketplace_journey.py`.
- Jornada cobre cadastro Identity, criacao de wallet Finance, consulta de wallets, criacao de escrow, criacao de pedido Marketplace, transicao de pedido para `paid` e verificacao de evento `marketplace.order.paid` na outbox.

### Validacoes executadas

- `git status` no worktree principal: limpo e alinhado com `origin/main`.
- `git status` no worktree auxiliar: limpo e alinhado com `origin/main`.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_user_marketplace_journey.py`: 1 teste aprovado.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 116 testes aprovados, 29 ignorados.
- `python3 scripts/validate_repository.py`: aprovado.
- `python3 scripts/validate_openapi.py`: aprovado.

### Pendencias rastreadas

- Ampliar jornadas E2E para `business -> jobs -> candidate access` e demais apps.
- Resolver aviso ambiental do pytest Windows no cleanup de `pytest-current`, que ocorre apos a suite verde e nao muda o codigo de saida.

### Git

- Sincronizacao remota concluida para `origin/main` e `fork/main`.
- Novo incremento de jornada pronto para commit e push automatico.

## STATUS OPERACIONAL - 2026-05-30 API Hub E Gate De Artefatos

### Concluido neste ciclo

- GitHub verificado novamente: `origin/main` e `fork/main` permanecem alinhados em `6f3ddf9`; nao havia commits novos na nuvem para aplicar localmente.
- API Hub avancado com validacao de API key em `/gateway/api-key/check`, configurada por `ALL_IN_ONE_API_KEYS`.
- API Hub avancado com verificacao de assinatura HMAC SHA-256 em `/gateway/webhooks/verify`, configurada por `ALL_IN_ONE_WEBHOOK_SECRET`.
- `rate_limiter` mantido com Redis quando disponivel e modo degradado para ambientes locais sem pacote `redis`, permitindo carregar e testar rotas nao dependentes de Redis real.
- Validador JWT do gateway passou a reportar `503` quando a dependencia `jwt` nao estiver instalada, sem impedir rotas abertas/API key/webhook em testes locais.
- Contrato OpenAPI do API Hub atualizado com rotas de gateway, API key e webhook assinado.
- Testes de gateway adicionados em `modules/api_hub/tests/test_gateway_security.py`, cobrindo API key valida, API key ausente/invalida/sem escopo, webhook assinado e bloqueio de rate limit.
- Gate de artefatos gerados criado em `scripts/check_generated_artifacts.ps1` e incluido no workflow `.github/workflows/ci.yml`.
- `scripts/validate_repository.py` atualizado para exigir os gates operacionais versionados.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q modules/api_hub/tests/test_gateway_security.py`: 4 testes aprovados.
- `python3 scripts/validate_repository.py`: aprovado.
- `python3 scripts/validate_openapi.py`: aprovado.
- `python3 -m compileall -q modules/api_hub scripts platform_test_support.py`: aprovado.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 115 testes aprovados, 29 ignorados, 2 avisos Pydantic.

### Pendencias rastreadas

- Executar `scripts/check_generated_artifacts.ps1` em ambiente com PowerShell Core disponivel; este shell local nao possui `pwsh`/`powershell`.
- Instalar/autenticar GitHub CLI ou credencial HTTPS para permitir push local dos commits ja criados.
- Substituir exemplos Pydantic `Field(example=...)` por `json_schema_extra` em `modules/identity/auth_logic.py`.

### Git

- Branch local continua a frente da nuvem ate liberacao de credenciais de push.
- `.vscode/` permanece nao versionado e foi preservado fora dos commits.

## STATUS OPERACIONAL - 2026-05-30 Limpeza Pydantic Identity

### Concluido neste ciclo

- Campos `LoginRequest.email` e `LoginRequest.password` em `modules/identity/auth_logic.py` migrados de `Field(example=...)` para `json_schema_extra`, removendo avisos de depreciacao do Pydantic v2.

### Validacoes executadas

- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q tests/test_identity_jobs_domain.py modules/api_hub/tests/test_gateway_security.py`: 10 testes aprovados.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 115 testes aprovados, 29 ignorados, sem avisos Pydantic.

### Pendencias rastreadas

- O pytest em Windows ainda emite `PermissionError` no callback de limpeza de `pytest-current` depois da suite verde; nao altera o codigo de saida dos testes.

## STATUS OPERACIONAL - 2026-05-30 Sincronizacao GitHub E Gates Operacionais

### Concluido neste ciclo

- GitHub verificado contra os remotos `origin` e `fork`; ambos apontam para `main` em `6f3ddf9`, sem commits novos na nuvem para trazer ao checkout local.
- Checkout local preservado com os 2 commits do memorando ja criados anteriormente, ficando a frente da nuvem ate que credenciais GitHub estejam disponiveis para push HTTPS.
- Gate de divergencia Git criado em `scripts/check_git_sync.ps1`, com deteccao de merge/rebase em andamento, arvore suja e comparacao `behind/ahead` por remoto.
- Gate Docker Compose criado em `scripts/validate_compose_health.ps1`, validando `docker compose config`, subida do ambiente e `/health` das 13 APIs FastAPI principais.
- Workflows CI adicionados em `.github/workflows/git-sync.yml` e `.github/workflows/compose-health.yml`.
- `scripts/validate_repository.py` atualizado para exigir os novos workflows de sincronizacao e Compose health.
- `docs/OPERATIONS.md` atualizado com a operacao dos gates automatizados.
- Teste E2E de Identity ajustado para ser opt-in quando o servico HTTP real nao estiver ativo, pulando explicitamente em ambiente sem Docker Compose em vez de falhar por conexao recusada.

### Validacoes executadas

- `python3 scripts/validate_repository.py`: aprovado.
- `python3 scripts/validate_openapi.py`: aprovado.
- `python3 -m compileall -q scripts platform_test_support.py`: aprovado.
- `docker compose -f infra/docker/docker-compose.yml config --quiet`: aprovado.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q modules/identity/tests/test_e2e_identity.py`: 1 teste ignorado corretamente por servico E2E indisponivel.
- `.venv/Scripts/python.exe -m pytest --import-mode=importlib -q`: 111 testes aprovados, 29 ignorados, 2 avisos Pydantic.

### Pendencias rastreadas

- Executar `scripts/check_git_sync.ps1` e `scripts/validate_compose_health.ps1` em ambiente com PowerShell Core disponivel; este shell local nao possui `pwsh`/`powershell`.
- Resolver credenciais GitHub locais para permitir `git push origin HEAD:main` ou `git push fork HEAD:main`.
- Investigar aviso ambiental do pytest Windows no cleanup de `pytest-current`, que ocorre apos a suite concluir com status verde.

### Git

- Branch local `main` verificada contra `origin/main` e `fork/main`.
- Push automatico continua bloqueado por ausencia de login GitHub no CLI local (`gh auth status`: nao autenticado; `git push`: `could not read Username for 'https://github.com'`).

## STATUS OPERACIONAL - 2026-05-30 Memorando ABNT De Progresso E Mercado

### Concluido neste ciclo

- Status de progresso consolidado em memorando tecnico-comercial no arquivo `docs/memorando_status_mercado_abnt.md`.
- PDF em formato ABNT simplificado gerado em `docs/memorando_status_mercado_abnt.pdf`.
- Levantamento de modulos, servicos e microservicos atualizado com percentual de conclusao, estado tecnico, pendencias e proximos passos naturais.
- Analise comercial incluida com concorrentes no mercado brasileiro, precos publicos/faixas de referencia, estrategia de atracao de clientes e sugestao de precos All-in-One pelo menos 20% abaixo das referencias nacionais quando havia preco publico comparavel.
- Gerador local sem dependencias externas criado em `scripts/generate_abnt_memo_pdf.py` para reproduzir o PDF a partir do Markdown.

### Fontes de mercado consultadas

- Conta Azul, Bling, RD Station CRM, Nuvemshop, Yampi, iFood, Loggi, Uber para Empresas, iClinic, Feegow, Gupy e Solides.
- Quando o concorrente opera com preco sob consulta, o memorando registra a limitacao e usa recomendacao por paridade funcional, sem tratar estimativa como tabela publica.

### Pendencias rastreadas

- Revisar o memorando apos a proxima rodada de validacao tecnica dos stores PostgreSQL.
- Complementar precos sob consulta com cotacoes comerciais reais quando houver contato com fornecedores/concorrentes.
- Converter a estrategia comercial em backlog de go-to-market por modulo.

### Git

- Commit local seletivo criado para os artefatos do memorando.
- Push automatico bloqueado por ausencia de credenciais GitHub no ambiente (`could not read Username for 'https://github.com'`).

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
