# Configuracao de rede privada para servicos gerenciados (AlloyDB, Redis)

resource "google_compute_global_address" "private_ip_alloc" {
  name          = "all-in-one-private-ip-alloc"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc_network.id
}

resource "google_service_networking_connection" "default" {
  network                 = google_compute_network.vpc_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_alloc.name]
}
