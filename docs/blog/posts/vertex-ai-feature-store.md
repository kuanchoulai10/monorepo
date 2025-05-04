---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2025-04-11
  updated: 2025-04-11
categories:
  - GCP
tags:
  - vertex-ai
comments: true
---


# Vertex AI Feature Store

!!! info "TLDR"
    看完這篇文章，你可以
    
    - ABC
    - STU
    - XYZ

<!-- more -->

- It streamlines your ML feature management and online serving processes by letting you manage your feature data in a BigQuery table or view. You can then serve features online directly from the BigQuery data source.
- Vertex AI Feature Store provisions resources that let you set up online serving by specifying your feature data sources. It then acts as a metadata layer interfacing with the BigQuery data sources and serves the latest feature values directly from BigQuery for online predictions at low latencies.

## Wokrflow

1. Prepare your data source in BigQuery.
2. Optional: Register your data sources by creating feature groups and features.
3. Set up online store and feature view resources to connect the feature data sources with online serving clusters.
4. Serve the latest feature values online from a feature view.


## Offline store
- In Vertex AI Feature Store, the BigQuery tables or views containing the feature data collectively form the offline store.
- Because all the feature data is maintained in BigQuery, Vertex AI Feature Store doesn't need to provision a separate offline store within Vertex AI.
Moreover, if you want to use the data in the offline store to train ML models, you can use the **APIs** and capabilities in BigQuery to export or fetch the data.

## Data preparation in BigQuery

- Before you set up Feature Registry or online serving resources, you must store your feature data in **one or more** BigQuery tables or views.
- Within a BigQuery table or view, each column represents a feature
- Because you prepare the data source in BigQuery and not in Vertex AI, you don't need to create any Vertex AI resources at this stage

## Feature Registry setup

- After you've prepared your data sources in BigQuery, you can register those data sources, including specific feature columns, in the Feature Registry.
- Registering your features is optional
- Advantages
    - Your data contains multiple instances of the same entity ID and you need to prepare your data in a time-series format with a timestamp column
    - You want to aggregate specific columns from multiple data sources to define a feature view instance.
    - You want to monitor the feature statistics and detect feature drift.
- two types of Vertex AI Feature Store resources in the Feature Registry:
    - Feature Registry resources for feature data
        - Feature group: A `FeatureGroup` resource is associated with a specific BigQuery source table or view.
        - Feature: A `Feature` resource represents a specific column containing feature values
    - Feature Registry resources for feature monitoring
        - Feature monitor
        - Feature monitor job

## Online Serving setup

- To serve features for online predictions, you must define and configure at least one online serving cluster, and associate it with your feature data source or Feature Registry resources.
In Vertex AI Feature Store, the online serving cluster is called an **online store instance**.
- An online store instance can contain multiple feature view instances, where each feature view is associated with a feature data source.
- Online store: A `FeatureOnlineStore` resource represents an online serving cluster instance and contains the online serving configuration, such as the number of online serving nodes.
    - An online store instance doesn't specify the source of the feature data, but contains FeatureView resources that specify the feature data sources in either BigQuery or the Feature Registry.
- Feature view (FeatureView): A FeatureView resource is a logical collection of features in an online store instance.


## Online serving

Vertex AI Feature Store provides the following types of online serving for real-time online predictions:

- Bigtable online serving
    - provides improved caching to mitigate hotspotting
    - Bigtable online serving doesn't support embeddings. 
    - If you need to serve large volumes of data that are frequently updated and don't need to serve embeddings, use Bigtable online serving.
- Optimized online serving: 
    - Optimized online serving can provide lower latencies than Bigtable online serving and is recommended for most scenarios
    - support embeddings management



# Feast

