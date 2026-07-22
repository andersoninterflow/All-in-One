# Changelog

## 0.1.1 - 2026-07-22

- Adicionada politica versionada `config/autonomy/brasildesconto_domain_policy.json`
  para diretriz permanente do dominio `brasildesconto.com.br`.
- Adicionado `scripts/validate_brasildesconto_domain_policy.py` e integracao no
  `scripts/validate_repository.py` para validar automaticamente o contrato.
- Atualizada documentacao operacional (README, DEPLOYMENT e OPERATIONS) para
  explicitar o fluxo obrigatorio de sincronizacao IaC + Cloudflare.

## 0.1.0 - 2026-05-25

- Inicializacao do monorepo All-in-One.
- Adicao dos apps, modulos FastAPI, contratos, schemas de banco e runtime comum.
- Adicao de infraestrutura, CI/CD, documentacao e validacoes de baseline.
