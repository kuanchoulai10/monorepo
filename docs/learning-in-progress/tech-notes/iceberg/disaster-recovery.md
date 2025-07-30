# Disaster Recovery with Apache Iceberg


- The Catalog Is Missing or Points to the Wrong `metadata.json` --> `register_table` to re-establish the link to your latest `metadata.json`.
- File Paths Have Changed During Restore --> use `rewrite_table_path` to rewrite metadata and create a clean recovery copy


## Best Practices for Iceberg Disaster Recovery

Implement proactive backup practices

- Always Backup Metadata and Data Together
- Track the Latest `metadata.json` in Every Backup
- Check for File Path Changes Before Recovery
- Automate Validation Post-Restore
- Dry-Run Your Recovery Plan


## References

- [Disaster Recovery for Apache Iceberg Tables – Restoring from Backup and Getting Back Online](https://www.dremio.com/blog/disaster-recovery-for-apache-iceberg-tables-restoring-from-backup-and-getting-back-online/)