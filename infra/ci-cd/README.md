# CI/CD

Os workflows GitHub executam os gates de codigo, banco, OpenAPI e seguranca.
`autocommit.yml` somente sincroniza artefatos gerados quando disparado
manualmente; `automerge.yml` exige label explicita e checks bem-sucedidos.
