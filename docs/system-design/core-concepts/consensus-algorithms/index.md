# Consensus Algorithms


!!! question "How Raft Work?"

    ??? tip "Answer"

        Raft is a consensus algorithm that **ensures all nodes in a distributed system agree on a shared log, even with failures**. It works by electing a leader, which handles all client requests and replicates log entries to followers. Followers apply entries once a majority (quorum) agrees.

        Raft has three main phases: **Leader Election**, **Log Replication**, and **Safety**. If a follower doesn't hear from a leader, it becomes a candidate and starts an election. Once elected, **the leader sends periodic heartbeats to maintain authority**. This design is easier to understand and implement compared to Paxos.
