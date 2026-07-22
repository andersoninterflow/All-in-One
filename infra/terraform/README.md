# Terraform

Este diretorio reserva infraestrutura como codigo para ambientes homologados.
O baseline cria recursos base de rede, computacao, storage e dados gerenciados.
Para DNS, a criacao e opcional e so acontece quando `dns_zone_name` e
`dns_domain` forem preenchidos.

## DNS (Cloud DNS)

Variaveis:
- `dns_zone_name`: nome da zona gerenciada (RFC1035). Vazio desativa DNS.
- `dns_domain`: dominio raiz da zona (ex.: `example.com`). Vazio desativa DNS.
- `dns_description`: descricao da zona.
- `dns_records`: lista de registros DNS.

Exemplo:

```hcl
dns_zone_name = "all-in-one-zone"
dns_domain    = "example.com"
dns_records = [
  {
    name    = "@"
    type    = "A"
    ttl     = 300
    rrdatas = ["203.0.113.10"]
  },
  {
    name    = "api"
    type    = "CNAME"
    ttl     = 300
    rrdatas = ["gateway.example.com."]
  }
]
```

## Dominio brasildesconto.com.br

Quando houver mudanca de dominio/subdominio para `brasildesconto.com.br`, a
atividade deve seguir `config/autonomy/brasildesconto_domain_policy.json`.
Esse contrato exige Terraform como fonte declarativa, sincronizacao com
Cloudflare e validacao automatica no gate `python3 scripts/validate_repository.py`.
