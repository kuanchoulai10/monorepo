# resource "google_cloudfunctions2_function" "remove_html_tags" {
#   name = "bqrm-remove-html-tags"
#   location = "us-central1"
#   description = "a new function"

#   build_config {
#     runtime = "nodejs16"
#     entry_point = "helloPubSub"  # Set the entry point 
#     environment_variables = {
#         BUILD_CONFIG_TEST = "build_test"
#     }
#     source {
#       storage_source {
#         bucket = google_storage_bucket.bucket.name
#         object = google_storage_bucket_object.object.name
#       }
#     }
#   }

#   service_config {
#     max_instance_count  = 3
#     min_instance_count = 0
#     available_memory    = "4Gi"
#     timeout_seconds     = 60
#     max_instance_request_concurrency = 80
#     available_cpu = "4"
#     environment_variables = {
#         SERVICE_CONFIG_TEST      = "config_test"
#         SERVICE_CONFIG_DIFF_TEST = google_service_account.account.email
#     }
#     ingress_settings = "ALLOW_INTERNAL_ONLY"
#     all_traffic_on_latest_revision = true
#     service_account_email = google_service_account.account.email
#   }

#   event_trigger {
#     trigger_region = "us-central1"
#     event_type = "google.cloud.pubsub.topic.v1.messagePublished"
#     pubsub_topic = google_pubsub_topic.topic.id
#     retry_policy = "RETRY_POLICY_RETRY"
#   }
# }

resource "google_bigquery_connection" "default" {
  connection_id = "bqrf"
  location      = "asia-east1"
  cloud_resource {}
}

module "project_iam_bindings" {
  source  = "terraform-google-modules/iam/google//modules/projects_iam"
  version = "~> 8.0"

  projects = [data.google_project.default.project_id]
  mode     = "additive"

  bindings = {
    "roles/run.invoker" = [
      "serviceAccount:${google_bigquery_connection.default.cloud_resource[0].service_account_id}"
    ]
    "roles/storage.objectViewer" = [
      "serviceAccount:${google_bigquery_connection.bq_object_tables.cloud_resource[0].service_account_id}"
    ]
    "roles/serviceusage.serviceUsageConsumer" = [
      "serviceAccount:${google_bigquery_connection.bq_object_tables.cloud_resource[0].service_account_id}"
    ]
    "roles/documentai.viewer" = [
      "serviceAccount:${google_bigquery_connection.document_ai.cloud_resource[0].service_account_id}",
      "serviceAccount:${google_bigquery_connection.bq_object_tables.cloud_resource[0].service_account_id}"
    ]
    "roles/aiplatform.user" = [
      "serviceAccount:${google_bigquery_connection.vertex_ai.cloud_resource[0].service_account_id}"
    ]
  }
}

resource "google_bigquery_connection" "bq_object_tables" {
  connection_id = "bg-object-tables"
  location      = "US"
  cloud_resource {}
}

resource "google_bigquery_connection" "bq_cloud_vision" {
  connection_id = "bg-cloud-vision"
  location      = "US"
  cloud_resource {}
}

resource "google_bigquery_connection" "document_ai" {
  connection_id = "document_ai"
  location      = "US"
  cloud_resource {}
}

resource "google_bigquery_connection" "vertex_ai" {
  connection_id = "vertex_ai"
  location      = "US"
  cloud_resource {}
}

resource "google_document_ai_processor" "layout_parser_processor" {
  location     = "us"
  display_name = "layout-parser-processor"
  type         = "LAYOUT_PARSER_PROCESSOR"
}
