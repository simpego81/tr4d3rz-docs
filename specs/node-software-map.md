# TR4D3RZ — Mappa del Software per Nodo

**Stato**: Draft
**Autore**: Manus (Chief Architect)

Questo documento definisce l'inventario del software in esecuzione su ciascuna classe di nodo dell'ecosistema TR4D3RZ.

---

## 1. Core Infrastructure Node (Raspberry Pi 1)

Il nodo centrale di infrastruttura gestisce la raccolta dati e lo smistamento dei messaggi. Date le limitazioni hardware (ARMv6l, 700MHz), il software è selezionato per la massima efficienza.

| Software / Componente | Repository di Origine | Stack Tecnologico | Descrizione e Note |
|---|---|---|---|
| **NanoMQ** | (Emqx/NanoMQ) | C | Broker MQTT ultra-leggero compilato da sorgente per ARMv6l. Sostituisce Mosquitto per evitare bug di compilazione noti su questa architettura. Espone la porta TCP 1883 e WebSocket 8083. |
| **Data Scraper** | `borsa-italiana-scraper` | Node.js 14.15.1 | Script di ingestion che interroga le API di Borsa Italiana. È stato adattato (downgrade di `p-limit`) per girare su Node 14. Converte i dati in formato JSON standardizzato e li pubblica su MQTT. |
| **Event Logger** (Futuro) | `tr4d3rz-persistence` | Rust | Demone che si iscrive a tutti gli eventi MQTT e li salva in append-only su un database SQLite locale. |

---

## 2. Evolution Nodes (PC Linux / Android Potenti)

I nodi evolutivi sono i "muscoli" del sistema. Eseguono il grosso del carico computazionale, generando genomi e valutando le fitness.

| Software / Componente | Repository di Origine | Stack Tecnologico | Descrizione e Note |
|---|---|---|---|
| **L-System Engine** | `tr4d3rz-core` | Rust | Generatore di genomi ibridi (grafo) a partire da grammatiche L-System. |
| **FSM Runtime** | `tr4d3rz-core` | Rust | Motore di esecuzione ad alte prestazioni che compila il genoma grafo in una Macchina a Stati Finiti ed elabora il flusso dati OHLCV in tempo reale. |
| **Evolution Engine** | `tr4d3rz-evolution` | Rust | Gestisce le popolazioni di agenti, applica operatori di mutazione strutturale e calcola la fitness multi-dimensionale. |
| **MQTT Client** | `tr4d3rz-messaging` | Rust | Sottosistema di comunicazione per ricevere i dati OHLCV dal Core Node e pubblicare i risultati di fitness e i segnali cooperativi. |

---

## 3. Optimization Nodes (ESP8266 / STM32)

Nodi hardware embedded dedicati a compiti di ottimizzazione locale, validazione e micro-tuning.

| Software / Componente | Repository di Origine | Stack Tecnologico | Descrizione e Note |
|---|---|---|---|
| **Micro FSM Runtime** | `tr4d3rz-embedded` | C / Rust (no_std) | Versione minimale del runtime FSM progettata per girare in <80KB di RAM senza allocazione dinamica eccessiva. |
| **Capsule Manager** | `tr4d3rz-embedded` | C | Gestore della serializzazione CBOR per importare/esportare genomi tramite UART o USB, utile per nodi che non hanno connettività WiFi. |
| **Micro MQTT** (solo ESP) | `tr4d3rz-embedded` | C | Client MQTT leggero per ESP8266 per la comunicazione diretta con NanoMQ. |

---

## 4. Observatory Nodes (Browser / Tablet)

Nodi passivi dedicati esclusivamente all'osservabilità, alla visualizzazione e al replay dell'ecosistema.

| Software / Componente | Repository di Origine | Stack Tecnologico | Descrizione e Note |
|---|---|---|---|
| **Ecosystem UI** | `tr4d3rz-observatory` | TypeScript, React | Interfaccia utente globale (Deploy Map, Theory Map). |
| **3D Galaxy Engine** | `tr4d3rz-observatory` | Three.js / WebGL | Motore di rendering 3D per visualizzare i cluster di agenti, le nicchie emergenti e i flussi di segnali (Signal Ecology). |
| **WASM FSM Replay** | `tr4d3rz-core` | WebAssembly | Il runtime FSM di base compilato in WASM. Permette al browser di eseguire il replay temporale e il lineage replay senza gravare sui nodi evolutivi. |
| **MQTT WS Client** | `tr4d3rz-observatory` | TypeScript | Client MQTT via WebSocket (porta 8083) per ricevere in tempo reale lo stato dell'ecosistema dal NanoMQ broker. |

---

## 5. Gateway Nodes (Bridge UART/MQTT)

Nodi intermedi (spesso script in esecuzione su PC Linux o Raspberry Pi secondarie) che fanno da ponte per l'hardware embedded privo di rete.

| Software / Componente | Repository di Origine | Stack Tecnologico | Descrizione e Note |
|---|---|---|---|
| **Protocol Translator** | `tr4d3rz-messaging` | Python / Rust | Demone che ascolta su una porta seriale (UART/USB), riceve i pacchetti CBOR dai nodi STM32 e li inoltra al broker MQTT, facendo anche il percorso inverso. |

---

## 6. External Persistence & Logic (PHP Hosting Gratuiti)

Servizi esterni di hosting PHP/MySQL utilizzati come memoria distribuita secondaria e watchdog computazionale.

| Software / Componente | Repository di Origine | Stack Tecnologico | Descrizione e Note |
|---|---|---|---|
| **Ping-Pong Watchdog** | `tr4d3rz-persistence-web` | PHP | Script che si invocano a vicenda tramite HTTP GET/POST per mantenere attiva la computazione distribuita nonostante i limiti di timeout dei servizi gratuiti. |
| **Distributed Registry** | `tr4d3rz-persistence-web` | PHP / MySQL | Registro remoto dei genomi più promettenti (Archetypes) e degli endpoint dei nodi attivi. |
| **Relay Service** | `tr4d3rz-persistence-web` | PHP | Funge da punto di rendezvous per nodi dietro NAT o con connettività intermittente. |

