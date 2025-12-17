---
tags:
  - Knative
  - How It Works
---

# What Is Knative?

- Knative is an Open-Source Enterprise-level solution to build Serverless and Event Driven Applications
- Why serverless containers?
    - Simpler Abstractions
    - Autoscaling (Scale down to zero and up from zero)
    - Progressive Rollouts
    - Event Integrations
    - Handle Events
    - Plugable

![](./static/knative-serving-and-eventing.png)
/// caption
Knative Serving and Eventing
///


- Knative has two main components that empower teams working with Kubernetes. **Serving** and **Eventing** work together to automate and manage tasks and applications.
- serving and eventing各自獨立，可分別安裝使用
- Knative Serving: Run serverless containers in Kubernetes with ease. Knative takes care of the details of networking, autoscaling (even to zero), and revision tracking. Teams can focus on core logic using any programming language.
- Knative Eventing: Universal subscription, delivery and management of events. Build modern apps by attaching compute to a data stream with declarative event connectivity and developer friendly object models.

## Knative History

- Knative 最初由 Google 於 2018 年 7 月發起，並與 IBM、Red Hat、VMware 和 SAP 等公司密切合作開發。
- 發展里程碑
    - 2018 年 7 月：Knative 首次公開發布。
    - 2019 年 3 月：Build 組件演進為 Tekton，專注於 CI/CD。
    - 2019 年 9 月：Serving API 達到 v1 版本。
    - 2020 年 7 月：Eventing API 達到 v1 版本。
    - 2021 年 11 月：Knative 發布 1.0 版本，標誌著其穩定性和商業可用性。
    - 2022 年 3 月：Knative 成為 CNCF 的孵化專案。


## Knative 適合使用的情境

- 事件觸發型應用（Event-Driven Applications）當應用程式只需要在特定事件發生時執行，例如：
    - GitHub webhook: 有 push 事件時觸發自動部署流程
    - Kafka message: 有訊息進入特定 topic 時啟動處理邏輯
    - IoT 資料上傳: 設備回傳資料就處理一次
    - 定時工作: 每10分鐘執行一次資料清洗任務
- 不需要一直運行的應用 (Scale-to-zero)
    - 開發環境 API: 不常被調用，但不能下線  
    - 自助報表產生: 使用者點選時才啟動產生程式  
    - 使用者觸發的任務: 例如資料導入、轉換等臨時任務  
- 藍綠部署與灰階發布 (Blue-Green / Canary Release)
    - 發布新版本: 可將 10% 流量導向新版本  
    - 逐步擴大流量: 根據健康狀況慢慢轉移流量  
    - 快速回退: 新版有問題時立即切回舊版  
- 無伺服器函數 (FaaS) 平台建設
    - 建立企業內部 FaaS: 開發者只需提供 container 映像即可  
    - 自定義觸發條件: 可綁定 Kafka、Webhook、Cron 等  
    - 標準化事件格式: 支援 CloudEvents 標準格式  
- 結合 DevOps / GitOps 的快速交付場景
    - 自動部署 pipeline: Git push --> Tekton build --> Knative deploy  
    - GitOps Workflow: Git 設定變更 --> 自動更新 revision  
    - 多版本控管與切換: 可快速切換版本、測試、回退  
- 資源敏感型的微服務架構
    - 使用者報表服務: 白天用量高、晚上幾乎沒人用  
    - 行銷活動系統: 活動期間高峰，平常無人使用  
    - Edge/IoT 節點: 需節省 CPU/Memory 使用量  

## 不適合 Knative 的場景

- 高吞吐、低延遲常駐服務: scale-to-zero 會造成冷啟動延遲
- WebSocket / gRPC Streaming: 不支援長連線協定
- 非 HTTP 協議: Knative Serving 目前只支援 HTTP-based 請求
- 有狀態服務: Knative 僅支援 stateless container

## Eventing

