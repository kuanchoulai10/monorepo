27;2;13~27;2;13~# Slack × Iceberg @ Scale

**來源**：[Maintaining Iceberg at Scale: Lessons from Slack | 2026 Iceberg Summit](https://youtu.be/NRSlundcwvc?si=NOw46genitJRooXX)

這場演講分享 Slack 如何把 Apache Iceberg 導入到自家數據湖倉中，從第一個 streaming ingestion 的 use case，一路擴展到 CDC、business metrics、telemetry 等關鍵流水線，以及他們在過程中累積的維運經驗。

## 1. Slack 的資料現狀

- **數據湖倉（Data Lakehouse）總量**：規模高達 **180 PB**。
- **每日 Ingest 量**：
    - 每日處理約 **250 TB** 的日誌數據（來自應用程式複製）。
    - 額外約 **55 TB** 的 CDC（Change Data Capture，變更數據擷取）數據。
- **表格與流水線**：擁有約 **35,000 張分析表**，分布在約 **29,000 條分析流水線** 中。

## 2. 使用 Iceberg 前的痛點

在採用 Iceberg 之前，Slack 主要使用 **Hive Metastore** 作為其目錄（cataloging）系統，並搭配 **Parquet** 文件格式來管理他們的數據湖。

以下是他們當時管理資料表的主要方式與面臨的挑戰：

*   **分區管理（Partitioning）**：在 Iceberg 之前，Slack 必須針對不同的分區策略**建立多個資料表副本**，這對維護來說是一個巨大的負擔。此外，一些大型資料表擁有數百萬個分區，這導致 Hive Metastore 中存在**龐大的元數據（metadata）**，影響了系統效能。
*   **手動修復與 schema 管理**：在 Hive 環境下，如果誤刪了生產環境的資料表，管理員必須嘗試找回原本的 **schema**，並透過 `repair table` 指令或**手動重新添加分區**來恢復資料，過程非常耗時且困難。
*   **文件級維護（File-level Maintenance）**：過去的資料維護（如資料保留）是透過 **S3 的生命週期策略（life cycle policies）** 在文件系統層級進行的，而非像現在 Iceberg 可以在數據集（data set）層級進行更精細的管理。
*   **資料共享限制**：在 Slack 的數據網格（data mesh）架構中，**Hive 被視為一個巨大的障礙**，限制了在不同生態系統間快速且零拷貝（zero copy）地共享數據的能力。

目前 Slack 的技術演進方向是全面**從 Hive 和 Parquet 遷移至 Iceberg**，並利用 Iceberg REST Catalog 來簡化目錄系統的抽象層。

## 3. 第一個 Use Case：從批次轉向串流 Ingestion

Slack 最初採用 Iceberg 的契機，是為了把數據攝取流程從 **批次（Batch）** 轉向 **串流（Streaming）**。

- 他們使用 **Kafka Connect** 作為工具，因為它能快速同步到數據湖中，並且 **原生支持 Iceberg**。

## 4. 擴展 Use Case：CDC 流水線

在初步成功後，Slack 將 Iceberg 應用於 CDC 流水線，結合了 **Vitess、Debezium 和 Kafka**。他們每小時執行一次合併（Merge）操作，以便在數據湖中建立上游數據的快照，並記錄變更日誌（Change Log）。

### 4.1 CDC 流水線的技術架構

Slack 的 CDC 流程主要由以下組件構成：

- **Vitess & Debezium**：用於監控與擷取上游資料庫的變更紀錄。
- **Kafka**：作為中間的訊息傳輸層，接收來自 Debezium 的變更數據。
- **Iceberg Sync（Kafka Connect）**：利用 Kafka Connect 將數據同步到 Iceberg 表格中，因為它原生支持 Iceberg 格式。

### 4.2 Merge 操作

Slack 在 CDC 流程中使用了 Merge，主要體現在以下兩個層面：

- **每小時的合併快照**：為了在數據湖中反映出上游的最新狀態，Slack 每小時執行一次 **Merge Table** 操作。目的是從變更日誌（Change Log）中創建出與上游一致的數據快照。
- **採用 Merge-on-Read（MOR）策略**：對於這類包含頻繁 Upsert（更新）和 Delete（刪除）的「易變數據」（Volatile Data），Slack 啟用了 Iceberg 的 **Merge-on-Read** 模式。
    - **優點**：提供原子性事務，能縮短持有鎖（Lock）的時間，進而大幅減少對表格的寫入壓力。
    - **挑戰**：寫入變快，但會產生較多的小文件或刪除文件（Delete Files），因此需要透過其開發的 **Ice Chipper** 系統定期執行資料壓縮（Compaction）和維護。

## 5. 關鍵資料集與新解鎖的 Use Cases

- **Business 與 Product 指標** 用上了 **Write-Audit-Publish** 模式。
- 透過 **Iceberg REST Catalog**，在 Slack 的 data mesh 之間實現 **Zero-copy sharing**（零拷貝共享）。
- 透過 **bucket partitioning**，能在大規模下處理 **Traces 與 telemetry** 資料。

## 6. 整體效能提升

- 對於 multi-petabyte 規模的分析資料集，查詢速度最高加快 **70%**。
- **Partition Evolution**：要改變分區策略時，不再需要昂貴的全表重寫。
- 可以透過 **snapshot rollback** 與 **table reregistration** 來做表格回復。
- **Redaction（資料遮蔽 / 刪除）成本顯著降低**。


## 最前面講了一些痛點，然後提到怎麼導入iceberg 後解決的了哪些痛點？最後怎麼帶到maintanance work的？
根據來源內容，Slack 在導入 Apache Iceberg 前後經歷了顯著的技術轉變。以下詳細說明其痛點、Iceberg 帶來的解決方案，以及如何延伸到維護工作（Maintenance Work）：

### **1. 導入 Iceberg 前的痛點與解決方案**

在傳統的 Hive 與 Parquet 架構下，Slack 面臨了多項挑戰，而 Iceberg 逐一解決了這些問題：

*   **分區管理的僵化：**
    *   **痛點：** 以前若需要不同的分區策略，必須針對同一份數據創建多個副本表，這造成管理上的巨大負擔。
    *   **解決方案：** Iceberg 提供**靈活分區（Flexible Partitioning）**，可以隨意切換分區方式而不需重新複製數據。
*   **元數據（Metadata）效能瓶頸：**
    *   **痛點：** 部分大型表格擁有數百萬個分區，傳統 Hive Metastore 在處理龐大元數據時效率極低。
    *   **解決方案：** 將元數據移至 **S3** 存儲，讓整個系統更精簡且反應更快。
*   **災難恢復的難度：**
    *   **痛點：** 在 Hive 中誤刪表格是場噩夢，需要手動恢復 Schema、修復表格並重新手動添加分區。
    *   **解決方案：** 在 Iceberg 中，只需指向元數據文件並在 **30 秒內重新註冊**即可恢復。
*   **數據共享與治理：**
    *   **痛點：** Hive 是數據網格（Data Mesh）共享中的一道障礙。
    *   **解決方案：** 透過 Iceberg 的 **REST Catalog**，實現了生態系統內部的**零複製（Zero-copy）數據共享**。
*   **性能與安全：**
    *   **解決方案：** 透過文件剪裁（File Pruning），查詢性能提升了 **70%**；此外，數據脫敏（Redaction）可以精確鎖定特定文件，不再需要處理整個數據集。

---

### **2. 如何帶到維護工作（Maintenance Work）？**

雖然 Iceberg 解決了許多痛點，但隨著採用規模擴大，Slack 發現了新的挑戰：

*   **採用的「平原期」（Plateau）：**
    演講者提到，Iceberg 的採用曲線在初期快速增長後突然停滯（Flatlined）。調查後發現，阻礙增長的「摩擦力」主要來自於：**缺乏統一的維護機制**。

*   **維護是 Iceberg 的「隱形代價」：**
    演講者強調「維護是採用 Iceberg 的成本（Maintenance is the cost of adopting Iceberg）」。特別是對於以下類型的數據，維護變得不可或缺：
    *   **串流數據（Streaming）：** 寫入頻繁會產生大量小文件，需要進行**壓縮（Compaction）**。
    *   **易變數據（Volatile）：** 頻繁的 Upsert 與 Delete 操作會產生大量刪除文件（Delete files），若不處理會拖慢查詢性能。
    *   **存儲管理：** 隨著快照增加，會產生大量過期數據和孤立文件（Orphan files），必須定期清理以控制數據湖成本。

*   **從「各司其職」轉向「集中管理」：**
    Slack 最初考慮讓各數據團隊自行負責維護，但發現這樣會帶來極高的**上門檻成本（Onboarding cost）**、知識傳遞負擔以及執行不一致的問題。為了讓各團隊專注於數據分析而非底層設施（Plumbing），Slack 最終決定開發一個中央服務——**Ice Chipper**。

*   **集中維護系統（Ice Chipper）的誕生：**
    這個系統利用 **Airflow** 編排和 **Spark** 執行，自動化處理快照過期、清單重寫、孤立文件刪除及數據壓縮等任務。透過解決這些維護上的摩擦，Iceberg 的採用率隨即突破了平原期，並開始呈倍數增長。

在開發 **Ice Chipper** 之前，Slack 針對如何處理 Apache Iceberg 的維護工作進行了多層面的思考，主要從「組織管理」與「現成產品」兩個角度進行評估：

## 提到Ice Chipper 前，有哪些選項在思考？他們怎麼思考的？

### **1. 組織管理面的選項與思考**
Slack 最初從「誰該負責維護」的角度出發，考慮了以下三種模式：

*   **選項一：由各數據團隊（Data Teams）自行負責維護**
    *   **思考方式：** 既然這些分析團隊擁有數據、創建了表格，理論上他們最適合運行維護任務。
    *   **否決原因：** 這會產生極高的**上門檻成本（Onboarding costs）**，需要大量的知識傳遞與 Iceberg 教育訓練，且容易導致各團隊間的**執行標準不一**，成為團隊持續的負擔。

*   **選項二：提供精選腳本或自助服務（Curated Scripts / Self-service）**
    *   **思考方式：** 這是對選項一的優化嘗試，透過提供統一的工具讓團隊自己運行，藉此降低入職負擔並提高維護的一致性。

*   **選項三：構建集中式管理服務（最終選擇的 Ice Chipper 方向）**
    *   **思考方式：** 數據團隊明確表達他們「**只想關注數據內容與見解，不想管底層的『管路』工程（Plumbing）**」。
    *   **結論：** Slack 認同團隊不應在意底層是 Hive 還是 Iceberg，因此決定由基礎架構團隊建立中央服務，實現**零入職成本**、**一致的執行標準**，讓使用者專注於數據本身。

### **2. 外部技術產品的評估**
除了內部開發，Slack 也曾評估過現成的解決方案：

*   **選項：Amazon S3 Tables**
    *   **思考方式：** Slack 曾與 AWS 團隊討論此產品是否能自動處理壓縮與維護。
    *   **否決原因：** 在大約一年半前評估時，該產品的功能尚無法滿足 Slack 對**微調（Fine-tuning）**的需求，例如：無法精確控制維護頻率，或是進行能優化文件剪裁（File Pruning）的**內部排序（Internal Sorting）**。因此，Slack 決定繼續留在標準的 S3 上，並自行開發維護系統。

### **3. 維護策略的核心思考**
在決定開發系統後，他們將數據分為四類（靜態、僅追加、串流、易變），並根據這些類型的特性來思考維護需求：
*   **非全有即全無：** 思考維護時，他們認為「有進度比沒進度好」，因此系統應支持**部分進度（Partial progress）**，而非失敗就全部重來。
*   **利用既有設施：** 為了減少外部依賴，他們優先思考如何利用公司已有的 **Airflow（調度）** 與 **Amazon EMR（Spark 執行）** 基礎設施。

## slack 怎麼思考這四類的資料種類？

根據來源內容，Slack 將其數據湖中的資料分為四大類，這種分類法是為了針對不同特性的資料制定最有效的**維護策略（Maintenance Strategy）**與 **SLA（服務等級協議）**。

以下是 Slack 對這四類資料的思考方式與分類細節：

### **1. 靜態數據 (Static Data)**
*   **定義與範例：** 變動極少的資料，例如計費層級（Billing Tiers）。這類資料在 Slack 可能每兩到三年才更動一次。
*   **讀寫模式：** 一次寫入，多次讀取。
*   **維護思考：** 由於幾乎沒有新的快照產生，Slack 認為這類資料**不需要每天執行快照過期（Snapshot Expiration）**等維護操作，可以降低維護頻率。這屬於維護成本最低的類型。

### **2. 僅追加數據 (Append-only Data)**
*   **定義與範例：** 主要是批次處理（Batch）的資料，例如用於長期追蹤分析的日誌，通常按小時或按天追加。
*   **讀寫模式：** 一次寫入，多次讀取；有時會進行分區的覆寫（Insert Overwrite）。
*   **維護思考：** 與靜態數據類似，這類資料的維護相對簡單，通常能在幾分鐘內完成。

### **3. 串流數據 (Streaming Data)**
*   **定義：** 頻繁且持續寫入的資料。
*   **面臨挑戰：** 由於寫入頻率高，會產生大量的**小文件**，嚴重影響查詢效能。
*   **維護思考：** 
    *   **資料壓縮（Compaction）**對這類資料至關重要。
    *   Slack 考慮為其設定更嚴格的 SLA，例如**每小時執行一次維護**（而非每天），透過提高頻率來縮小每次處理的資料量，進而減少所需資源並提高系統可靠性。

### **4. 易變數據 (Volatile Data)**
*   **定義：** 包含頻繁更新（Upserts）與刪除（Deletes）的資料，通常涉及複雜的合併操作。
*   **技術特性：** 如果表格使用 **Merge-on-Read (MOR)** 模式，通常就屬於此類。
*   **維護思考：** 
    *   這是**最難維護**的一類資料，因為會產生大量的「刪除位置文件」（Delete Position Files），必須定期重寫以維持效能。
    *   維護難度會隨著數據量的增加而呈複合式增長。

### **總結：維護的共通性與差異性**
Slack 在思考這四類資料時，將維護操作分為兩類：
*   **普遍性操作 (Ubiquitous)：** 無論哪一類，都必須執行**快照過期**、**清單重寫（Manifest Rewrites）**以及**孤立文件刪除（Orphan File Deletion）**，以確保查詢計畫快速並控制存儲成本。
*   **選擇性操作 (Opt-in)：** 僅針對「串流」與「易變」數據執行**資料壓縮**與**刪除文件重寫**。

透過這種分類，Slack 的中央維護系統 **Ice Chipper** 能夠根據資料類型優先執行輕量級、低風險的操作，再處理重量級、高風險的任務，從而達到 99.9% 的維護成功率。


## maintenance requirements

Slack's centralized maintenance service, **Ice Chipper**, was designed to eliminate the "friction" and "ongoing burden" that individual data teams faced when trying to manage their own Iceberg tables. The system follows a specific set of requirements and operational mandates to ensure the data lake remains performant and cost-effective.

### **Maintenance Requirements**
Slack established several core requirements for how maintenance must be performed across their 35,000 analytical tables:
*   **Frequency:** Maintenance should be run on every table **at least once a day**. For high-volume streaming datasets, they are moving toward **hourly maintenance** to reduce input sizes and improve reliability.
*   **Partial Progress:** The service must be able to make **partial progress** rather than following an "all or nothing" approach, as some progress is always better than none.
*   **Infrastructure Leverage:** To minimize external dependencies, the service should leverage existing infrastructure, specifically **Airflow** for orchestration and **Spark on EMR** for execution.
*   **Visibility and Tracking:** The system must **track every operation** (start/end times, success/failure, metadata like files rewritten) and surface errors to dashboards for on-call investigation.
*   **Idempotency and Resiliency:** Since Spark jobs can fail, the service must be **idempotent**, allowing it to reacquire locks and resume work upon restart.

### **What the Service Should Do (Core Operations)**
The service categorizes maintenance tasks into "ubiquitous" operations (required for all) and "opt-in" operations (based on data type):

**Ubiquitous Operations (Run on all tables):**
*   **Snapshot Expiration:** To prevent the accumulation of old data versions.
*   **Manifest Rewrites:** To optimize query planning and keep it fast across different execution engines.
*   **Orphan File Deletion:** To manage the size of the lakehouse by deleting files no longer accessible or registered.
*   **Data Retention:** Conceptualizing retention at the **dataset layer** (e.g., keeping 90 days of data) rather than just the file-system level.

**Opt-in Operations (Data-type specific):**
*   **Compaction (Data File Rewriting):** Crucial for **streaming data** to merge the "lots of tiny files" created during frequent writes.
*   **Rewriting Delete Position Files:** Essential for **volatile data** (those using Merge-on-Read) to maintain query performance.

### **Service Execution Logic**
To maintain a 99.9% success rate, the service follows a specific operational flow:
*   **Dynamic Discovery:** It must automatically find Iceberg tables in the catalog, allowing for seamless onboarding and offboarding.
*   **Concurrency Locking:** It must **lock tables** during maintenance to ensure no two maintenance actors work on the same table simultaneously, which would otherwise create more orphan files.
*   **Ordered Execution:** It should run operations from **most lightweight/least risky to heaviest/most risky**. Required (ubiquitous) tasks are performed first, followed by opt-in tasks like compaction.
*   **Time-Boxing:** Jobs should be killed after **24 hours** to prevent "starving" other tables and ensure the EMR clusters remain healthy.
*   **Write Pressure Management:** When updating its own internal tracking and locking tables, the service should use **batch inserts** and **Merge-on-Read** to reduce snapshot frequency and write pressure.


## icechipper 的系統架構長怎樣？為什麼樣lock 機制？怎麼做到的？

根據來源內容，Slack 開發的 **Ice Chipper** 是一個集中式的 Apache Iceberg 維護服務，其系統架構與鎖定（Locking）機制說明如下：

### **Ice Chipper 的系統架構**
Ice Chipper 的架構旨在實現自動化與規模化，主要包含以下組件：
*   **探索服務（Discovery Service）：** 定期從目錄（Catalog）中讀取資訊，動態識別現有的 Iceberg 表格，確保新表格自動加入維護，且已刪除的表格能自動移除。
*   **編排與執行（Airflow & Spark on EMR）：** 由 **Airflow** 定期觸發任務，並在 **Amazon EMR** 上運行 **Spark** 腳本執行具體的維護操作。
*   **追蹤與鎖定表（Tracking & Locking Tables）：** Slack 並未額外使用外部數據庫（如 Aurora），而是直接利用 **Iceberg 表格**來紀錄任務狀態與管理併發鎖定。
*   **儀表板（Dashboards）：** 將追蹤表中的元數據（如重寫的文件數量、成功/失敗紀錄、報錯堆棧等）可視化，供維護人員監控與調查。

### **為什麼需要鎖定機制？**
鎖定機制的主要目的是：
*   **防止併發衝突：** 確保**沒有兩個維護執行者（Maintenance Actors）同時對同一張表進行操作**。
*   **減少孤立文件（Orphan Files）：** 如果多個維護任務同時處理同一張表，會導致產生大量無法被目錄追蹤的孤立文件。
*   **不影響業務運作：** 此鎖定僅針對 Ice Chipper 內部的維護者，**不會阻礙**外部的分析流水線（Analytical Pipelines）對數據進行讀取或寫入。

### **鎖定機制是如何做到的？**
Slack 透過以下技術細節實現了具備彈性的鎖定功能：
*   **利用 Merge 操作獲取鎖：** Spark 任務在執行維護前，會對「鎖定表」執行 **Merge 操作**來嘗試獲取該表的鎖定權。
*   **以 Run ID 作為唯一識別：** 系統將 Spark 應用程序的 **Run ID** 作為鎖定表的主鍵（Primary Key）。這確保了冪等性（Idempotency），如果任務失敗重啟，它可以憑藉相同的 Run ID 重新獲取或更新原本屬於該批次的鎖定。
*   **優化寫入壓力：** 由於頻繁寫入鎖定表會產生壓力，Slack 採用了兩大策略：
    *   **批量寫入（Batch Inserts）：** 盡可能減少提交頻率，避免產生過多小文件與快照。
    *   **啟用讀時合併（Merge-on-Read, MOR）：** 利用 MOR 的原子事務特性縮短持有鎖的時間窗口，從而顯著減輕對鎖定表的寫入壓力。
*   **自動釋放：** 若任務因基礎設施故障等原因掛掉，系統設有 24 小時超時機制，超時後該表格會重新釋出，供下一輪維護使用。

Discovery

• Dynamic on and off boarding: Scans catalog to find and register all Iceberg tables
• Marks each table as active and eligible for maintenance
• Should allow manual overrides to skip maintenance

Tracking

• Keeps operation-level details of maintenance for every table

Lock/Semaphore

• Ensure table maintenance isn’t duplicated; acted upon by one actor at a time
• Doesn’t impede reads/writes from outside actors; only restricts maintenance service

Spark Job

• On a cadence, finds a batch of table due for maintenance from Discovery table
• Acquires locks via MERGE into Lock table
• Runs all maintenance operations in a defined order
◦ Required, then opt-in
• Parallelizes execution across tables using Spark Jobs
• Killed after 24 hours, making tables eligible again

Idempotency & Resilience

- Upon any restart, locks are reacquired based on Run ID and refreshed via MERGE into Lock table
- Errors are grouped and prioritized for On-Call to fix

## icechipper 的result 長怎樣？有四大點
根據來源內容，**Ice Chipper** 是 Slack 開發的集中式管理維護服務，其執行後的**結果（Result）**主要可以總結為以下四大指標：

1.  **廣泛的維護規模**：目前 Ice Chipper 負責維護超過 **4,000 張資料表**。
2.  **極高的作業成功率**：在所有的維護操作中，達到了 **99.9% 的成功率**。
3.  **高效的批次處理能力**：
    *   每個批次（Batch）大約處理 **35 張資料表**。
    *   批次平均執行時間約為 **15 分鐘**。
    *   其中最核心、輕量級的操作非常快速，處理 35 張表僅需約 **2 分鐘**。
4.  **強大的大數據處理實力**：
    *   能夠管理極為複雜且龐大的資料表，其中最大的規模甚至達到 **17 PB**。
    *   處理能力足以應對每日產生的**數百萬個孤立文件（orphan files）**的刪除與清理。

此外，由於 Ice Chipper 穩定了維護作業，克服了導入初期因維護不便而產生的停滯期，使 Slack 的 Iceberg 採用率在短時間內**翻倍並持續加速成長**。

## ice chipper 也不是完美的。它們有哪些known failures?看起來有分成三點

妳的觀察非常正確！根據來源內容中 Lawrence 的演講，**Ice Chipper 的已知問題（known failures）** 確實在投影片中被歸納為以下三大類，這也是 Slack 團隊目前最主要的挑戰：

1.  **孤立文件刪除問題 (Orphan File Deletion)**：
    *   **驅動程式記憶體不足 (Driver OOM)**：這是最常見的失敗原因。當刪除程序完成後，會將所有已刪除文件的清單回傳給驅動程式。如果一個批次中刪除了數百萬個文件（例如 200 萬個），即使驅動程式有 **80 GB 的記憶體**也可能崩潰。雖然文件實際上已被刪除，但系統會因此失去追蹤與紀錄的可視性。
    *   **AWS 速率限制 (Rate Limiting)**：刪除操作執行過快時會觸發 AWS 限制，導致僅能**部分刪除**，未完成的刪除會累積到下一次，使問題變得更嚴重。

2.  **統計性批次衝突 (Statistical Batch Clashing)**：
    *   這發生在多個**大型且高流量的串流資料表**同時被排定進行資料壓縮（compaction）時。
    *   這些沉重的任務會**消耗掉所有資源**，導致較小的資料表無法獲得維護資源（資源飢餓），或是因為達到 **24 小時的超時限制**而被迫停止。
    *   這會產生惡性循環，因為未完成的維護會被排入下一個批次，導致問題像滾雪球般擴大。

3.  **邊際案例 (Edge Cases) — S3 生命週期策略衝突**：
    *   Slack 過去針對資料集有大量的 **S3 生命週期策略**（針對檔案級別的刪除）。如果轉換到 Iceberg 後忘記移除這些舊策略，兩者會產生衝突。
    *   S3 策略可能會誤刪 Iceberg 的 **manifest 或數據文件**，導致查詢時出現錯誤。雖然 Slack 的 bucket 有開啟版本控制（versioned）可以救回資料，但這反映了從檔案級維護過渡到資料集級維護期間的陣痛期。

## Slack 對 Ice Chipper 的 future plan

根據來源內容，Slack 針對 Ice Chipper 的未來計畫可歸納為以下四大面向：

### 1. 擴展能力 (Expanding Capabilities)
*   **新 Manifest 任務**：計畫納入 **Puffin 檔案**，利用其提供的統計數據 (stats) 與分區統計數據 (partition stats) 來進一步優化查詢規劃與剪裁效能。
*   **評估 Temporal 編排**：目前使用 Airflow，但正考慮轉向 **Temporal** 以追求更成熟的運算與操作模型。這將允許系統**動態創建批次**（不再只是按表格分組，而是按需要執行的「操作類型」來分組）。
*   **按關鍵程度區分 SLA**：針對不同類型的數據（靜態、追加、流式、揮發性）設定不同的維護頻率。例如，靜態數據不需要每天過期快照，而**流式數據（Streaming data）則可能需要增加到每小時進行一次壓縮**，以縮減輸入規模並提高系統可靠性。

### 2. 孤兒檔案刪除轉向 (Remove Orphan File Deletion Pivot)
*   **目前問題**：主要面臨兩大挑戰：一是**驅動程式記憶體不足 (OOM)**，因為刪除程序會回傳所有已刪除檔案的清單，當檔案數量極大時會撐爆記憶體；二是 **AWS 速率限制 (Rate limiting)**，過快的大規模刪除操作會觸發雲端服務商的限制，導致任務失敗並產生堆疊追蹤 (stack trace)。
*   **可能替代方案**：計畫改用**預演模式 (dry run mode)** 來收集待刪除檔案，並將其放入**緩衝系統或隊列**中處理，以受控的速度進行刪除來避免速率限制。此外也參考了 Salesforce 團隊的做法，透過比對 S3 清單與 Iceberg 元數據來手動找出孤兒檔案。

### 3. 壓縮操作轉向 (Compaction Pivot)
*   **目前問題**：壓縮操作有時表現得不夠聰明（例如無故重新壓縮整個資料集，而非僅處理新分區）。特別是對於**流式和揮發性數據**，由於產生大量小檔案，壓縮任務變得異常沉重且難以維護。
*   **可能解決方案**：
    *   **設定邊界**：僅壓縮特定時間範圍內的數據（例如**最近 7 天**），這已被證明非常有效。
    *   **解耦運作**：將耗時的壓縮任務與其他輕量級維護操作分離，以便針對重型任務更精確地調配運算資源。

### 4. 選擇性操作解耦 (Opt-in Decoupling)
*   **核心理念**：將「核心維護操作」（如快照過期、Manifest 重寫等，通常非常快速且可靠）與「選擇性/重型操作」（如數據壓縮、孤兒檔案刪除）**進行解耦 (Decouple)**。
*   **預期效益**：核心操作在批次處理中通常只需幾分鐘即可完成。透過解耦與不同的編排方式，可以確保**重型任務不會拖累或導致核心任務超時**，並能根據任務特性優化資源分配。

### 5. 補充：更廣的方向

*   **引入新功能與優化查詢**：計畫納入 **Puffin 檔案**，利用其提供的統計數據（stats）和分區統計數據（partition stats）來進一步提升查詢規劃與效能。
*   **改進調度與作業模型**：
    *   考慮將編排工具從 Airflow 轉向 **Temporal**，以實現更成熟的運作。
    *   從目前簡單的表格分組，轉向**動態創建批次**，改為根據需要執行的「操作類型」來分組。
*   **實施差異化服務水準協議 (SLA)**：針對不同類型的數據（如靜態、追加型、流式、揮發性）設定不同的維護頻率。例如，靜態數據不需每天清理，而**流式數據（Streaming data）則可能需要增加到每小時進行一次壓縮**，以減少資源消耗並提高可靠性。
*   **AI 倡議**：探索將 **AI 納入決策過程**或用於自動調整（tuning）維護操作的運行方式。
*   **優化孤兒檔案（Orphan File）刪除**：
    *   為解決目前的記憶體不足（OOM）和 AWS 速率限制問題，計畫採用「預演模式」（dry run mode）來收集待刪除檔案。
    *   考慮建立**緩衝系統（Buffered system）或隊列**來處理刪除操作，以避免觸發雲端服務商的限制。
*   **解耦維護操作**：計畫將耗時較長的「選擇性操作」（如數據壓縮 compaction）與快速的「核心操作」**解耦（Decouple）**，以便更精確地針對重型任務調配資源。
*   **成為社群貢獻者**：Slack 希望從目前的觀察者（lurkers）轉變為 **Apache Iceberg 的積極貢獻者**，分享他們在參數調整與優化方面的經驗。
*   **重新評估 Catalog**：正在重新評估長期使用的 Hive Catalog 策略，雖然目前尚無確定的替代方案。


## 後續的提問

在 Lawrence 的演說結束後，現場觀眾提出了關於技術細節與架構選擇的多個問題，Lawrence 的回答摘錄如下：

### 1. 關於 Catalog 的選擇
*   **提問：** Slack 目前使用哪種 Catalog？
*   **回答：** 目前仍在使用 **Hive Catalog**，並在其上層架設了 **Iceberg REST Catalog** 以提供 Data Mesh 的存取能力。不過，他們正長期評估是否要替換 Hive，只是目前尚未有確定的替代策略。

### 2. 關於 S3 Tables 的自動維護
*   **提問：** 是否考慮過使用 S3 Tables（宣稱可自動處理壓縮與維護）？
*   **回答：** 他們在大約一年半前產品剛推出時曾與 AWS 討論過。當時 S3 Tables **缺乏他們需要的微調功能**（例如調整維護頻率、內部排序以優化檔案剪裁等），因此目前仍維持使用基本的 S3 Standard Tier。他認為 Slack 目前的規模已經過了適合轉向該產品的時機。

### 3. 關於分區（Partitioning）的調優
*   **提問：** 在如此大規模下，如何決定與調優分區策略？
*   **回答：** 通常是在效能變慢時進行重估。首先會看是否能讓利害關係人進行更細粒度的數據聚合。針對 PB 級的大表，他們會特別注意**數據傾斜（Data Skew）**問題。解決方案包括使用**分桶（Bucketing）**策略，或是手動將高流量的分區獨立出來，其餘則歸入預設桶中。這目前仍是一個包含手動操作且存在些微低效率的過程。

### 4. 關於刪除孤兒檔案的安全性
*   **提問：** 在不鎖定表格的情況下，如何確保不會誤刪尚未提交（Commit）到表格的新檔案？
*   **回答：** Lawrence 指出 `remove_orphan_files` 程序通常有一個**時間邊界（Time Boundary）**（他印象中約為 24 小時），小於該時間的檔案不會被刪除。由於 Slack 的流式寫入每 5 到 15 分鐘提交一次，且批次作業通常不超過 24 小時，因此這個時間窗口足以保護未提交的檔案。

### 5. 關於維護難易度的比較（COW vs. MOR）
*   **提問：** Copy-on-Write (COW) 和 Merge-on-Read (MOR) 哪種表較容易維護？
*   **回答：** 他認為難易度不在於寫入模式，而在於**變動頻率與數據量**。**流式數據**（產生大量小檔案需壓縮）與**高波動性數據（Volatile data）**（頻繁更新與刪除）是最難維護的。相比之下，靜態或追加型的批次數據（Static/Append-only batch）維護起來最簡單，通常幾分鐘就能完成。

### 6. 關於攝入工具對維護的影響
*   **提問：** 使用 Flink CDC 與 Debezium/Kafka 在維護上有何差異？
*   **回答：** 從維護角度看差異不大，兩者都會產生大量小檔案而需要壓縮。Slack 主要使用 Kafka Connect，並透過調優參數（如將輸出檔案目標設為 512MB 而非預設的 32MB）來優化後續維護。他提到雖然 Flink 有其優點，但 Kafka Connect 對他們來說更輕量且能快速上線。
