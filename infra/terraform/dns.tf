locals {
  dns_enabled     = var.dns_zone_name != "" && var.dns_domain != ""
  dns_domain_root = trimsuffix(var.dns_domain, ".")
  dns_domain_fqdn = "${local.dns_domain_root}."

  dns_records_normalized = local.dns_enabled ? [
    for record in var.dns_records : {
      key = format(
        "%s|%s|%d",
        lower(record.name),
        upper(record.type),
        record.ttl
      )
      name = record.name == "@" ? local.dns_domain_fqdn : (
        endswith(record.name, ".") ? record.name : (
          endswith(record.name, local.dns_domain_root) ? "${record.name}." : "${record.name}.${local.dns_domain_fqdn}"
        )
      )
      type    = upper(record.type)
      ttl     = record.ttl
      rrdatas = record.rrdatas
    }
  ] : []
}

resource "google_dns_managed_zone" "primary" {
  count = local.dns_enabled ? 1 : 0

  name        = var.dns_zone_name
  dns_name    = local.dns_domain_fqdn
  description = var.dns_description

  depends_on = [google_project_service.dns]
}

resource "google_dns_record_set" "records" {
  for_each = {
    for record in local.dns_records_normalized : record.key => record
  }

  managed_zone = google_dns_managed_zone.primary[0].name
  name         = each.value.name
  type         = each.value.type
  ttl          = each.value.ttl
  rrdatas      = each.value.rrdatas
}
