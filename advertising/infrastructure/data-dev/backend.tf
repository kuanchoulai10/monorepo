terraform {
  cloud {
    organization = "kcl"
    workspaces {
      name = "advertising-data-dev"
    }
  }
}