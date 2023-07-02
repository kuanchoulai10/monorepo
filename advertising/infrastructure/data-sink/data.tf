data "tfe_outputs" "advertising_data_dev" {
  organization = "kcl"
  workspace    = "advertising-data-dev"
}

data "tfe_outputs" "advertising_data_prod" {
  organization = "kcl"
  workspace    = "advertising-data-prod"
}
