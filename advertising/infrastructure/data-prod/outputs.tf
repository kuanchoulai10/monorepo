output "dbt_sa_key" {
  value = module.dbt_sa.key
  sensitive = true
}

output "dbt_sa" {
  value = module.dbt_sa
}
