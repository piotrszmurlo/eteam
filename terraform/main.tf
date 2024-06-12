terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_network" "my_network" {
  name = "my_network"
}

resource "docker_image" "frontend_image" {
  name         = "frontend:latest"
  build {
    context    = "../front/"
    dockerfile = "Dockerfile"
  }
}

resource "docker_image" "auth_image" {
  name         = "auth:latest"
  build {
    context    = "../backend/"
    dockerfile = "authentication/Dockerfile"
  }
}

resource "docker_image" "storage_image" {
  name         = "storage:latest"
  build {
    context    = "../backend/"
    dockerfile = "storage/Dockerfile"
  }
}

resource "docker_image" "payment_image" {
  name         = "payment:latest"
  build {
    context    = "../backend/"
    dockerfile = "payment/Dockerfile"
  }
}

resource "docker_image" "notification_image" {
  name         = "notification:latest"
  build {
    context    = "../backend/"
    dockerfile = "notification/Dockerfile"
  }
}

resource "docker_container" "frontend_container" {
  name  = "frontend"
  image = docker_image.frontend_image.image_id

  ports {
    internal = 80
    external = 80
  }

  ports {
    internal = 443
    external = 443
  }

  volumes {
    host_path      = abspath("${path.module}/../certs")
    container_path = "/etc/nginx/certs"
  }

  volumes {
    host_path      = abspath("${path.module}/nginx.conf")
    container_path = "/etc/nginx/nginx.conf"
    read_only      = true
  }

  networks_advanced {
    name = docker_network.my_network.name
  }

  depends_on = [
    docker_image.frontend_image
  ]
}

resource "docker_container" "auth_container" {
  name  = "auth"
  image = docker_image.auth_image.image_id

  ports {
    internal = 8001
    external = 8001
  }

  volumes {
    host_path      = abspath("${path.module}/../certs")
    container_path = "/certs"
  }

  networks_advanced {
    name = docker_network.my_network.name
  }

  env = [
    "CERT_PATH=/certs/cert.pem",
    "KEY_PATH=/certs/key.pem"
  ]

  depends_on = [
    docker_image.auth_image
  ]
}

resource "docker_container" "storage_container" {
  name  = "storage"
  image = docker_image.storage_image.image_id

  ports {
    internal = 8002
    external = 8002
  }

  volumes {
    host_path      = abspath("${path.module}/../certs")
    container_path = "/certs"
  }

  networks_advanced {
    name = docker_network.my_network.name
  }

  env = [
    "CERT_PATH=/certs/cert.pem",
    "KEY_PATH=/certs/key.pem"
  ]

  depends_on = [
    docker_image.storage_image
  ]
}

resource "docker_container" "payment_container" {
  name  = "payment"
  image = docker_image.payment_image.image_id

  ports {
    internal = 8003
    external = 8003
  }

  volumes {
    host_path      = abspath("${path.module}/../certs")
    container_path = "/certs"
  }

  networks_advanced {
    name = docker_network.my_network.name
  }

  env = [
    "CERT_PATH=/certs/cert.pem",
    "KEY_PATH=/certs/key.pem"
  ]

  depends_on = [
    docker_image.payment_image
  ]
}

resource "docker_container" "notification_container" {
  name  = "notification"
  image = docker_image.notification_image.image_id

  ports {
    internal = 8004
    external = 8004
  }

  volumes {
    host_path      = abspath("${path.module}/../certs")
    container_path = "/certs"
  }

  networks_advanced {
    name = docker_network.my_network.name
  }

  env = [
    "CERT_PATH=/certs/cert.pem",
    "KEY_PATH=/certs/key.pem"
  ]

  depends_on = [
    docker_image.notification_image
  ]
}




