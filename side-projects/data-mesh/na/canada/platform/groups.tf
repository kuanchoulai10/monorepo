# TODO: delete
resource "googleworkspace_group" "usa" {
  for_each = toset(local.groups)
  email    = "usa-${each.key}@kcl10.com"
  name     = title(replace(each.key, "-", " "))
}

locals {
  groups = [
    "data",
    "sales",
    "marketing",
    "human-resource",
    "finance",
    "legal"
  ]
}
