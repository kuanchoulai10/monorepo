# APAC
resource "google_folder" "apac" {
  display_name = "apac"
  parent       = data.google_organization.org.name
}

resource "google_folder" "twn" {
  display_name = "twn"
  parent       = google_folder.apac.name
}

resource "google_folder" "twn_depts" {
  for_each     = toset(["data", "sales", "marketing"])
  display_name = each.key
  parent       = google_folder.twn.name
}

# TODO: delete
resource "google_folder" "taiwan" {
  display_name = "taiwan"
  parent       = data.google_organization.org.name
}

# TODO: delete
resource "google_folder" "data" {
  display_name = "data"
  parent       = google_folder.taiwan.name
}

resource "google_folder" "jpn" {
  display_name = "jpn"
  parent       = google_folder.apac.name
}

resource "google_folder" "jpn_depts" {
  for_each     = toset(["data", "sales", "marketing"])
  display_name = each.key
  parent       = google_folder.jpn.name
}


# EMEA
resource "google_folder" "emea" {
  display_name = "emea"
  parent       = data.google_organization.org.name
}

resource "google_folder" "gbr" {
  display_name = "gbr"
  parent       = google_folder.emea.name
}

resource "google_folder" "gbr_depts" {
  for_each     = toset(["data", "sales", "marketing"])
  display_name = each.key
  parent       = google_folder.gbr.name
}

resource "google_folder" "fra" {
  display_name = "fra"
  parent       = google_folder.emea.name
}

resource "google_folder" "fra_depts" {
  for_each     = toset(["data", "sales", "marketing"])
  display_name = each.key
  parent       = google_folder.fra.name
}


# NA
resource "google_folder" "na" {
  display_name = "na"
  parent       = data.google_organization.org.name
}

resource "google_folder" "can" {
  display_name = "can"
  parent       = google_folder.na.name
}

resource "google_folder" "can_depts" {
  for_each     = toset(["platform", "data", "sales", "marketing"])
  display_name = each.key
  parent       = google_folder.can.name
}

resource "google_folder" "usa" {
  display_name = "usa"
  parent       = google_folder.na.name
}

resource "google_folder" "usa_depts" {
  for_each     = toset(["data", "sales", "marketing"])
  display_name = each.key
  parent       = google_folder.usa.name
}
