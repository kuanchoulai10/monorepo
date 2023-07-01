module "project_services" {
  source                      = "terraform-google-modules/project-factory/google//modules/project_services"
  version                     = "~> 14.2.0"
  project_id                  = var.project_id
  enable_apis                 = true
  disable_dependent_services  = false
  disable_services_on_destroy = false
  activate_apis = [
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "datacatalog.googleapis.com"
  ]
}

module "dbt_sa" {
  source       = "terraform-google-modules/service-accounts/google"
  version      = "~> 4.1.0"
  project_id   = var.project_id
  names        = ["dbt-sa"]
  display_name = "dbt Service Account"

  generate_keys = true
  project_roles = [
    "${var.project_id}=>roles/bigquery.dataOwner",
    "${var.project_id}=>roles/bigquery.jobUser",
    "${var.project_id}=>roles/bigquery.connectionAdmin",
  ]
  depends_on = [
    module.project_services
  ]
}

module "project_iam" {
  source   = "terraform-google-modules/iam/google//modules/projects_iam"
  version  = "~> 7.4.1"
  projects = [var.project_id]
  mode     = "additive"

  bindings = {
    "roles/bigquery.resourceViewer" = [
      "serviceAccount:${data.tfe_outputs.advertising_data_dev.nonsensitive_values.edisonlai_sa_email}"
    ]
    "roles/bigquery.jobUser" = [
      "serviceAccount:${data.tfe_outputs.advertising_data_dev.nonsensitive_values.edisonlai_sa_email}"
    ]
    "roles/bigquery.dataViewer" = [
      "serviceAccount:${data.tfe_outputs.advertising_data_dev.nonsensitive_values.edisonlai_sa_email}"
    ]
  }
  depends_on = [
    module.project_services
  ]
}

module "cube" {
  source  = "terraform-google-modules/cloud-storage/google"
  version = "~> 4.0.0"
  project_id  = var.project_id
  names = ["cubestore-20230701"]
  prefix = "kcl"
  set_storage_admin_roles = true
  storage_admins = [
    module.dbt_sa.iam_email
  ]
  versioning = {
    cubestore-20230701 = true
  }
}

resource "google_data_catalog_tag_template" "product" {
  tag_template_id = "data_product"

  display_name = "Data Product"

  fields {
    field_id = "data_domain"
    display_name = "Data domain"
    description = "The broad category for the data"
    order = 11
    is_required = true
    type {
      enum_type {
        allowed_values {
          display_name = "Sales"
        }
        allowed_values {
          display_name = "Marketing"
        }
        allowed_values {
          display_name = "Advertising"
        }
        allowed_values {
          display_name = "Video"
        }
        allowed_values {
          display_name = "Social Media"
        }
        allowed_values {
          display_name = "Other"
        }
      }
    }
  }

  fields {
    field_id = "data_subdomain"
    display_name = "Data subdomain"
    description = "The subcategory for the data"
    is_required = false
    order = 10
    type {
      enum_type {
        allowed_values {
          display_name = "Events"
        }
        allowed_values {
          display_name = "User Behaviors"
        }
      }
    }
  }

  fields {
    field_id = "data_product_name"
    display_name = "Data product name"
    description = "The name of the data product"
    is_required = true
    order = 9
    type {
      primitive_type = "STRING"
    }
  }

  fields {
    field_id = "data_product_description"
    display_name = "Data product description"
    description = "Short description of the data product"
    is_required = false
    order = 8
    type {
      primitive_type = "STRING"
    }
  }

  fields {
    field_id = "business_owner"
    display_name = "Business owner"
    description = "Name of the business person who owns the data product"
    is_required = true
    order = 7
    type {
      primitive_type = "STRING"
    }
  }

  fields {
    field_id = "technical_owner"
    display_name = "Technical owner"
    description = "Name of the technical person who owns the data product"
    is_required = true
    order = 6
    type {
      primitive_type = "STRING"
    }
  }

  fields {
    field_id = "number_data_resources"
    display_name = "Number of data resources"
    description = "Number of data resources in the data product"
    is_required = false
    order = 5
    type {
      primitive_type = "DOUBLE"
    }
  }

  fields {
    field_id = "storage_location"
    display_name = "Storage location"
    description = "The storage location for the data product"
    is_required = false
    order = 4

    type {
      enum_type {
        allowed_values {
          display_name = "us-east1"
        }
        allowed_values {
          display_name = "us-central1"
        }
        allowed_values {
          display_name = "us"
        }
        allowed_values {
          display_name = "eu"
        }
        allowed_values {
          display_name = "other"
        }
      }
    }
  }

  fields {
    field_id = "documentation_link"
    display_name = "Documentation Link"
    description = "Link to helpful documentation about the data product"
    is_required = false
    order = 3
    type {
      primitive_type = "STRING"
    }
  }

  fields {
    field_id = "access_request_link"
    display_name = "Access request link"
    description = "How to request access the data product"
    is_required = false
    order = 2
    type {
      primitive_type = "STRING"
    }
  }

  fields {
    field_id = "data_product_status"
    display_name = "Data product status"
    description = "Status of the data product"
    is_required = true
    order = 1
    type {
      enum_type {
        allowed_values {
          display_name = "DRAFT"
        }
        allowed_values {
          display_name = "PENDING"
        }
        allowed_values {
          display_name = "REVIEW"
        }
        allowed_values {
          display_name = "DEPLOY"
        }
        allowed_values {
          display_name = "RELEASED"
        }
        allowed_values {
          display_name = "DEPRECATED"
        }
      }
    }
  }

  fields {
    field_id = "last_modified_date"
    display_name = "Last modified date"
    description = "The last time this annotation was modified"
    is_required = true
    order = 0
    type {
      primitive_type = "TIMESTAMP"
    }
  }

  force_delete = "true"
  depends_on = [
    module.project_services
  ]
}
