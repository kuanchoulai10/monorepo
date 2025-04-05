data "google_organization" "org" {
  domain = "kcl10.com"
}

data "google_billing_account" "kcl" {
  display_name = "KCL"
}
