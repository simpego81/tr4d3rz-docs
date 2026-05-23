# Current Task — M1-T2 Backbone MQTT Consolidato su Raspberry Pi 2

**Task ID**: M1-T2  
**Assigned Agent**: Claude Code  
**Repository target**: `tr4d3rz-messaging`  
**Status**: PENDING  
**Issued by**: Manus  
**Milestone**: M1 — Foundational Backbone

---

## 1. Obiettivo

Implementare il **backbone MQTT consolidato su Raspberry Pi 2** per l'MVP TR4D3RZ. Il risultato deve permettere a Linux PC, persistence logger, embedded node e Observatory browser di scambiare eventi attraverso un broker unico, installabile come servizio di sistema sulla RPi2.

---

## 2. Contesto obbligatorio da leggere

| Documento | Perché è necessario |
|---|---|
| `tr4d3rz-docs/COMMUNICATION/SPEC_MASTER.md` | Definisce scope e DoD dell'MVP. |
| `tr4d3rz-docs/protocols/MVP_INTERFACE_CONTRACTS.md` | Definisce payload minimi capsule, fitness ed event log. |
| `tr4d3rz-docs/protocols/mqtt-topic-structure.md` | Definisce gerarchia topic e QoS. |
| `tr4d3rz-docs/adr/ADR-0003-mqtt-broker.md` | Vincola broker e servizi al nodo centrale RPi2. |
| `tr4d3rz-docs/adr/ADR-0004-ohlcv-data-contract.md` | Definisce feed OHLCV JSON. |

---

## 3. Deliverable richiesti

| Deliverable | Percorso consigliato | Criterio di accettazione |
|---|---|---|
| Config broker NanoMQ | `config/nanomq.conf` | Porta MQTT `1883`, WebSocket ove disponibile, retained/session policy documentata. |
| Script setup RPi2 | `scripts/install_rpi2.sh` | Idempotente, non distruttivo, verifica architettura ARMv7 e dipendenze. |
| Unit/smoke publisher | `tools/publish_smoke_event.*` | Pubblica OHLCV sample, capsule sample e heartbeat. |
| Unit/smoke subscriber | `tools/subscribe_smoke_events.*` | Verifica ricezione dei topic MVP e stampa payload decodificabile. |
| Service templates | `systemd/*.service` | Template per NanoMQ e bridge/scraper se presente. |
| Implementazione log | `COMMUNICATION/IMPLEMENTATION_LOG.md` | Descrive scelte, comandi testati, limiti e TODO. |

---

## 4. Topic minimi da supportare

| Topic | Payload | QoS | Note |
|---|---|---|---|
| `tr4d3rz/data/ohlcv/intraday/{isin}` | JSON ADR-0004 | 0 | Debuggable e consumabile dalla UI. |
| `tr4d3rz/node/{node_id}/status` | JSON heartbeat | 0 | Stato base dei nodi. |
| `tr4d3rz/node/{node_id}/capsule/in` | CBOR Genome Capsule v0.1 | 1 | Input per edge node. |
| `tr4d3rz/ecosystem/fitness/{agent_id}` | CBOR o JSON-debug Fitness Result v0.1 | 1 | Output fitness MVP. |
| `tr4d3rz/observatory/snapshot` | JSON snapshot request/response | 1 | Supporto dashboard/replay. |

---

## 5. Vincoli tecnici

La soluzione deve essere compatibile con Raspberry Pi 2 ARMv7 e non deve reintrodurre dipendenze da nodi legacy separati. Eventuali fallback a Mosquitto sono ammessi solo come profilo di sviluppo documentato, mentre il target architetturale resta NanoMQ su RPi2.

---

## 6. Definition of Done

Il task è completato quando un test locale o documentato dimostra che un publisher invia almeno un heartbeat, un evento OHLCV e un fitness result, mentre un subscriber li riceve dai topic `tr4d3rz/#`. Il log deve indicare chiaramente come l'utente può replicare il test sulla Raspberry Pi 2.
