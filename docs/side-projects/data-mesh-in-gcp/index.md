# Build a Data Mesh with Dataplex

## What is Dataplex?

- data fabric tool
- enables organizations to centrally manage, govern, discover, monitor their data while keeping data teams decentralized
- to build data mesh architecture
- manages data in a way that doesn't require data movement or duplication.
- harvest the metadata for both structured and unstructured data, and automatically registers all metadata in a secure, unified metastore.

### Lake

- highest organizational domain that represents a specific data area or business unit
- create a lake for each department or data domain
- regional or multi regional

### Zone

- within lake
- categorize data further for example by stage, usage or restrictions
- 2 types of zones
  - raw zones
  - curated zones

### IAM

- Dataplex allows Dataplex administrators to grant Dataplex IAM roles to users at the level of the project, lake, zone, and individual assets


### Asset

- GCS buckets or BigQuery datasets can be attached as assets to zones

### Data Quality Check

- run data quality checks on Dataplex assets such as BigQuery tables and Cloud Storage files.


## What is Data Catalog?

- Data Catalog is a fully managed, scalable metadata management service within Dataplex that you can use to tag data assets and search for assets to which you have access.
- Tags allow you to attach custom metadata fields to specific data assets for easy identification and retrieval
- you can also create reusable tag templates to rapidly assign the same tags to different data assets.


### Tag Template

- A tag template can be a public or private tag template. When you create a new tag template, the option to create a public tag template is the default and recommended option. 
- Users who have the required view permissions for a data asset can view all the public tags associated with it
- regional resource


