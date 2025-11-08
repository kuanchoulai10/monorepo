# Work Experience

| Period               | Role                     | Company          | Type                                | Link                                                                 |
|----------------------|--------------------------|------------------|-------------------------------------|----------------------------------------------------------------------|
| Sep. 2025 - Present  | Sr. Engineer            | TM       | Full-time, Hybrid                   | [:fontawesome-solid-arrow-pointer:](./tm/tm.md){ .md-button } |
| May 2024 - Sep 2024  | Sr. Data Engineer            | UST Global       | Full-time, Remote                   | [:fontawesome-solid-arrow-pointer:](./ust/ust.md){ .md-button } |
| Jun 2021 - Feb 2024  | Data Engineer            | TVBS Media Inc.  | Full-time, Hybrid (Taipei, Taiwan)  | [:fontawesome-solid-arrow-pointer:](./tvbs/tvbs.md){ .md-button } |
| Jun 2020 - Sep 2020  | ML Researcher            | NinoX            | Contract, Remote                    | [:fontawesome-solid-arrow-pointer:](./ninox/ninox.md){ .md-button } |
| Jul 2018 - Aug 2018  | Industry Analyst Intern  | ITRI             | Intern, On-site (Hsinchu, Taiwan)   | [:fontawesome-solid-arrow-pointer:](./itri/itri.md){ .md-button } |

## XDR Lakehouse Project (Apache Iceberg + Trino)

XDR的核心是將資料從各個端點（email server, server, network devices, cloud services, laptops）整合，後續提供給SOC團隊做威脅偵測與回應。這些資料量非常龐大，且來自不同來源，因此需要一個強大的資料處理平台來進行分析與查詢。

過去使用的資料查詢平台成本高昂，且受制於單一雲端服務供應商。為了降低成本並提升彈性和自主性，TM思考轉向使用開源的Trino作為資料查詢引擎，並且將Table format改成Apache Iceberg，以便更有效地管理和查詢大量資料。

!!! success "Summary"

    XDR Lakehouse Project (Apache Iceberg + Trino)

    - [x] 
    - [x] 
    - [x] 
    - [x] 
    - [x]
    - [x]



- 協助資深工程師完成fluentbit部署在eks，目的是要收集Trino的log，並送到cloudwatch。為什麼要做這件事，因為我們需要監控Trino 每個query的執行狀況，包含成功或失敗，還有執行時間等資訊。
- 做Traffic Mirroring，測試production流量在新技術架構上的可行性，Peak Time需要承受QPS 200的流量，將production環境的APIs requests logs，從Azure application insights轉送到AWS SQS，透過CloudFormation部署整個traffic mirroring的架構，進行流量的sampling, routing, rate limiting等
- 透過CloudWatch，製作monitoring dashboard，監控requests forwarding的成功率，失敗率，latency等指標，確保新技術架構在production流量下的穩定性
- 能在任何時間點，replay過去任一時間區間的production流量，好處是可以讓測試時的benchmark有可比性，可以更容易地持續了解在peak time的技術瓶頸在哪
- EKS 導入Karpenter ，dynamic autoscaling，提升資源利用率，降低成本
- Trino 導入KEDA，根據query queue length自動調整worker數量
- 透過降低Trino concurrent queries數量，避免 trino coordinator 資源競爭，提升整體查詢效能


[Work Experience :material-page-previous-outline:{ .lg .middle }](../index.md){ .md-button }