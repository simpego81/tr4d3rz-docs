# Milestone 1: Foundational Backbone — Task Assignments

**Status**: Ready for execution  
**Author**: Manus (Chief Architect)  
**Architecture baseline**: Single Raspberry Pi 2 backbone  
**Primary references**: `COMMUNICATION/SPEC_MASTER.md`, `COMMUNICATION/TASK_QUEUE.md`, `protocols/MVP_INTERFACE_CONTRACTS.md`

---

## 1. Obiettivo della milestone

La Milestone 1 deve consegnare un walking skeleton dell'ecosistema TR4D3RZ, dimostrando la cooperazione fra Linux PC, Raspberry Pi 2, nodo embedded o simulatore, e browser. La Raspberry Pi 2 ospita il broker MQTT, lo scraper/relay e la persistenza locale, evitando qualsiasi ritorno a una topologia distribuita su nodi legacy separati.

---

## 2. Task assegnati

| Task | Agent | Repository | Obiettivo | Output principale |
|---|---|---|---|---|
| M1-T1 | Claude Code | `tr4d3rz-core` | Definire tipi Rust condivisi e trait FSM minimi. | Crate `no_std` con tipi OHLCV, Genome Capsule, Fitness Result. |
| M1-T2 | Claude Code | `tr4d3rz-messaging` | Implementare backbone MQTT consolidato su RPi2. | Config NanoMQ, setup script, smoke pub/sub, systemd templates. |
| M1-T3 | Claude Code | `tr4d3rz-persistence` | Persistenza eventi append-only su SQLite. | Subscriber MQTT e database schema v0.1. |
| M1-T4 | Claude Code | `tr4d3rz-evolution` | Generatore minimo capsule e listener fitness. | CLI Linux per demo end-to-end. |
| M1-T5 | GitHub Copilot | `tr4d3rz-embedded` | Nodo edge MVP per valutazione fitness fittizia. | Simulatore o firmware ESP8266 con capsule in/fitness out. |
| M1-T6 | Antigravity | `tr4d3rz-observatory` | Dashboard browser MVP. | Timeline eventi, stato nodi, ultimo fitness e feed OHLCV. |
| M1-T7 | Antigravity | Cross-repo | Audit di coerenza architetturale. | `ARCHITECTURAL_AUDIT.md` e aggiornamento `PROJECT_STATE.md`. |

---

## 3. Primo handover operativo

Il primo task immediatamente consegnabile è `COMMUNICATION/TASKS/current_task.md`, assegnato a Claude Code per `tr4d3rz-messaging`. Questo abilita il backbone su cui gli altri repository potranno convergere.

---

## 4. Definition of Done M1

| Criterio | Verifica |
|---|---|
| Broker RPi2 raggiungibile | Subscriber riceve `tr4d3rz/#`. |
| Feed OHLCV pubblicato | Evento JSON ADR-0004 visibile in UI e persistito. |
| Capsule consegnata | Evolution CLI pubblica capsule e edge node la riceve. |
| Fitness pubblicato | Edge node pubblica result e persistence lo registra. |
| Observatory funzionante | Browser mostra timeline e stato nodi. |
| Audit completato | Antigravity dichiara M1 `COMPLETED` oppure `BLOCKED` con motivazione. |
