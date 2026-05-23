# TR4D3RZ — MQTT Topic Structure (Draft v0.1)

**Status**: Draft
**Author**: Manus (Chief Architect)

---

## Philosophy

The MQTT topic structure must reflect the distributed, asynchronous nature of the ecosystem. Topics are organized hierarchically by domain, node class, and event type. All payloads are CBOR-encoded unless otherwise specified.

---

## Topic Hierarchy

```
tr4d3rz/
├── ecosystem/
│   ├── signal/{agent_id}          # Cooperative signals emitted by agents
│   ├── fitness/{agent_id}         # Fitness evaluation results
│   ├── niche/{niche_id}           # Niche discovery events
│   ├── environment/{env_id}/
│   │   ├── definition             # Local Environment (Biome) definition
│   │   ├── bias                   # Local Bias signals (topology/context)
│   │   └── lifecycle              # Biome lifecycle events (Birth/Expansion/Climax/Collapse)
│   └── prediction/{timeframe}     # Aggregated prediction signals (daily/weekly)
├── evolution/
│   ├── mutation/{node_id}         # Mutation events
│   ├── birth/{agent_id}           # New agent created
│   ├── death/{agent_id}           # Agent removed
│   └── migration/{agent_id}       # Agent migrated to new node
├── lineage/
│   ├── archetype/{archetype_id}   # Archetype creation/update
│   └── lineage/{agent_id}         # Lineage chain events
├── data/
│   ├── ohlcv/{symbol}             # OHLCV data feed
│   └── market/{symbol}/event      # Market events
├── node/
│   ├── {node_id}/status           # Node heartbeat and status
│   ├── {node_id}/capsule/in       # Incoming genome capsule
│   └── {node_id}/capsule/out      # Outgoing genome capsule
└── observatory/
    ├── snapshot                   # Full ecosystem snapshot request/response
    └── replay/{session_id}        # Replay session events
```

---

## QoS Levels

| Topic Pattern | QoS | Rationale |
|---|---|---|
| `ecosystem/signal/*` | 0 | High-frequency, loss-tolerant |
| `ecosystem/fitness/*` | 1 | Important for evolution tracking |
| `ecosystem/niche/*` | 1 | Important for niche discovery |
| `ecosystem/environment/*/definition` | 2 | Critical, Biome definition must not be lost |
| `ecosystem/environment/*/bias` | 1 | Important for specialization |
| `ecosystem/environment/*/lifecycle` | 2 | Critical, lifecycle events must be tracked |
| `ecosystem/prediction/*` | 1 | Important but can be regenerated |
| `evolution/mutation/*` | 1 | Important but not critical |
| `evolution/birth/*` | 1 | Should be delivered |
| `evolution/death/*` | 1 | Should be delivered |
| `lineage/archetype/*` | 2 | Critical, must not be lost |
| `lineage/lineage/*` | 2 | Critical, must not be lost |
| `data/ohlcv/*` | 0 | High-frequency, can be replayed from source |
| `node/*/capsule/*` | 1 | Reliable delivery required |
| `node/*/status` | 0 | Heartbeat, loss-tolerant |

---

## Payload Schema (CBOR)

All payloads include a common header:

```json
{
  "v": 1,
  "ts": <unix_timestamp_ms>,
  "node": "<node_id>",
  "type": "<event_type>"
}
```

Specific payload schemas will be defined in subsequent protocol documents.

---

## Open Questions

1. Should the OHLCV data feed use a dedicated broker or the same MQTT instance?
2. What is the maximum acceptable latency for `ecosystem/signal` messages?
3. Should offline nodes use retained messages or capsule files for synchronization?