- Knative Eventing is a powerful Kubernetes-based framework that enables event-driven application development. It allows developers to build loosely coupled, reactive services that respond to events from various sources. By decoupling producers and consumers of events, Knative Eventing makes it easier to scale, update, and maintain modern cloud-native applications, especially in serverless environments.
- Knative Eventing uses standard HTTP POST requests to send and receive events between event producers and sinks.
- These events conform to the [CloudEvents specifications](https://cloudevents.io/), which enables creating, parsing, sending, and receiving events in any programming language.

### Event Mesh

<figure markdown="span">
  ![](./static/knative-event-mesh.png)
  <figcaption>Knative Event Mesh</figcaption>
</figure>

- An Event Mesh is dynamic, interconnected infrastructure which is designed to simplify distributing events from senders to recipients.
- provides asynchronous (store-and-forward) delivery of messages which allows decoupling senders and recipients in time
- Event Meshes also simplify the routing concerns of senders and recipients by decoupling them from the underlying event transport infrastructure (which may be a federated set of solutions like Kafka, RabbitMQ, or cloud provider infrastructure)
- The mesh transports events from producers to consumers via a network of interconnected event brokers across any environment, and even between clouds in a seamless and loosely coupled way.
- Event producers can publish all events to the mesh, which can route events to interested subscribers without needing the application to subdivide events to channels
- Event consumers can use mesh configuration to receive events of interest using fine-grained filter expressions rather than needing to implement multiple subscriptions and application-level event filtering to select the events of interest.
- the Broker API offers a discoverable endpoint for event ingress and the Trigger API completes the offering with its event filtering and delivery capabilities

當我第一次接觸到 Knative Eventing 的 "Event Mesh" 概念時，其實有點疑惑。畢竟我以前習慣用 Kafka 這種比較直接的訊息系統，producer 把資料丟到某個 topic，consumer 訂閱那個 topic，大家各司其職、清楚明瞭。久了也就理所當然地接受了這種「大家都要知道訊息去哪、從哪來」的模式。

但後來我開始理解 Event Mesh 的時候，腦中有一種「啊，原來還可以這樣設計」的感覺。Event Mesh 不再要求 sender 跟 receiver 都知道訊息通過了哪條通道，也不需要大家硬綁在同一個 Kafka topic 上。相反地，它強調的是「事件本身」，比如這是一個來自某個來源、某種類型、發生在某個時間點的事件——這些屬性才是它能不能被處理的關鍵。系統會根據這些屬性，自動把事件送到真正需要它的地方。這中間的路怎麼走，不再是應用程式的責任，而是 Event Mesh 幫你處理好。

最讓我驚訝的是，它甚至可以在背後同時用 Kafka、RabbitMQ，甚至 cloud provider 的 Pub/Sub，作為事件傳輸的底層。換句話說，你不用選邊站，也不需要在設計初期就綁死在某個技術上。只要事件送得出來，有興趣的服務就會收到，不需要事前約好 topic、也不需要維護一堆 subscriptions。這種鬆耦合的設計讓系統擴展起來輕鬆很多，開發起來也比較自由，特別適合微服務或 serverless 架構。

如果你也曾經覺得 Kafka 的 topic 設計很靈活但越來越難管理，那我真的很推薦你看看 Event Mesh 的做法。它讓事件成為架構的主角，而不是某個工具或平台。這種轉變，對我來說不只是技術上的演進，也是一種思維上的釋放。

*Event Sources*

:   - An event source is a Kubernetes custom resource (CR), created by a developer or cluster administrator, that acts as a link between an event producer and an event sink. A sink can be a k8s service, including Knative Services, a Channel, or a Broker that receives events from an event source.
    - Apache Kafka, RabbitMQ, Amazon S3, Amazon SQS etc.

*Brokers*

:   ![](./static/knative-event-broker.png)
    Brokers are Kubernetes custom resources that define an event mesh for collecting a pool of events. Brokers provide a discoverable endpoint for event ingress, and use Triggers for event delivery. Event producers can send events to a broker by POSTing the event.


### Triggers

A trigger represents a desire to subscribe to events from a specific broker.

### Event Sinks

- When you create an event source, you can specify a sink where events are sent to from the source. A sink is an Addressable or a Callable resource that can receive incoming events from other resources.
- Knative Services, Channels, and Brokers are all examples of sinks.
- Amazon S3, SNS, SQS, Kafka, Logger, Redis Sink,

The core components of Knative Eventing include **Event Sources**, **Brokers**, **Triggers** and Sink. **Event sources** can originate from systems like GitHub (webhooks), Apache Kafka, CronJobs, Kubernetes API server events, or even custom containers that emit CloudEvents. A **Broker** acts as a central event mesh that receives and buffers incoming events. **Triggers** are routing rules that filter events from the Broker and forward them to services based on specific criteria. Currently, the most common event delivery mechanism is **HTTP** using the **CloudEvents** specification, typically in a **push-based manner** to HTTP endpoints such as Knative Services.

For example, imagine you’ve deployed Knative Eventing with a PingSource that emits an event every minute. This event is sent to a Broker, which acts as an event hub. A Trigger listens on that Broker and filters events based on attributes like the event type. When a matching event arrives, the Trigger forwards it to a Knative Service (a containerized HTTP handler). Behind the scenes, Knative handles service discovery, traffic routing, autoscaling (even from zero), and ensures that the container is activated just-in-time to handle the event. This creates a seamless, scalable, and efficient event-driven pipeline without needing to manage infrastructure manually.


## Serving

### Resources

<figure markdown="span">
  ![](./static/knative-serving-resources.png){ width=400 }
  <figcaption>Knative Serving Resources: Services, Routes, Configurations, Revisions</figcaption>
</figure>

- **Service**: The main entry point that manages the full lifecycle of your app.
- **Route**: Sends traffic to specific revisions, with support for splitting and naming.
- **Configuration**: Stores deployment settings; changes create new revisions.
- **Revision**: A read-only snapshot of code and config that auto-scales with traffic.

### Componenets

<figure markdown="span">
  ![](./static/knative-serving-architecture.png){ width=400 }
  <figcaption>Knative Serving Architecture</figcaption>
</figure>

- **Activator**:
    - It is responsible to queue incoming requests (if a Knative Service is scaled-to-zero)
    - It communicates with the autoscaler to bring scaled-to-zero Services back up and forward the queued requests.
    - Activator can also act as a request buffer to handle traffic bursts.
- **Autoscaler**: scale the Knative Services based on configuration, metrics and incoming requests.
- **Controller**: manages the state of Knative resources within the cluster
- **Queue-proxy**:
    - The Queue-Proxy is a sidecar container in the Knative Service's Pod.
    - collect metrics and enforcing the desired concurrency when forwarding requests to the user's container
    - a queue if necessary, similar to the Activator.
- **Webhooks**: validate and mutate Knative Resources.

### Networking Layer

- Knative Serving depends on a Networking Layer that fulfils the Knative Networking Specification.
- Knative Serving defines an internal `KIngress` resource, which acts as an abstraction for different multiple pluggable networking layers
- Currently, three networking layers are available and supported by the community:
    - net-istio
    - net-kourier
    - net-contour

How does the network traffic flow?

<figure markdown="span">
  ![](./static/knative-network-traffic-flow.png){ width=400 }
  <figcaption>Knative Serving Network Traffic Flow</figcaption>
</figure>

- The `Ingress Gateway` is used to route requests to the activator (proxy mode) or directly to a Knative Service Pod (serve mode), depending on the mode (proxy/serve, see here for more details).
- Each networking layer has a controller that is responsible to watch the KIngress resources and configure the Ingress Gateway accordingly.
- For the Ingress Gateway to be reachable outside the cluster, it must be exposed using a Kubernetes Service of `type: LoadBalancer` or `type: NodePort`


## References

- [Knative Serving | Knative](https://knative.dev/docs/serving/)
- [Knative Serving Architecture | Knative](https://knative.dev/docs/serving/architecture/)
- [Knative Eventing | Knative](https://knative.dev/docs/eventing/)
- [Event Mesh | Knative](https://knative.dev/docs/eventing/event-mesh/)
- [Event Sources | Knative](https://knative.dev/docs/eventing/sources/)
- [About Sinks | Knative](https://knative.dev/docs/eventing/sinks/)
- [About Brokers | Knative](https://knative.dev/docs/eventing/brokers/)
- [Using Triggers | Knative](https://knative.dev/docs/eventing/triggers/)
