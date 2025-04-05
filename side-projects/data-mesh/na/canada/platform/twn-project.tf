
module "project-factory" {
  source  = "terraform-google-modules/project-factory/google"
  version = "~> 17.1"

  name              = "kcl-tw-data"
  random_project_id = true
  folder_id         = google_folder.data.folder_id
  billing_account   = data.google_billing_account.kcl.id
  sa_role           = "roles/editor"
  activate_apis = [
    "bigquery.googleapis.com",
    "bigqueryconnection.googleapis.com",
    "run.googleapis.com",
    "cloudfunctions.googleapis.com",
    "compute.googleapis.com",
    "cloudbuild.googleapis.com",
    "vision.googleapis.com",
    "documentai.googleapis.com",
    "aiplatform.googleapis.com",
    "datacatalog.googleapis.com",
    "dataplex.googleapis.com",
    "cloudresourcemanager.googleapis.com", # optional
    "serviceusage.googleapis.com",         # optional
    "admin.googleapis.com"                 # for google workspace
  ]
}
