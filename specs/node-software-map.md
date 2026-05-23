# TR4D3RZ — Mappa del Software per Nodo

**Stato**: Draft
**Autore**: Manus (Chief Architect)

Questo documento definisce l'inventario del software in esecuzione su ciascuna classe di nodo dell'ecosistema TR4D3RZ.

---

## 1. Central Infrastructure & Persistence Node (Raspberry Pi 2)

Il nodo centrale Raspberry Pi 2 gestisce raccolta dati, broker MQTT, logging append-only, persistenza locale e relay/gateway. Il profilo ARMv7 quad-core a 900MHz con 1GB RAM consente di consolidare servizi che prima erano separati, mantenendo NanoMQ prioritario rispetto ai picchi di scraper e logger.

| Software / Componente | Repository di Origine | Stack Tecnologico | Descrizione e Note |
|---|---|---|---|
| **NanoMQ** | (Emqx/NanoMQ) | C | Broker MQTT ultra-leggero per il nodo centrale ARMv7/RPi2. Espone la porta TCP 1883 e WebSocket 8083 verso ESP8266, STM32 tramite bridge, Linux PC e Observatory. |
| **Data Scraper** | `borsa-italiana-scraper` | Node.js 14.15.1 | Script di ingestion che interroga le API di Borsa Italiana. È eseguito sulla RPi2 con concorrenza controllata, converte i dati in formato JSON standardizzato e li pubblica su MQTT. |
| **Event Logger** (Futuro) | `tr4d3rz-persistence` | Rust | Demone che si iscrive a tutti gli eventi MQTT e li salva in append-only su un database SQLite locale in WAL mode. |
| **Persistence Service** (Futuro) | `tr4d3rz-persistence` | Rust | Servizio locale per lineage, archetype memory e export Parquet. |
| **Local Gateway / Relay** | `tr4d3rz-messaging` | Rust / Python | Endpoint locale verso il broker RPi2 per bridge UART/USB, nodi offline e delayed synchronization. |

---

## 2. Evolution Nodes (PC Linux / Android Potenti)

I nodi evolutivi sono i "muscoli" del sistema. Eseguono il grosso del carico computazionale, generando genomi e valutando le fitness.

| Software / Componente | Repository di Origine | Stack Tecnologico | Descrizione e Note |
|---|---|---|---|
| **L-System Engine** | `tr4d3rz-core` | Rust | Generatore di genomi ibridi (grafo) a partire da grammatiche L-System. |
| **FSM Runtime** | `tr4d3rz-core` | Rust | Motore di esecuzione ad alte prestazioni che compila il genoma grafo in una Macchina a Stati Finiti ed elabora il flusso dati OHLCV in tempo reale. |
| **Evolution Engine** | `tr4d3rz-evolution` | Rust | Gestisce le popolazioni di agenti, applica operatori di mutazione strutturale e calcola la fitness multi-dimensionale. |
| **MQTT Client** | `tr4d3rz-messaging` | Rust | Sottosistema di comunicazione per ricevere i dati OHLCV dal nodo centrale RPi2 e pubblicare i risultati di fitness e i segnali cooperativi. |

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

Nodi intermedi opzionali, spesso script in esecuzione su PC Linux o bridge dedicati, che fanno da ponte fisico per l'hardware embedded privo di rete. Il loro endpoint logico resta sempre l'IP unico del nodo centrale RPi2.

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

