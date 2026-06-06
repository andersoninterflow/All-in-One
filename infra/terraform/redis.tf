resource "google_redis_instance" "primary" {
  name           = "all-in-one-redis"
  tier           = "BASIC"
  memory_size_gb = 1
  region         = var.region

  authorized_network = google_compute_network.vpc_network.id
  connect_mode       = "PRIVATE_SERVICE_ACCESS"

  depends_on = [google_service_networking_connection.default]
}
