resource "google_alloydb_cluster" "primary" {
  cluster_id = "all-in-one-cluster"
  location   = var.region
  network_config {
    network = google_compute_network.vpc_network.id
  }
  initial_user {
    user     = "all_in_one"
    password = var.alloydb_password
  }

  depends_on = [google_service_networking_connection.default]
}

resource "google_alloydb_instance" "primary" {
  cluster       = google_alloydb_cluster.primary.name
  instance_id   = "all-in-one-primary-instance"
  instance_type = "PRIMARY"
  
  machine_config {
    cpu_count = 2
  }

  depends_on = [google_service_networking_connection.default]
}
