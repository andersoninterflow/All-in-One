# Status Operacional

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
