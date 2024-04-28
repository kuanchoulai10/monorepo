terraform {
  required_providers {
    google = {
      version = "~> 4.70.0"
    }
    tfe = {
      source  = "hashicorp/tfe"
      version = "~> 0.45.0"
    }
  }
}
