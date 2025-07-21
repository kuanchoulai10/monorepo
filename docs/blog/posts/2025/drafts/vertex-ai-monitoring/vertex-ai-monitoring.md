---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2025-08-01
  updated: 2025-08-01
categories:
  - GCP
tags:
  - vertex-ai
comments: true
---


# Vertex AI Model Monitoring

!!! info "TLDR"
    看完這篇文章，你可以
    
    - ABC
    - STU
    - XYZ

<!-- more -->
- Vertex AI Model Monitoring lets you run monitoring jobs as needed or on a regular schedule to track the quality of your tabular models.
- If you've set alerts, Vertex AI Model Monitoring informs you when metrics surpass a specified threshold.
- Vertex AI Model Monitoring can track and alert you when deviations exceed a specified threshold. You can then re-evaluate or retrain your model to ensure the model is behaving as intended.
- Vertex AI Model Monitoring can provide visualizations like in the following figure, which overlays two graphs from two datasets. This visualization lets you quickly compare and see deviations between the two sets of data.

## Versions

### Version 2

- Preview
- You can run on-demand monitoring jobs or set up scheduled runs.
- For each model version, you can specify one or more monitoring objectives.
- objective
    - Input feature data drift: Measures the distribution of input feature values compared to a baseline data distribution. Supported metrics: L-Infinity, Jensen Shannon Divergence.
    - Output prediction data drift: Measures the model's predictions data distribution compared to a baseline data distribution. Supported metrics: L-Infinity, Jensen Shannon Divergence.
    - Feature attribution: Measures the change in contribution of features to a model's prediction compared to a baseline. Supported metrics: SHAP value (SHapley Additive exPlanations)
- Input feature and output prediction drift: Model Monitoring v2 can monitor changes in the distribution of production data compared to the training data or to track the evolution of production data distribution over time.
- Similarly, for prediction data, Model Monitoring v2 can monitor changes in the distribution of predicted outcomes compared to the training data or production data distribution over time.
- By monitoring feature attributions, Model Monitoring v2 tracks changes in a feature's contributions to a model's predictions over time. A change in a key feature's attribution score often signals that the feature has changed in a way that can impact the accuracy of the model's predictions.

### Version 1

- Generally Available
- Production-level support
- For existing Model Monitoring v1 users, Model Monitoring v1 is maintained as is. You aren't required to migrate to Model Monitoring v2.
- Model Monitoring v1 monitors the model's prediction input data for feature skew and drift:
- **Training-serving skew** occurs when the **feature data distribution** in production deviates from the feature data distribution used to train the model. If the original training data is available, you can enable skew detection to monitor your models for training-serving skew.
- **Prediction drift** occurs when **feature data distribution** in production changes significantly over time. If the original training data isn't available, you can enable drift detection to monitor the input data for changes over time.
- Once the skew or drift for a model's feature exceeds an alerting threshold that you set, Model Monitoring v1 sends you an email alert.

## Considerations when using Model Monitoring

- For **cost efficiency**, you can set a **prediction request sampling rate** to monitor a subset of the production inputs to a model.
- You can set a **frequency** at which a deployed model's recently logged inputs are monitored for skew or drift.
- Monitoring frequency determines the timespan, or monitoring window size, of logged data that is analyzed in each monitoring run.



## References

- [Introduction to Vertex AI Model Monitoring](https://cloud.google.com/vertex-ai/docs/model-monitoring/overview)