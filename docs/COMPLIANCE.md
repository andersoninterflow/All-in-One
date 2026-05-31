# Compliance LGPD E Producao

Este documento consolida a primeira matriz operacional de compliance do
All-in-One. A fonte versionada esta em
`config/compliance/data_classification.json` e cobre os 25 modulos do catalogo.

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

## Evidencia Atual

- `docs/SECURITY.md` descreve controles implementados e obrigatorios.
- `config/integrations/provider_matrix.json` inclui gates de producao por
  provedor externo.
- `config/compliance/data_classification.json` versiona a classificacao de
  dados, base legal, retencao e gates por modulo.
- `tests/test_compliance_matrix.py` bloqueia ausencia de modulo, campos
  obrigatorios e classificacao invalida.

## Pendencias

- Criar fluxo operacional de direitos do titular.
- Conectar retencao a jobs de anonimizacao e descarte.
- Gerar evidencias de DPIA assinadas por modulo critico.
- Integrar scans SAST/SCA/DAST obrigatorios ao CI com severidade bloqueante.
