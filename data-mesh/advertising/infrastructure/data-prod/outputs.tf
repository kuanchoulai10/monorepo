output "dbt_sa_key" {
  value = module.dbt_sa.key
  sensitive = true
}

output "dbt_sa_iam_email" {
  value = module.dbt_sa.iam_email
}
