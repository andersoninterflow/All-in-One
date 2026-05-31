# Catalogo Valley Super App

O Valley apresenta o ecossistema em linguagem de consumo, sem obrigar o usuario
final a conhecer nomes internos de modulos. Toda oferta agregada deve declarar:

- `offer_type`: `food`, `product` ou `service`.
- `consumer_category`: agrupamento simples exibido ao consumidor.
- `source_module`: modulo tecnico de origem, mantido para auditoria e roteamento.
- `service_radius_km`: raio regional em quilometros quando a oferta for local.
- `region_label`: area amigavel, sem endereco sensivel.

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

- `GET /valley/catalog/modules`
- `GET /valley/catalog/categories`
- `GET /valley/catalog/offers`
- `GET /valley/catalog/search?q=&category=&offer_type=&lat=&lng=`

O evento `valley.catalog.offer.synced` usa allowlist segura no outbox e nao
publica custo interno, margem, markup, endereco sensivel ou observacoes privadas.