![Feast Architecture Diagram](https://docs.feast.dev/~gitbook/image?url=https%3A%2F%2F1434314375-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FVuINcVtEUuzdbwh3URX1%252Fuploads%252Fgit-blob-9f7df7c01969608f5a8b1d48b21f20ddeaed5590%252Ffeast_marchitecture.png%3Falt%3Dmedia&width=768&dpr=4&quality=100&sign=65ac251b&sv=2)

- Feast uses a Push Model to ingest data 
- Feast supports feature transformation for On Demand and Streaming data sources

## Hierarchy

![](https://docs.feast.dev/~gitbook/image?url=https%3A%2F%2F1434314375-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FVuINcVtEUuzdbwh3URX1%252Fuploads%252Fgit-blob-af58d3cf3809fcc5e69119de273668f715f27538%252Fimage%2520%287%29.png%3Falt%3Dmedia&width=400&dpr=3&quality=100&sign=b9097205&sv=2)

- The top-level namespace within Feast is a **project**.
- Users define one or more **feature views** within a project.
- Each feature view contains one or more **features**.
- These features typically relate to one or more **entities**.
- A feature view must always have a **data source**, which in turn is used during the generation of training datasets and when materializing feature values into the online store.

## Data Ingestion

- A data source in Feast refers to raw underlying data that users own (e.g. in a table in BigQuery). Feast does not manage any of the raw underlying data but instead, is in charge of loading this data and performing different operations on the data to retrieve or serve features.
- Feast uses a time-series data model to represent data.
- Feast supports primarily time-stamped tabular data as data sources
- Many kinds of possible data sources
    - Batch data sources: BigQuery, Snowflake, Redshift, S3, GCS
    - Stream data sources: doesn't have native streaming integrations
        - Push sources: allow users to push features into Feast
        - Stream sources (Alpha): register metadata from Kafka or Kinesis sources
- (Experimental) Request data sources: only available at request time (on-demand feature views), aloow light-weight feature engineering and combining features across sources

### Batch data ingestion

- Ingesting from batch sources is only necessary to power real-time models. This is done through materialization. 
- A key command to use in Feast is the `materialize_incremental` command, which fetches the latest values for all entities in the batch source and ingests these values into the online store.

### Stream data ingestion

- Ingesting from stream sources happens either via 
    1. a Push API or via
    2. a contrib processor that leverages an existing Spark context


### offline use cases

- For offline use cases that only rely on batch data, Feast **does not need to ingest data and can query your existing data** (leveraging a compute engine, whether it be a data warehouse or (experimental) Spark / Trino).

### online use cases

- For online use cases, Feast supports **ingesting** features from batch sources to make them available online (through a process called **materialization**),
- and pushing streaming features to make them available both offline / online.

## Feature registration and retrieval

- Features are registered as code in a version controlled repository, and tie to data sources + model versions via the concepts of entities, feature views, and feature services.
- These features are then stored in a registry, which can be accessed across users and services.
- The features can then be retrieved via SDK API methods or via a deployed feature server which exposes endpoints to query for online features

## Entity

1. An entity is a collection of semantically related features.
2. Users define entities to map to the domain of their use case.

Use cases

1. Defining and storing features
    - Feast's primary object for defining features is a feature view, which is a collection of features.
    - Feature views map to 0 or more entities, since a feature can be associated with
        - zero entities
        - one entities
        - mulitple entities
    - Feast refers to this collection of entities for a feature view as an entity key
    - Entities should be reused across feature views. This helps with discovery of features
2. Retrieving features
    - At training time, users control what entities they want to look up. A user specifies a list of entity keys + timestamps they want to fetch point-in-time correct features
    - At serving time, users specify entity key(s) to fetch the latest feature values which can power real-time model prediction

## Feature view

- A feature view is an object representing a logical group of time-series feature data as it is found in a data source.
- A feature view is defined as a collection of features.
    - In the **online** settings, this is a **stateful** collection of features that are read when the `get_online_features` method is called.
    - In the **offline** setting, this is a **stateless** collection of features that are created when the `get_historical_features` method is called.

A feature view contains

- a data source
- zero or more entities
- uniquely identifiable name in the project
- a schema
- metadata
- TTL (Time to Live), which limits how far back Feast will look when generating historical datasets

Feature views are used during

- The generation of training datasets
- Loading of feature values into an online store.
- Retrieval of features from the online store

## Entity aliasing

- This could be used if a user has no control over these column names or if there are multiple entities are a subclass of a more general entity.

## Feature services

- A **feature service** is an object that represents a logical group of features from one or more feature views.
- Feature Services allows features from within a feature view to be used as needed by an ML model.
- Users can expect to **create one feature service per model version**, allowing for tracking of the features used by models.
- Feature services are used during
    - The generation of training datasets
    - Retrieval of features **from the offline store for batch scoring**
    - Retrieval of features **from the online store for online inference**
- Feature services enable referencing all or some features from a feature view.

## Feature References

- This mechanism of retrieving features is only recommended as you're experimenting
- It is possible to retrieve features from multiple feature views with a single request, and Feast is able to join features from multiple tables in order to build a training dataset.

```
online_features = fs.get_online_features(
    features=[
        'driver_locations:lon',
        'drivers_activity:trips_today'
    ],
    entity_rows=[
        # {join_key: entity_value}
        {'driver': 'driver_1001'}
    ]
)
```

## Running Feast in Production

1. Automatically deploying changes to your feature definitions
    1. Setting up a feature repository
    2. Setting up a database-backed registry
    3. Setting up CI/CD to automatically update the registry
    4. Setting up mulitple environments
2. How to load data into your online store and keep it up to date
    1. Scalable Materialization
    2. Scheduled materialization with Airflow
    3. Stream feature ingestion (both online and offline)
    4. Scheduled batch transformations with Airflow + dbt
3. How to use Feast for model training
    1. Generating training data
    2. Versioning features that power ML models
4. Retrieving online features for prediction
    1. Use the Python SDK within an existing Python service
    2. Deploy Feast festure servers on Kubernetes (Deprecated, replaced by [feast-operator](https://github.com/feast-dev/feast/blob/v0.48-branch/infra/feast-operator/README.md))
5. Using environment variables in your yaml configuration

### Summary

![](https://docs.feast.dev/~gitbook/image?url=https%3A%2F%2F1434314375-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FVuINcVtEUuzdbwh3URX1%252Fuploads%252Fgit-blob-ce3f7017cdfa4c12f6abe8e8d089626ad71efb66%252Fproduction-spark-bytewax.png%3Falt%3Dmedia&width=768&dpr=4&quality=100&sign=b644b016&sv=2)

1. CI/CD: Feast SDK is being triggered by CI (eg, Github Actions)
2. Batch data ingestion: Airflow manages batch transformation jobs + materialization jobs. It's recommended to use a batch materialization engine to materialize large datasets.
3. Stream data ingestion: The Feast Push API is used within existing Spark / Beam pipelines to push feature values to offline / online stores
4. Online features are served via (1) the Python feature server over HTTP, or (2) consumed using Feast Python SDK
5. Feast Python SDK is called locally to generate a training dataset