resource "google_compute_instance" "bastion" {
  name         = "bastion-host"
  machine_type = "e2-micro"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network.name
    subnetwork = google_compute_subnetwork.gke_subnet.name
    # Sem IP externo para segurança, o acesso deve ser via IAP
  }

  service_account {
    scopes = ["cloud-platform"]
  }
}
