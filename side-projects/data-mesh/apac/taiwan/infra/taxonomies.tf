resource "google_data_catalog_taxonomy" "sensitivity" {
  display_name =  "Sensitivity"
  activated_policy_types = ["FINE_GRAINED_ACCESS_CONTROL"]
}

# High Sensitivity
resource "google_data_catalog_policy_tag" "high" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "High-sensitivity"
}

resource "google_data_catalog_policy_tag" "ssn" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Social Security Number"
  parent_policy_tag = google_data_catalog_policy_tag.high.id
}

resource "google_data_catalog_policy_tag" "passport" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Passport Number"
  parent_policy_tag = google_data_catalog_policy_tag.high.id
}

resource "google_data_catalog_policy_tag" "biometric" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Biometric Data"
  parent_policy_tag = google_data_catalog_policy_tag.high.id
}

resource "google_data_catalog_policy_tag" "medical_records" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Medical Records"
  parent_policy_tag = google_data_catalog_policy_tag.high.id
}

# Medium Sensitivity
resource "google_data_catalog_policy_tag" "medium" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Medium-sensitivity"
}

resource "google_data_catalog_policy_tag" "full_name" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Full Name"
  parent_policy_tag = google_data_catalog_policy_tag.medium.id
}

resource "google_data_catalog_policy_tag" "email" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Email Address"
  parent_policy_tag = google_data_catalog_policy_tag.medium.id
}

resource "google_data_catalog_policy_tag" "phone_number" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Phone Number"
  parent_policy_tag = google_data_catalog_policy_tag.medium.id
}

resource "google_data_catalog_policy_tag" "address" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Address"
  parent_policy_tag = google_data_catalog_policy_tag.medium.id
}

# Low Sensitivity
resource "google_data_catalog_policy_tag" "low" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Low-sensitivity"
}

resource "google_data_catalog_policy_tag" "first_name" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "First Name"
  parent_policy_tag = google_data_catalog_policy_tag.low.id
}

resource "google_data_catalog_policy_tag" "public_profiles" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "Public Social Media Profiles"
  parent_policy_tag = google_data_catalog_policy_tag.low.id
}

resource "google_data_catalog_policy_tag" "demographic_data" {
  taxonomy = google_data_catalog_taxonomy.sensitivity.id
  display_name = "General Demographic Data"
  parent_policy_tag = google_data_catalog_policy_tag.low.id
}
