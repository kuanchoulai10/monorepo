# SQL-based RAG Application

![](rag.drawio.svg)

## Create a Bucket in GCS and upload a pdf file


### Create a Object Table in BigQuery

``` sql
create or replace external table `us_test2.pdf`
with connection `us.bg-object-tables`
options(
  object_metadata = 'SIMPLE',
  uris = ['gs://kcl-us-test/scf23.pdf']
);
```

## Create a Layout Parser type of Processor in Document AI and a Remote Model corresponding to the processor

``` sql
create or replace model `us_test2.doc_parser`
remote with connection `us.document_ai`
options(
  remote_service_type='CLOUD_AI_DOCUMENT_V1',
  document_processor='ec023753643cb1be'
);
```

## Create a embeddings Remote Model in BigQuery

``` sql
create or replace model `us_test2.embedding_model`
remote with connection `us.vertex_ai`
options (
  endpoint='text-embedding-004'
)
```

## Create a generative text Remote Model in BigQuery

``` sql
create or replace model `us_test2.text_model`
remote with connection `us.vertex_ai`
options(
  endpoint = 'gemini-1.5-flash-002'
)
```