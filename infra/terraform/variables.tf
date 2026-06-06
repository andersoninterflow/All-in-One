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
