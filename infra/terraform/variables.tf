variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
  default     = "all-in-one-498012"
}

variable "region" {
  description = "The region to deploy resources in"
  type        = string
  default     = "southamerica-east1"
}

variable "zone" {
  description = "The zone to deploy resources in"
  type        = string
  default     = "southamerica-east1-a"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "alloydb_password" {
  description = "Initial password for the AlloyDB postgres user"
  type        = string
  sensitive   = true
}

variable "dns_zone_name" {
  description = "Cloud DNS managed zone name (RFC1035). Leave empty to skip DNS resources."
  type        = string
  default     = ""
}

variable "dns_domain" {
  description = "DNS root domain for the zone (for example: example.com). Leave empty to skip DNS resources."
  type        = string
  default     = ""
}

variable "dns_description" {
  description = "Description for the Cloud DNS managed zone."
  type        = string
  default     = "Managed DNS zone for All-in-One"
}

variable "dns_records" {
  description = "DNS records to create in the managed zone. Use name '@' for zone apex."
  type = list(object({
    name    = string
    type    = string
    ttl     = number
    rrdatas = list(string)
  }))
  default = []

  validation {
    condition = alltrue([
      for record in var.dns_records :
      contains(["A", "AAAA", "CNAME", "TXT", "MX", "NS", "CAA", "SRV", "PTR"], upper(record.type))
    ])
    error_message = "dns_records[*].type deve ser um tipo DNS suportado (A, AAAA, CNAME, TXT, MX, NS, CAA, SRV, PTR)."
  }

  validation {
    condition = alltrue([
      for record in var.dns_records :
      record.ttl > 0 && length(record.rrdatas) > 0
    ])
    error_message = "dns_records[*] deve ter ttl > 0 e ao menos um valor em rrdatas."
  }
}
