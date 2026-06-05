# Business

Matriz, filiais, documentos empresariais, aprovacao manual, memberships e
ofertas comerciais publicaveis no catalogo Valley.

## Responsabilidade

Este microservico e isolado por dominio, mas toda criacao mantem `user_id`
associado ao All-in-One ID. Operacoes mutaveis sao auditadas e exigem o
cabecalho `X-Actor-User-Id`, salvo o autorregistro inicial em Identity.

## Entidades

`companies`, `branches`, `company_documents`, `user_company_memberships`,
`catalog_offers`.

`catalog_offers` e o ponto canônico para PF, MEI ou PJ configurar produto ou
servico que sera normalizado pelo Marketplace e exibido no Valley quando
`publish_to_valley=true`, `publication_status` aprovado/publicado e filtros
publicos estiverem completos.

## Execucao

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

O contrato HTTP esta em `OPENAPI.yaml`; os controles especificos estao
descritos em `CONTRACT.md` e `SECURITY.md`.
