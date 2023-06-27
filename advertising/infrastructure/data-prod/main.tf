module "project_services" {
  source                      = "terraform-google-modules/project-factory/google//modules/project_services"
  version                     = "~> 14.2.0"
  project_id                  = var.project_id
  enable_apis                 = true
  disable_dependent_services  = false
  disable_services_on_destroy = false
  activate_apis = [

  ]
}

module "dbt_sa" {
  source  = "terraform-google-modules/service-accounts/google"
  version = "~> 4.1.0"
  project_id   = var.project_id
  names        = ["dbt-sa"]
  display_name = "dbt Service Account"

  generate_keys = true
  project_roles = [
    "${var.project_id}=>roles/bigquery.dataOwner",
    "${var.project_id}=>roles/bigquery.jobUser",
    "${var.project_id}=>roles/bigquery.connectionAdmin",
  ]
}

module "project_iam" {
  source   = "terraform-google-modules/iam/google//modules/projects_iam"
  version  = "~> 7.4.1"
  projects = [var.project_id]
  mode     = "additive"

  bindings             = {
    "roles/bigquery.resourceViewer" = [
      
    ]
    "roles/bigquery.jobUser" = [

    ]
    "roles/bigquery.dataViewer" = [
      
    ]
  }
}