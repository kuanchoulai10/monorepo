---
tags:
  - Apache Kafka
---

# Exactly Once Semantics in Kafka

- Debezium Kafka Connect Source Connectors --> [KIP-618: Exactly-Once Support for Source Connectors](https://cwiki.apache.org/confluence/display/KAFKA/KIP-618%3A+Exactly-Once+Support+for+Source+Connectors) --> [KIP-98: Exactly Once Delivery and Transactional Messaging](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
- Icerberg Kafka Connect Sink Connectors --> [KIP-447: Producer scalability for exactly once semantics](https://cwiki.apache.org/confluence/display/KAFKA/KIP-447%3A+Producer+scalability+for+exactly+once+semantics)

![](https://www.tabular.io/wp-content/uploads/2023/12/image-24.jpeg){width="500"}

## Idempotent Producers

```mermaid
sequenceDiagram
  participant P as Producer (enable.idempotence=true)
  participant B1 as Broker-1 (Leader P0)
  participant B2 as Broker-2 (Follower)
  participant B3 as Broker-3 (Follower)
  participant C as KRaft Controllers

  Note over P: 啟動
  P->>B1: InitProducerId
  B1->>C: 請求分配 ProducerId
  C-->>B1: 回覆 PID 範圍
  B1-->>P: PID, epoch

  Note over P: 針對 Partition-0，sequence=0 組批
  P->>B1: Produce(PID,epoch,seq=0,batch)
  B1->>B1: 檢查序號=預期？是
  B1->>B1: 寫入本地日誌
  par 複寫到 ISR
    B1->>B2: 複寫 batch
    B1->>B3: 複寫 batch
  end
  B2-->>B1: 複寫完成
  B3-->>B1: 複寫完成
  B1-->>P: ACK (acks=all, min.insync.replicas=2 滿足)

  Note over P: 網路抖動，重送同一批
  P->>B1: Produce(PID,epoch,seq=0,batch)  // 重傳
  B1->>B1: 看見舊序號→判定重複→不寫盤
  B1-->>P: ACK (去重成功)

  Note over B1: Leader 故障，B2 被選為新 Leader
  B1-xB1: Down
  C->>B2: 升為 Leader
  B2->>B2: 從日誌恢復 (PID,seq=0 已存在)

  Note over P: 續傳下一批 seq=1
  P->>B2: Produce(PID,epoch,seq=1,batch)
  B2->>B2: 檢查序號=預期→寫盤→複寫→ACK
  B2-->>P: ACK
```

## Transactional Producers

```mermaid
sequenceDiagram
  autonumber
  participant P as Producer (transactional.id)
  participant TC as Transaction Coordinator
  participant L0 as Leader: Topic-Partition A
  participant F0 as Follower: Partition A (replica)
  participant L1 as Leader: Topic-Partition B
  participant F1 as Follower: Partition B (replica)
  participant GC as Group Coordinator
  participant C as Consumer (isolation=read_committed)

  rect rgb(245,245,245)
    Note over P,TC: 初始化：拿 PID 與 Epoch（可被 fencing 的身分）
    P->>TC: InitProducerId(transactional.id)
    TC-->>P: ProducerId + Epoch
    P->>P: beginTransaction()
  end

  rect rgb(240,255,240)
    Note over P,TC: 觸碰分區時會被加入交易
    P->>TC: AddPartitionsToTxn([A,B])
    TC-->>P: OK
  end

  rect rgb(235,245,255)
    par 對 Partition A 寫入（具序號的 idempotent 批次）
      P->>L0: Produce(PID,Epoch,Seq... batch)
      L0->>F0: Replicate batch
      F0-->>L0: ACK
      L0-->>P: ACK（acks=all；ISR≥2 才成功）
    and 對 Partition B 寫入
      P->>L1: Produce(PID,Epoch,Seq... batch)
      L1->>F1: Replicate batch
      F1-->>L1: ACK
      L1-->>P: ACK（acks=all；ISR≥2 才成功）
    end
  end

  rect rgb(255,245,235)
    Note over P,GC: 將來源位移納入同一交易（CT/P 的 EOS）
    P->>GC: sendOffsetsToTransaction(groupId, offsets)
    GC-->>P: OK（提交時與輸出原子性落地）
  end

  alt 正常提交 (COMMIT)
    rect rgb(245,255,245)
      P->>TC: EndTxn(COMMIT)
      TC->>L0: WriteTxnMarker(COMMIT)
      L0->>F0: Replicate ControlBatch(COMMIT)
      F0-->>L0: ACK
      L0-->>TC: Marker written

      TC->>L1: WriteTxnMarker(COMMIT)
      L1->>F1: Replicate ControlBatch(COMMIT)
      F1-->>L1: ACK
      L1-->>TC: Marker written

      TC-->>P: COMMIT success
    end
    rect rgb(240,240,255)
      C->>L0: Fetch(read_committed)
      L0-->>C: 只回「已被 COMMIT 標記」的批次（跳過未決/abort）
      C->>L1: Fetch(read_committed)
      L1-->>C: 同上
    end
  else 發生錯誤 → 回滾 (ABORT)
    rect rgb(255,240,240)
      P->>TC: EndTxn(ABORT)
      TC->>L0: WriteTxnMarker(ABORT)
      L0->>F0: Replicate ControlBatch(ABORT)
      F0-->>L0: ACK
      L0-->>TC: Marker written

      TC->>L1: WriteTxnMarker(ABORT)
      L1->>F1: Replicate ControlBatch(ABORT)
      F1-->>L1: ACK
      L1-->>TC: Marker written

      TC-->>P: ABORT success
    end
    rect rgb(240,240,255)
      C->>L0: Fetch(read_committed)
      L0-->>C: 跳過 ABORT 範圍內的資料
    end
  end

  rect rgb(255,255,235)
    Note over P,TC: Fencing（同一 transactional.id 被雙活使用）
    participant P2 as Producer'(同 transactional.id)
    P2->>TC: InitProducerId(transactional.id)
    TC-->>P2: ProducerId + 更高 Epoch
    Note over P,P2: 舊 Producer (P) 後續寫入將被 broker 以 INVALID_PRODUCER_EPOCH 拒絕
  end
```

## Exactly-Once Support for Source Connectors

## References

- [Towards Debezium exactly-once delivery | Debezium Blog](https://debezium.io/blog/2023/06/22/towards-exactly-once-delivery/)
- [Exactly once delivery | Debezium Docs](https://debezium.io/documentation//reference/3.3/configuration/eos.html)