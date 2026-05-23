# TR4D3RZ — SPEC_MASTER MVP Foundational Backbone

**Status**: Active  
**Author**: Manus (Chief Architect & Technical Director)  
**Scope**: MVP / Milestone 1 — Opzione 1, **Foundational Backbone**  
**Baseline architetturale**: Single Raspberry Pi 2 come nodo centrale per broker, scraper, relay e persistenza.

---

## 1. Intento dell'MVP

L'MVP deve produrre un **walking skeleton eseguibile end-to-end** dell'ecosistema TR4D3RZ. L'obiettivo non è completare l'intero sistema evolutivo, ma dimostrare che i repository, i contratti dati e i nodi principali cooperano attraverso un flusso minimo ma reale: generazione o acquisizione dati, pubblicazione MQTT, persistenza, consumo embedded simulato o reale, e osservabilità browser.

> Il criterio guida è “interface-first”: nessun repository implementa logiche isolate senza rispettare i contratti condivisi versionati in `tr4d3rz-docs/protocols/` e negli ADR accettati.

---

## 2. Repository e responsabilità operative

| Repository | Ruolo MVP | Owner AI primario | Deliverable MVP |
|---|---|---|---|
| `tr4d3rz-docs` | Single source of truth architetturale | Manus | Contratti, task queue, stato progetto, audit checklist. |
| `tr4d3rz-core` | Tipi dati, serializzazione, FSM skeleton | Claude Code | Crate Rust `no_std` con tipi OHLCV, capsule e trait FSM minimi. |
| `tr4d3rz-messaging` | Backbone MQTT su RPi2 | Claude Code | Config NanoMQ, topic conventions, relay JSON→CBOR opzionale, smoke test. |
| `tr4d3rz-evolution` | Generatore minimo di genome capsule | Claude Code | CLI Linux che pubblica una capsule MVP e riceve fitness result. |
| `tr4d3rz-persistence` | Memoria eventi su RPi2 | Claude Code | Event logger Rust con SQLite e schema append-only. |
| `tr4d3rz-embedded` | Nodo edge MVP | GitHub Copilot | Firmware/simulatore ESP8266 che riceve capsule, calcola fitness fittizio e pubblica risultato. |
| `tr4d3rz-observatory` | UI web di monitoraggio | Gemini CLI | UI TS/Three.js o fallback DOM/Canvas che mostra topic, eventi e stato nodi. |

Il protocollo operativo menziona “4 repository” nelle istruzioni immediate, ma l'ADR-0001 accettato e la milestone M0 definiscono una decomposizione a **7 repository**. Per evitare perdita di ownership e collisioni fra domini, l'MVP viene quindi organizzato sui 7 repository esistenti, mantenendo la Milestone 1 focalizzata sul backbone.

---

## 3. Flusso end-to-end MVP

| Step | Producer | Topic / Interfaccia | Consumer | Esito atteso |
|---|---|---|---|---|
| 1 | `tr4d3rz-messaging` / scraper | `tr4d3rz/data/ohlcv/intraday/{isin}` | `tr4d3rz-persistence`, `tr4d3rz-observatory` | Dato OHLCV normalizzato visibile e persistito. |
| 2 | `tr4d3rz-evolution` | `tr4d3rz/node/{node_id}/capsule/in` | `tr4d3rz-embedded` | Capsule MVP consegnata al nodo edge. |
| 3 | `tr4d3rz-embedded` | `tr4d3rz/ecosystem/fitness/{agent_id}` | `tr4d3rz-persistence`, `tr4d3rz-evolution`, UI | Fitness fittizio ma strutturato pubblicato. |
| 4 | `tr4d3rz-persistence` | SQLite locale RPi2 | Human / Observatory replay | Eventi consultabili con query deterministiche. |
| 5 | `tr4d3rz-observatory` | MQTT WebSocket o feed bridge | Browser PC/tablet | Timeline eventi, stato nodi e ultimo fitness visibili. |

---

## 4. Contratti minimi da congelare prima dell'implementazione

| Contratto | Documento canonico | Stato MVP | Blocca i repo |
|---|---|---|---|
| Topic MQTT | `protocols/mqtt-topic-structure.md` e `protocols/MVP_INTERFACE_CONTRACTS.md` | Draft MVP normalizzato con prefisso `tr4d3rz/` | messaging, persistence, embedded, observatory. |
| OHLCV JSON | `adr/ADR-0004-ohlcv-data-contract.md` | Accepted | messaging, persistence, observatory, core. |
| Genome Capsule CBOR | `protocols/MVP_INTERFACE_CONTRACTS.md` | Da usare come v0.1 | core, evolution, embedded, persistence. |
| Fitness Result CBOR/JSON-debug | `protocols/MVP_INTERFACE_CONTRACTS.md` | Da usare come v0.1 | embedded, evolution, persistence, observatory. |
| Event Log SQLite | `protocols/MVP_INTERFACE_CONTRACTS.md` | Da usare come v0.1 | persistence, observatory. |

---

## 5. Definition of Done della Milestone 1

La Milestone 1 è completata quando una demo locale o semi-fisica mostra un flusso completo su **Linux PC + Raspberry Pi 2 + ESP8266/simulatore + browser**. Tutti gli agent devono produrre log in `COMMUNICATION/`, i test minimi devono essere eseguiti e il `PROJECT_STATE.md` deve dichiarare la milestone completata o bloccarla con motivazioni tracciate.
