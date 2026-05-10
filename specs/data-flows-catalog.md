# TR4D3RZ — Catalogo dei Flussi Dati Inter-Nodo

**Stato**: Draft
**Autore**: Manus (Chief Architect)

Questo documento definisce e descrive tutti i flussi di dati (payload) scambiati tra i nodi dell'ecosistema TR4D3RZ. Tutto il traffico passa attraverso il Core Infrastructure Node (NanoMQ Broker).

---

## 1. Flusso Dati di Mercato (OHLCV Feed)

Il flusso vitale che alimenta l'intero ecosistema. I dati sono estratti dal sito di Borsa Italiana e trasmessi a tutti i nodi evolutivi e agli osservatori.

| Proprietà | Dettaglio |
|---|---|
| **Sorgente** | Core Node (`borsa-italiana-scraper`) |
| **Destinazione** | Evolution Nodes, Observatory Nodes |
| **Topic MQTT** | `data/ohlcv/history/{isin}` e `data/ohlcv/intraday/{isin}` |
| **Formato** | JSON |
| **QoS** | 0 (Fire and forget) |

**Descrizione**: 
Il payload contiene un array di candele con chiavi minificate (`o`, `h`, `l`, `c`, `v`, `t`) e timestamp Unix (`ts`). L'alta frequenza dei dati intraday impone il QoS 0 per evitare sovraccarichi sul broker.

---

## 2. Flusso di Segnalazione Cooperativa (Cooperative Signaling)

La comunicazione orizzontale tra agenti. Gli agenti non si conoscono direttamente, ma emettono segnali su un bus comune a cui altri agenti possono iscriversi (subscription).

| Proprietà | Dettaglio |
|---|---|
| **Sorgente** | Evolution Nodes, Optimization Nodes |
| **Destinazione** | Altri Evolution Nodes, Observatory Nodes |
| **Topic MQTT** | `ecosystem/signal/{agent_id}` |
| **Formato** | CBOR |
| **QoS** | 0 |

**Descrizione**: 
Quando la FSM di un agente valuta una specifica condizione come vera (es. un pattern rilevato), emette un segnale. Il payload contiene l'ID dell'agente, il tipo di segnale e una forza/confidenza (0.0 - 1.0).

---

## 3. Flusso di Valutazione Fitness e Nicchie

I risultati del lavoro computazionale dei nodi evolutivi. Questi dati guidano la selezione naturale e vengono visualizzati nell'Observatory.

| Proprietà | Dettaglio |
|---|---|
| **Sorgente** | Evolution Nodes |
| **Destinazione** | Persistence Node (Event Logger), Observatory Nodes |
| **Topic MQTT** | `ecosystem/fitness/{agent_id}` e `ecosystem/niche/{niche_id}` |
| **Formato** | CBOR |
| **QoS** | 1 (At least once) |

**Descrizione**: 
Ogni fine giornata di trading (o fine backtest), i nodi evolutivi calcolano la fitness secondo la formula multi-dimensionale. Il payload include: predictive power, niche strength, cooperation value, statistical confidence, e computational cost.

---

## 4. Flusso di Eventi Evolutivi (Lineage & Mutation)

La storia genetica dell'ecosistema. Cruciale per il replay evolutivo e la comprensione di come si formano le strutture predittive.

| Proprietà | Dettaglio |
|---|---|
| **Sorgente** | Evolution Nodes |
| **Destinazione** | Persistence Node (SQLite Event Log) |
| **Topic MQTT** | `evolution/mutation/{node_id}`, `evolution/birth/{agent_id}`, `evolution/death/{agent_id}` |
| **Formato** | CBOR |
| **QoS** | 1 (At least once) |

**Descrizione**: 
Ogni volta che un genoma viene modificato dall'L-System o tramite crossover, viene emesso un evento di mutazione. Il payload contiene l'ID del genitore, l'ID del figlio, e il delta delle modifiche strutturali (aggiunta nodo, modifica peso, ecc.).

---

## 5. Flusso di Archetipi (Archetype Memory)

Il consolidamento della conoscenza a lungo termine. Quando un pattern FSM si dimostra costantemente utile in una nicchia, viene "promosso" ad archetipo.

| Proprietà | Dettaglio |
|---|---|
| **Sorgente** | Persistence Node / Evolution Nodes (Clustering) |
| **Destinazione** | Tutti i nodi |
| **Topic MQTT** | `lineage/archetype/{archetype_id}` |
| **Formato** | CBOR |
| **QoS** | 2 (Exactly once) |

**Descrizione**: 
Payload pesante che contiene l'intera struttura di una sottomacchina a stati (FSM motif) altamente ottimizzata. Gli archetipi vengono riutilizzati come blocchi base per le generazioni future. Richiede QoS 2 data l'importanza critica dell'informazione.

---

## 6. Flusso Capsule Embedded (Offline Sync)

Il meccanismo di scambio dati per i nodi hardware senza connettività di rete (es. STM32 connessi via USB/UART).

| Proprietà | Dettaglio |
|---|---|
| **Sorgente/Destinazione** | Optimization Nodes (STM32) ↔ Gateway Nodes |
| **Trasporto** | UART Seriale / File System (USB) |
| **Formato** | CBOR (Binary Dump) |

**Descrizione**: 
Il Gateway Node pacchetta i dati OHLCV recenti e i migliori genomi in un file binario (Capsule) e lo trasmette via seriale al nodo STM32. Il nodo STM32 esegue l'ottimizzazione locale e restituisce una Capsule contenente i genomi migliorati e i risultati di fitness. Il Gateway si occupa di tradurre questi file in messaggi MQTT.
