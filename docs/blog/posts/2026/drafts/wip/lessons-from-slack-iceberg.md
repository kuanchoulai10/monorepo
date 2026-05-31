---
draft: true
authors:
  - kuanchoulai10
date:
  created: 2026-05-31
  updated: 2026-05-31
categories:
  - Data
links:
  - "Maintaining Iceberg at Scale: Lessons from Slack | 2026 Iceberg Summit": https://youtu.be/NRSlundcwvc?si=NOw46genitJRooXX
tags:
  -
comments: true
---


# Lessons from Slack：在 180PB 規模上維運 Iceberg


<!-- more -->


> 本文素材整理見 [`materials/slack-iceberg-at-scale.md`](materials/slack-iceberg-at-scale.md)。

(intro 段落：Slack 數據湖規模、talk 來源、本文要談的脈絡)


## Iceberg 之前，Hive + Parquet 的四個瓶頸

(intro：說明導入 Iceberg 前 Slack 主要靠 Hive Metastore + Parquet 管理數據湖，以下四個面向最痛)

### Partitioning strategy 綁死資料表結構

(內容待寫)

### Hive Metastore 成為效能瓶頸

(內容待寫)

### 災難恢復仰賴手動補回 schema 與分區

(內容待寫)

### Hive 缺乏支援 data mesh 的共享能力

(內容待寫)


## Adopting Iceberg: from batch to streaming, then CDC

(intro：說明 Slack 並不是一次性全面換掉 Hive，而是沿著 batch → streaming → CDC 三個階段把 Iceberg 用起來)

### First move: Kafka Connect

(內容待寫：第一個 use case，用 Kafka Connect 把 batch ingestion 改成 streaming)

### Next move：CDC pipeline

(內容待寫：Vitess + Debezium + Kafka Connect，每小時 MERGE，採用 MOR)

### Payoffs：Performance, Flexibility, Sharing

(內容待寫：multi-PB 查詢加速 70%、partition evolution、snapshot rollback、redaction、REST Catalog 上的 zero-copy sharing)


## Iceberg 的隱藏成本

(intro：no free lunch；引用 Lawrence "Maintenance is the cost of adopting Iceberg"；觀察到採用曲線突然停下來——plateau)

(以下三個被否決的方向，改用 **粗體 inline 小標** 寫成連貫敘述)

**(待寫小標 1)** 第一個方向：由各資料團隊自行維護。否決原因：onboarding 成本、知識傳遞、執行不一致。

**(待寫小標 2)** 第二個方向：提供統一的 curated scripts / self-service 工具。否決原因：團隊只想關心數據內容，不想碰 plumbing。

**(待寫小標 3)** 第三個方向：直接採用 AWS S3 Tables。否決原因：當時無法滿足 fine-tuning 需求（維護頻率、internal sorting 等）。

**(待寫小標 4)** 最後落腳的方向：由 infra team 蓋一個中央集中式的維護服務。


## 根據資料特性決定維護策略

(intro：建構系統之前，Slack 先把湖內資料分成四類，再從每一類的讀寫模式推導出對應的維護需求)

### Static: low change, low maintenance

(內容待寫)

### Append-only: batch-stacked, lightweight maintenance

(內容待寫)

### Streaming: compaction is the core

(內容待寫)

### Volatile: delete files are the hard part

(內容待寫)


## 維護系統的五個設計需求

(intro + 五項需求的連貫敘述，不用 H3)


## IceChipper：Slack 的集中式 Iceberg 維護服務

(intro：以「一張表從被排程到收工的旅程」當主敘事線，串起底下四個元件)

### 從 catalog 自動發現待維護的表

(內容待寫：Discovery Service / Discovery Table 動態 onboarding / offboarding)

### 用既有的 Airflow 與 EMR 撐起執行層

(內容待寫：Airflow 排程、Spark on EMR 執行，重用既有 infra)

### Locking：避免重複維護

(內容待寫：為什麼需要鎖、用 Iceberg Lock table + MERGE + Run ID、不擋外部讀寫、idempotency)

### Tracking：紀錄每次維護動作

(內容待寫：Tracking table 紀錄 start/end、success/failure、metadata；接 dashboards 給 on-call)

### 規模、成功率與效率同時到位

(內容待寫：4,000 張表、99.9% 成功率、15 分鐘 batch、17 PB 單表規模、每日百萬 orphan files)

### 三個待克服的挑戰

(內容待寫：Orphan file deletion 的 Driver OOM 與 AWS rate limiting、批次衝突造成資源飢餓、S3 lifecycle policy 邊際案例)
