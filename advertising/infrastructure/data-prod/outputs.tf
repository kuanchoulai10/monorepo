output "dbt_sa_key" {
  value = module.dbt_sa.key
  sensitive = true
}
