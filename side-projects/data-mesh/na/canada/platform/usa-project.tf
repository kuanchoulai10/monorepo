
module "usa_data_project" {
  source  = "terraform-google-modules/project-factory/google"
  version = "~> 17.1"

  name                    = "kcl-usa-data"
  random_project_id       = true
  folder_id               = google_folder.usa_depts["data"].folder_id
  billing_account         = data.google_billing_account.kcl.id
  default_service_account = "keep"
  create_project_sa       = false
  activate_apis = [
    "compute.googleapis.com",
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "cloudfunctions.googleapis.com",
    "bigquery.googleapis.com",
    "bigqueryconnection.googleapis.com",
    "vision.googleapis.com",
    "documentai.googleapis.com",
    "translate.googleapis.com",
    "speech.googleapis.com",
    "language.googleapis.com",
    "aiplatform.googleapis.com"
    # "datacatalog.googleapis.com",
    # "dataplex.googleapis.com",
    # "cloudresourcemanager.googleapis.com", # optional
    # "serviceusage.googleapis.com",         # optional
    # "admin.googleapis.com"                 # for google workspace
  ]
}

locals {
  ai_services = [
    "vision",
    "natural-language",
    "translation",
    "document-ai",
    "speech-to-text"
  ]
  bq_services = [
    "object-table",
    "remote-function"
  ]
}

resource "google_bigquery_connection" "ai_services" {
  for_each      = toset(local.ai_services)
  connection_id = each.key
  project       = module.usa_data_project.project_id
  location      = "us"
  cloud_resource {}
}

resource "google_bigquery_connection" "bq_services" {
  for_each      = toset(local.bq_services)
  connection_id = each.key
  project       = module.usa_data_project.project_id
  location      = "us"
  cloud_resource {}
}

resource "google_bigquery_dataset" "example_us" {
  project       = module.usa_data_project.project_id
  dataset_id    = "example_us"
  friendly_name = "Multi-region US"
  location      = "us"
}

resource "google_bigquery_dataset" "example_oregon" {
  project       = module.usa_data_project.project_id
  dataset_id    = "example_oregon"
  friendly_name = "Oregon"
  location      = "us-west1"
}

resource "google_bigquery_dataset" "example_oregon_aws" {
  project       = module.usa_data_project.project_id
  dataset_id    = "example_oregon_aws"
  friendly_name = "AWS Oregon"
  location      = "aws-us-west-2"
}

resource "google_storage_bucket" "product_images" {
  project  = module.usa_data_project.project_id
  name     = "product-images-${module.usa_data_project.project_id}"
  location = "us"
}

resource "google_storage_bucket" "ml_models" {
  project  = module.usa_data_project.project_id
  name     = "ml-models-${module.usa_data_project.project_id}"
  location = "us"
}

resource "google_storage_bucket" "documents" {
  project  = module.usa_data_project.project_id
  name     = "documents-${module.usa_data_project.project_id}"
  location = "us"
}
