# Catalogo Valley Super App

O Valley apresenta o ecossistema em linguagem de consumo, sem obrigar o usuario
final a conhecer nomes internos de modulos. O All-in-One Business e a retaguarda
onde PF, MEI, PJ, franquias e parceiros configuram produtos e servicos; o
Marketplace normaliza essas configuracoes; o Valley exibe somente ofertas claras,
aprovadas e autorizadas para o consumidor.

Toda oferta agregada deve declarar:

- `offer_type`: `food`, `product` ou `service`.
- `consumer_category`: agrupamento simples exibido ao consumidor.
- `source_module`: modulo tecnico de origem, mantido para auditoria e roteamento.
- `source_entity_id`, `business_id` e `seller_user_id`: origem rastreavel.
- `publish_to_valley` e `publication_status`: controle de publicacao no Valley.
- `company_type`, `company_category` e `business_activity_id`: filtros comerciais.
- `service_radius_km`: raio regional em quilometros quando a oferta for local.
- `region_label`: area amigavel, sem endereco sensivel.
- `primary_action_label`: texto simples como Comprar, Agendar, Contratar ou
  Solicitar.

## Regra de publicacao

Recursos reais vindos do Business e dos modulos Marketplace, Stock, Services,
Health, Delivery, Mobility, Jobs, Property e Finance so entram no catalogo se:

- `publish_to_valley = true`;
- `publication_status` estiver em `approved` ou `published`;
- `visible_to_consumer` nao estiver desativado;
- a oferta nao estiver cancelada, rejeitada, bloqueada, suspensa ou arquivada;
- modulos regulados, como Health, Legal, Finance e Document, tiverem
  `compliance_status` aprovado ou verificado quando a oferta real for publicada.

O recurso `business/catalog_offers` e a configuracao comercial canonica para PF,
MEI e PJ. Ele guarda a decisao do usuario Business de publicar no Valley e aponta
para o modulo tecnico de execucao por `source_module` e `source_resource_type`,
por exemplo `marketplace/products`, `services/providers` ou
`health/appointments`.

Modulos sem oferta operacional continuam aparecendo como `coming_soon`, para que
o usuario entenda o ecossistema sem confundir promessa futura com oferta
contratavel.

## Categorias amigaveis

- `Comida e Mercado`: delivery, restaurantes, mercado e alimentos.
- `Compras e Produtos`: produtos fisicos, digitais, cursos e assinaturas.
- `Saude e Bem-estar`: consultas, psicologia, odontologia e cuidado clinico.
- `Casa, Reparos e Imoveis`: reparos, manutencao, imoveis e servicos locais.
- `Mobilidade, Entregas e Logistica`: corridas, entregas, fretes e transporte.
- `Negocios e Profissionais`: juridico, contabilidade, recrutamento e gestao.
- `Beneficios, Wallet e Recompensas`: Pepitas, Gold, descontos e fidelidade.
- `Tecnologia, Seguranca e IA`: cameras, integracoes, automacoes e IA.

## Regionalizacao

Ofertas locais devem informar coordenadas publicas de base operacional e
`service_radius_km`. A busca `GET /valley/catalog/search` calcula distancia por
Haversine quando o consumidor envia `lat` e `lng`.

Regras:

- Oferta local dentro do raio aparece com `distance_km`.
- Oferta local fora do raio nao aparece na busca regional.
- Oferta local sem raio completo nao aparece como disponivel para localizacao.
- Oferta `online` ou `national` aparece independentemente da localizacao.
- O app mostra apenas `region_label` e distancia aproximada, nunca endereco
  sensivel do prestador ou lojista.

## Endpoints

- `GET /valley/catalog`
- `GET /valley/catalog/modules`
- `GET /valley/catalog/categories`
- `GET /valley/catalog/business-activities`
- `GET /valley/catalog/facets`
- `GET /valley/catalog/offers`
- `GET /valley/catalog/offers/{offer_id}`
- `GET /valley/catalog/search?q=&category=&offer_type=&lat=&lng=`

A busca tambem aceita `company_type`, `company_category`, `business_activity`,
`price_min`, `price_max`, `availability` e `verified_only`.

## Ramos de atividade

O catalogo mantem uma referencia inicial de ramos comerciais com nome para o
negocio e rotulo simples para o consumidor. Exemplos:

- `alimentacao`: Restaurantes e mercados.
- `varejo`: Produtos e lojas.
- `saude`: Saude e bem-estar.
- `servicos_domesticos`: Casa e manutencao.
- `juridico`: Advogados e documentos.
- `educacao`: Cursos e aulas.
- `logistica`: Entregas e transportes.
- `imobiliario`: Imoveis e condominio.
- `empregos`: Vagas e carreira.
- `financeiro`: Pagamentos e credito.
- `tecnologia`: Tecnologia e automacao.

O evento `valley.catalog.offer.synced` usa allowlist segura no outbox e nao
publica custo interno, margem, markup, endereco sensivel ou observacoes privadas.
