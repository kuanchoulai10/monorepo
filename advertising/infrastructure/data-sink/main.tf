module "project_services" {
  source                      = "terraform-google-modules/project-factory/google//modules/project_services"
  version                     = "~> 14.2.0"
  project_id                  = var.project_id
  enable_apis                 = true
  disable_dependent_services  = false
  disable_services_on_destroy = false
  activate_apis = [
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com"
  ]
}

module "project_iam" {
  source   = "terraform-google-modules/iam/google//modules/projects_iam"
  version  = "~> 7.4.1"
  projects = [var.project_id]
  mode     = "additive"

  bindings = {
    "roles/bigquery.jobUser" = [
      "serviceAccount:${data.tfe_outputs.advertising_data_dev.nonsensitive_values.edisonlai_sa_email}",
      "${data.tfe_outputs.advertising_data_prod.nonsensitive_values.dbt_sa_iam_email}"
    ]
    "roles/bigquery.dataViewer" = [
      "serviceAccount:${data.tfe_outputs.advertising_data_dev.nonsensitive_values.edisonlai_sa_email}",
      "${data.tfe_outputs.advertising_data_prod.nonsensitive_values.dbt_sa_iam_email}"
    ]
  }
  depends_on = [
    module.project_services
  ]
}