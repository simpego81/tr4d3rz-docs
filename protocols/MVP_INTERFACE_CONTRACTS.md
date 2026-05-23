# TR4D3RZ — MVP Interface Contracts v0.1

**Status**: Draft for implementation  
**Author**: Manus  
**Scope**: M1 Foundational Backbone  
**Compatibility target**: Linux PC, Raspberry Pi 2 ARMv7, ESP8266/STM32 class edge nodes, browser Observatory.

---

## 1. Convenzioni generali

Tutti i topic MQTT dell'MVP devono usare il prefisso `tr4d3rz/`. I payload OHLCV restano JSON per coerenza con ADR-0004 e per favorire il debug, mentre genome capsule e fitness result devono essere trattati come strutture compatibili CBOR; durante i primi smoke test è ammesso un profilo `application/json-debug` con gli stessi campi.

| Campo comune | Tipo | Obbligatorio | Descrizione |
|---|---|---|---|
| `v` | unsigned int | Sì | Versione schema, inizialmente `1`. |
| `ts` | unsigned int | Sì | Unix timestamp in millisecondi. |
| `node` | string | Sì | Identificativo del nodo producer. |
| `type` | string | Sì | Tipo evento o payload. |

---

## 2. Genome Capsule v0.1

**Topic principale**: `tr4d3rz/node/{node_id}/capsule/in`  
**Encoding target**: CBOR  
**QoS**: 1

| Campo | Tipo | Obbligatorio | Descrizione |
|---|---|---|---|
| `v` | u8 | Sì | Versione schema. |
| `ts` | u64 | Sì | Timestamp creazione. |
| `node` | string | Sì | Producer, tipicamente evolution node. |
| `type` | string | Sì | Valore `genome_capsule`. |
| `agent_id` | string | Sì | Identificativo agente/FSM. |
| `generation` | u32 | Sì | Generazione evolutiva. |
| `genome_hash` | string | Sì | Hash stabile del genoma. |
| `fsm` | map | Sì | FSM MVP serializzata. |
| `budget` | map | No | Limiti di esecuzione per edge node. |

Esempio JSON-debug equivalente:

```json
{
  "v": 1,
  "ts": 1779541200000,
  "node": "linux-evolution-01",
  "type": "genome_capsule",
  "agent_id": "agent-demo-001",
  "generation": 0,
  "genome_hash": "sha256:demo",
  "fsm": {
    "states": ["idle", "long", "flat"],
    "initial": "idle",
    "transitions": [
      {"from": "idle", "to": "long", "when": "close_gt_open"},
      {"from": "long", "to": "flat", "when": "close_lt_open"}
    ]
  },
  "budget": {"max_ticks": 128, "max_ms": 1000}
}
```

---

## 3. Fitness Result v0.1

**Topic principale**: `tr4d3rz/ecosystem/fitness/{agent_id}`  
**Encoding target**: CBOR o JSON-debug  
**QoS**: 1

| Campo | Tipo | Obbligatorio | Descrizione |
|---|---|---|---|
| `v` | u8 | Sì | Versione schema. |
| `ts` | u64 | Sì | Timestamp completamento valutazione. |
| `node` | string | Sì | Nodo che ha valutato la capsule. |
| `type` | string | Sì | Valore `fitness_result`. |
| `agent_id` | string | Sì | Agente valutato. |
| `genome_hash` | string | Sì | Hash del genoma valutato. |
| `fitness` | f64 | Sì | Valore scalare normalizzato per MVP. |
| `metrics` | map | No | Metriche accessorie, per esempio trades, drawdown, latency. |
| `status` | string | Sì | `ok`, `error`, `timeout`. |

---

## 4. Node Status v0.1

**Topic principale**: `tr4d3rz/node/{node_id}/status`  
**Encoding target**: JSON  
**QoS**: 0

| Campo | Tipo | Obbligatorio | Descrizione |
|---|---|---|---|
| `v` | u8 | Sì | Versione schema. |
| `ts` | u64 | Sì | Timestamp heartbeat. |
| `node` | string | Sì | Identificativo nodo. |
| `type` | string | Sì | Valore `node_status`. |
| `role` | string | Sì | `broker`, `evolution`, `embedded`, `persistence`, `observatory`. |
| `state` | string | Sì | `booting`, `ready`, `degraded`, `offline`. |
| `uptime_s` | u64 | No | Uptime in secondi. |

---

## 5. Event Log SQLite v0.1

Il repository `tr4d3rz-persistence` deve usare uno schema append-only iniziale. L'obiettivo non è modellare tutto il dominio, ma garantire replay e audit degli eventi MVP.

| Colonna | Tipo SQLite | Obbligatoria | Descrizione |
|---|---|---|---|
| `id` | INTEGER PRIMARY KEY | Sì | Sequenza locale. |
| `ts` | INTEGER | Sì | Timestamp evento. |
| `topic` | TEXT | Sì | Topic MQTT completo. |
| `event_type` | TEXT | Sì | Tipo evento estratto dal payload. |
| `node` | TEXT | No | Nodo producer. |
| `agent_id` | TEXT | No | Agente se presente. |
| `payload_encoding` | TEXT | Sì | `json`, `cbor`, `json-debug`. |
| `payload` | BLOB | Sì | Payload raw. |
| `ingested_at` | INTEGER | Sì | Timestamp di ingestione sulla RPi2. |

---

## 6. Criterio di compatibilità

Ogni repository consumer deve ignorare campi sconosciuti e fallire in modo esplicito quando mancano campi obbligatori. Le modifiche breaking devono incrementare la versione `v` e aggiornare questo documento prima di modificare il codice.
