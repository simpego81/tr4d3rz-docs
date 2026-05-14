# Analisi Comparativa: `archimate_diagram.puml` vs `tr4d3rz_master_spec.md`

**Data**: 2026-05-12
**Autore**: Manus (Chief Architect)

Questo documento analizza le discrepanze tra il diagramma PlantUML ArchiMate fornito dall'utente (`/mnt/desktop/tr4/archimate_diagram.puml`) e la Specifica Master del progetto (`tr4d3rz_master_spec.md`), e delinea le modifiche necessarie per allineare il diagramma alla visione architetturale aggiornata.

## 1. Elementi Allineati (Da Mantenere)

- **Struttura a Layer**: La divisione in Motivation, Business, Application, Data e Technology layer è corretta e ben strutturata.
- **Hardware Target**: L'elenco dei device nel Technology Layer (Linux PC, Android, STM32F*, ESP8266, Raspberry Pi 2, Browser) riflette esattamente la sezione "Hardware Target" della specifica master.
- **Componenti Core**: I moduli `L-System Generator`, `Graph Expansion`, `FSM Generator` e `Phenotype Runtime` mappano perfettamente la "Pipeline del Genoma" definita nella specifica.
- **Componenti Fitness**: `Fitness Calculator`, `Niche Evaluator` e `Cooperation Scorer` sono coerenti con la formula di fitness (predictive_power + niche_strength + cooperation_value).
- **Data Objects**: Gli oggetti `OHLCV Data`, `Hybrid Graph Genome`, `FSM Definition`, `Trading Signal`, `System Event` e `Archetype` sono accurati.

## 2. Discrepanze e Gap (Da Aggiornare/Aggiungere)

### A. Livello Motivation & Business
- **Gap**: Manca il concetto di "Cooperative Signaling" e "Open-Ended Evolution" come driver/obiettivi primari.
- **Azione**: Aggiungere `Motivation_Principle` per "Open-Ended Evolution", "Asynchronous Distributed Ecology" e "Cooperative Signaling".

### B. Livello Application - Nodi e Componenti
- **Discrepanza**: Il nodo "Core Infrastructure Node" (Raspberry Pi 1) con il ruolo di MQTT Broker e Data Ingestion (borsa-italiana-scraper) è completamente assente. Il PUML attuale delega la persistenza a un generico "Persistence Nodes".
- **Azione**: Aggiungere il `Core Infrastructure Node` nell'Application Layer con i componenti `Data Ingestion` e `MQTT Broker`.
- **Gap**: Mancano i componenti visivi descritti nella specifica master sotto "Visualizzazioni Richieste" (Deploy Architecture Map, Theory Map, Evolution Galaxy, Signal Ecology, Market Overlay).
- **Azione**: Espandere l'`Observatory Node` per includere esplicitamente questi componenti di visualizzazione.

### C. Livello Tecnologia - Software e Infrastruttura
- **Discrepanza**: La specifica menziona esplicitamente "CBOR" o "FlatBuffers" per la serializzazione embedded, e "Three.js" o "WebGL" per la visualizzazione. Questi dettagli mancano.
- **Azione**: Aggiungere `Technology_Artifact` per "CBOR Serialization" e "Three.js / WebGL Engine".
- **Discrepanza**: Il nodo MQTT è generico. Abbiamo deciso tramite ADR-0003 di usare "NanoMQ".
- **Azione**: Aggiornare `Technology_Node` a "NanoMQ Broker".
- **Discrepanza**: Il database locale è segnato come SQLite, ma manca il riferimento a Parquet per i dataset grandi. (In realtà Parquet c'è, ma manca il collegamento esplicito).

### D. Relazioni e Flussi
- **Gap**: Le relazioni di flusso dati tra i nodi (es. OHLCV dal Core Node agli Evolution Nodes, Segnali cooperativi) non sono esplicitate in modo chiaro tra i nodi fisici/applicativi.
- **Azione**: Aggiungere relazioni `Rel_Flow` esplicite per i flussi di dati principali identificati nel `data-flows-catalog.md`.

## 3. Conclusione

Il file `archimate_diagram.puml` esistente è un'ottima base di partenza che cattura fedelmente la filosofia iniziale della specifica master. Tuttavia, non riflette le decisioni architetturali prese durante la Milestone 0 (es. il ruolo centrale del Core Node / Raspberry Pi 1 con NanoMQ e lo scraper) e omette alcuni dettagli specifici richiesti per la UI dell'Observatory. 

Procederò a generare un nuovo file `archimate_diagram_v2.puml` che integra tutte queste correzioni.
