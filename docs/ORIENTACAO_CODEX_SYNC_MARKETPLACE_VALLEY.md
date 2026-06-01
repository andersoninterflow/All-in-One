# Orientacao Codex: Sincronizacao Marketplace Valley

Este documento versiona a diretriz de sincronizacao entre All-in-One Business,
modulos operacionais, Marketplace e Valley.

## Diretriz mestre

Todo produto ou servico configurado no All-in-One Business por PF, MEI, PJ,
franquia ou parceiro integrado pode alimentar o catalogo Marketplace do Valley,
desde que esteja ativo, aprovado, categorizado, precificado ou com regra de
orcamento, disponivel e explicitamente autorizado para publicacao.

O All-in-One opera a retaguarda. O Business concentra configuracao comercial,
documentos, categorias, ramos, precos, disponibilidade e permissao de publicacao.
O Marketplace normaliza ofertas. O Valley apresenta a vitrine em linguagem
simples para o usuario final comprar, contratar, agendar, pagar e acompanhar.

## Regras obrigatorias

- Ofertas reais devem declarar `publish_to_valley = true`.
- Ofertas reais devem ter `publication_status` em `approved` ou `published`.
- Toda oferta deve manter `source_module`, `source_resource_type` e
  `source_entity_id`.
- Toda oferta deve informar `offer_type`, `consumer_category`,
  `company_type`, `company_category` e `business_activity_id`.
- Ofertas locais devem informar `service_area`, `region_label` e
  `service_radius_km` para busca regional.
- Modulos regulados exigem `compliance_status` aprovado ou verificado antes da
  publicacao real.
- O Valley nunca deve expor endereco sensivel, custo interno, margem, markup ou
  observacoes privadas.

## Fontes de catalogo

- Produtos fisicos: `marketplace`, `stock`, `wms`, `erp`.
- Servicos profissionais: `services`, `legal`, `health`, `property`, `hr`,
  `jobs`, `document`.
- Logistica e execucao: `delivery`, `riders`, `mobility`, `tms`, `vision`.
- Financeiro e comercial: `finance`, `crm`, `bi`, `ai_core`, `api_hub`.

## Experiencia do usuario

O Valley deve esconder a complexidade tecnica. A primeira camada usa nomes
amigaveis, como Produtos e lojas, Saude, Servicos para casa, Profissionais,
Advogados e documentos, Cursos, Vagas, Imoveis, Entregas, Restaurantes e
mercados, Pagamentos e beneficios.

Cards e listagens devem priorizar:

- titulo simples;
- descricao curta de ate 160 caracteres;
- categoria compreensivel;
- vendedor ou prestador;
- selo de verificacao quando existir;
- preco ou sob orcamento;
- disponibilidade;
- distancia ou regiao;
- acao principal clara.

## Eventos e outbox

O evento seguro de publicacao para a vitrine e `valley.catalog.offer.synced`.
Ele deve circular apenas com payload publico em allowlist, preservando
`correlation_id` e rejeitando dados internos ou sensiveis.

