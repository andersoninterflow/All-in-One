# Compliance LGPD E Producao

Este documento consolida a primeira matriz operacional de compliance do
All-in-One. A fonte versionada esta em
`config/compliance/data_classification.json` e cobre os 25 modulos do catalogo.
O fluxo operacional de direitos do titular fica em
`config/compliance/data_subject_rights.json`. O contrato dos jobs de retencao,
anonimizacao, descarte e legal hold fica em
`config/compliance/retention_jobs.json`.

## Principios

- Minimizar dados por finalidade, modulo e jornada.
- Separar dados sensiveis brutos de payloads publicos, eventos e mockups.
- Guardar trilhas criticas em auditoria append-only.
- Aplicar retencao por obrigacao legal, contrato, consentimento ou defesa de
  direito.
- Exigir KMS/vault para segredos, documentos, biometria, prontuario, CTPS e
  credenciais.
- Dar suporte aos direitos do titular: acesso, correcao, portabilidade,
  anonimizacao, revogacao de consentimento e exclusao quando legalmente
  permitida.

## Matriz De Dados Sensiveis

| Grupo | Modulos | Risco | Controles minimos |
| --- | --- | --- | --- |
| Identidade e acesso | `identity`, `permissions`, `api_hub` | Critico/alto | DPIA, MFA, KMS/vault, credenciais hash-only, rotacao, testes negativos de permissao |
| Dinheiro, fiscal e empresa | `finance`, `business`, `erp` | Critico/alto | PSP/fiscal homologado, ledger append-only, conciliacao, segregacao de funcoes, backup/restore |
| Trabalho e pessoas | `jobs`, `hr`, `riders` | Critico/alto | Consentimento, cofre documental, retencao trabalhista, auditoria de acessos, validacao documental |
| Saude, documentos e IA | `health`, `document`, `ai_core`, `vision` | Critico | DPIA especifica, KMS, consentimento explicito, retencao curta quando aplicavel, governanca de modelo |
| Operacao local | `delivery`, `services`, `mobility`, `property`, `tms`, `wms` | Alto/medio | Opt-in de localizacao, minimizacao de endereco, POD seguro, retencao operacional, permissao por papel |
| Comercial e analytics | `marketplace`, `stock`, `crm`, `bpm`, `bi`, `legal` | Alto/medio | Anti-burla, opt-out, mascaramento, logs de exportacao, sigilo profissional, controle de margem/custo |

## Gates De Producao

Antes de producao ampla:

1. Validar a matriz `config/compliance/data_classification.json` contra o
   catalogo de modulos.
2. Executar DPIA para modulos `critical` e registrar aprovacao.
3. Homologar DPAs com provedores de KYC/KYB, PSP, fiscal, mapas, saude,
   assinatura, IA e armazenamento.
4. Ativar vault/KMS e rotacao de chaves.
5. Testar direitos do titular por modulo: exportacao, correcao, revogacao,
   anonimizacao e exclusao permitida.
6. Validar backup/restore e retencao para PostgreSQL, MongoDB e storage privado.
7. Rodar pentest, SAST/SCA, DAST e testes negativos de permissao.

## Direitos Do Titular

O atendimento operacional LGPD passa a ter contrato versionado. Cada pedido
deve informar `request_id`, `subject_id`, `right_type`,
`identity_verification_level`, `requested_at` e `source_channel`.

Direitos cobertos:

- Acesso aos dados.
- Correcao de dados.
- Portabilidade.
- Anonimizacao.
- Revogacao de consentimento.
- Exclusao quando legalmente permitida.

Regras obrigatorias:

- Todo fluxo comeca por validacao de identidade.
- Todo fluxo termina com auditoria em
  `compliance.data_subject_request.processed`.
- Saidas publicas nunca incluem segredos reais, chaves privadas, dados de
  cartao, biometria bruta, prontuario de terceiros ou documentos brutos sem
  revalidacao do titular.
- Modulos criticos (`identity`, `finance`, `jobs`, `document`, `hr`,
  `health`, `vision`, `ai_core` e `api_hub`) exigem cobertura completa dos
  direitos e revisao por papel de compliance quando houver dado sensivel.
- Quando houver obrigacao legal, contrato ativo, defesa de direito ou disputa,
  o pedido pode ser parcialmente atendido com justificativa registrada.

## Retencao, Anonimizacao E Descarte

Os jobs operacionais de retencao agora possuem contrato versionado antes da
ativacao produtiva:

- `retention_review_daily`: revisa dados vencidos por politica, contrato ou
  consentimento.
- `anonymization_worker_hourly`: anonimiza dados permitidos apos avaliacao de
  base legal.
- `deletion_worker_daily`: descarta dados excluiveis sem obrigacao legal ou
  disputa ativa.
- `legal_hold_reconciliation_daily`: bloqueia descarte quando houver obrigacao
  legal, fiscal, trabalhista, regulatoria ou defesa de direito.

Cada modulo declara acao padrao, razoes de legal hold, job minimo e dominio de
evidencia. Descartes produtivos exigem dry-run inicial, auditoria imutavel e
revisao legal para registros financeiros, fiscais, medicos, trabalhistas ou
contratos assinados.

## Evidencia Atual

- `docs/SECURITY.md` descreve controles implementados e obrigatorios.
- `config/integrations/provider_matrix.json` inclui gates de producao por
  provedor externo.
- `config/compliance/data_classification.json` versiona a classificacao de
  dados, base legal, retencao e gates por modulo.
- `config/compliance/data_subject_rights.json` versiona SLA, workflow,
  evidencias, guardrails e cobertura por modulo para direitos do titular.
- `config/compliance/retention_jobs.json` versiona jobs de retencao,
  anonimizacao, descarte e legal hold por modulo.
- `tests/test_compliance_matrix.py` bloqueia ausencia de modulo, campos
  obrigatorios e classificacao invalida.
- `tests/test_data_subject_rights.py` bloqueia ausencia de direito, SLA
  invalido, modulo sem cobertura e exportacao de dados proibidos.
- `tests/test_retention_jobs.py` bloqueia ausencia de job, modulo sem regra,
  evidencia fraca e descarte destrutivo sem revisao legal.

## Pendencias

- Implementar workers reais de retencao, anonimizacao e descarte a partir do
  contrato versionado.
- Gerar evidencias de DPIA assinadas por modulo critico.
- Integrar scans SAST/SCA/DAST obrigatorios ao CI com severidade bloqueante.
