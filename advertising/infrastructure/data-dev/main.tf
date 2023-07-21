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