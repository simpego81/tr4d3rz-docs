# MVP Development Plans: Walking Skeleton Options

Questo documento delinea tre opzioni strategiche per lo sviluppo di un **Walking Skeleton** del sistema TR4D3RZ. Lo scopo è validare l'architettura distribuita utilizzando 4 dispositivi fisici diversi prima di procedere alla Milestone 1 completa.

---

## Opzione 1: "The Foundational Backbone"
**Focus:** Infrastruttura di comunicazione e ciclo di vita del genoma.
**Obiettivo:** Testare la stabilità del broker e la serializzazione dei dati tra nodi eterogenei.

### 1. I 4 Device
*   **Linux PC (Evolution Node):** Generazione genomi (L-System) e gestione popolazione.
*   **Raspberry Pi 2 (Persistence & Broker):** Hosting MQTT Broker (Mosquitto) e SQLite (Lineage).
*   **ESP8266 (Optimization Node):** Esecuzione FSM semplificate e tuning parametri.
*   **Web Browser (Observatory):** Monitoraggio messaggi MQTT e stato popolazione (WASM/JS).

### 2. Walking Skeleton Flow
1.  **Linux PC** genera un nuovo genoma e lo pubblica via MQTT.
2.  **Raspberry Pi 2** intercetta il messaggio e lo salva nel database di persistenza.
3.  **ESP8266** scarica la FSM serializzata, la esegue su un set di test e restituisce il valore di fitness.
4.  **Web Browser** visualizza graficamente l'intero ciclo in tempo reale.

### 3. Valutazione Architetturale
*   Latenza e affidabilità del broker su hardware limitato (RPi 2).
*   Efficienza della serializzazione CBOR per microcontrollori a 8/32 bit.
*   Robustezza del flusso asincrono in caso di disconnessione dei nodi.

---

## Opzione 2: "The Embedded Edge"
**Focus:** Portabilità del runtime e interazione mobile.
**Obiettivo:** Validare l'esecuzione delle FSM su hardware "bare-metal" e il controllo remoto.

### 1. I 4 Device
*   **Linux PC (Genotype Station):** Archivio centrale e data provider storico.
*   **STM32F3 Discovery (Optimization Node):** Runtime FSM reale per calcolo fitness ad alta precisione.
*   **Android Tablet (Mobile Observatory):** Interfaccia utente per iniezione mutazioni e monitoraggio.
*   **ESP8266 (Gateway/Sensor):** Simulatore di ticker feed (generazione segnali di mercato).

### 2. Walking Skeleton Flow
1.  **Android Tablet** invia un comando di "Mutation Pulse".
2.  **Linux PC** genera la mutazione e la distribuisce.
3.  **ESP8266** invia stream di segnali (Open/Close simulati).
4.  **STM32F3** esegue la FSM sui segnali in tempo reale e riporta i trade generati al Tablet.

### 3. Valutazione Architetturale
*   Performance del runtime FSM scritto in Rust/C su Cortex-M.
*   Gestione dei trigger real-time provenienti da sensori/gateway esterni.
*   Usabilità dell'interfaccia di controllo mobile in un contesto distribuito.

---

## Opzione 3: "The High-Performance Ecology"
**Focus:** Specializzazione, nicchie e visualizzazione avanzata.
**Obiettivo:** Testare la capacità del sistema di gestire evoluzioni rapide e lineage complessi.

### 1. I 4 Device
*   **MIMXRT1050-EVK (High-Speed Evolution):** Evoluzione accelerata di popolazioni locali (Niche Discovery).
*   **Linux PC (Data Provider):** Streaming di dataset massivi (Parquet/CSV) verso i nodi.
*   **Raspberry Pi 2 (Archetype Memory):** Memorizzazione e recupero degli archetipi evolutivi vincenti.
*   **Web Browser (Galaxy View):** Visualizzazione 3D (Three.js) della topologia delle nicchie.

### 2. Walking Skeleton Flow
1.  **Linux PC** avvia uno stream di dati storici ad alta velocità.
2.  **MIMXRT1050** evolve specie specializzate su quei dati e identifica una "Nicchia".
3.  **Raspberry Pi 2** indicizza l'archetipo della nicchia scoperta.
4.  **Web Browser** renderizza la "Galassia" mostrando la posizione della nuova nicchia nel sistema.

### 3. Valutazione Architetturale
*   Scalabilità degli algoritmi di clustering e scoperta delle nicchie.
*   Efficienza del sistema di "Archetype Memory" per il riuso del codice genetico.
*   Capacità del sistema di visualizzazione di gestire grandi volumi di dati evolutivi (Galaxy View).

---

## Raccomandazione di Manus (Technical Director)

Per il primo walking skeleton, la raccomandazione è di procedere con l'**Opzione 1**.

**Motivazione:** È l'opzione che affronta i rischi tecnici più immediati (connettività e persistenza) con l'hardware più accessibile. Una volta stabilizzato il "Backbone", l'integrazione di nodi più potenti (MIMXRT) o interfacce più ricche (Tablet) avverrà su fondamenta già verificate.
