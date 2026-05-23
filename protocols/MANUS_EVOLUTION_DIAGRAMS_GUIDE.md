# Guida alla Creazione Diagrammi Evolutivi (Manus)

Questa guida contiene le specifiche tecniche per la creazione dei diagrammi PlantUML relativi ai meccanismi evolutivi del sistema TR4D3RZ.

## 1. Requisiti Globali
- **Stile**: `skinparam monochrome true`
- **Layout**: `direction lr` (dove applicabile)
- **Metadata**: Ogni diagramma deve includere una nota a fondo pagina (`footer`) con i topic MQTT coinvolti e la struttura del payload CBOR.
- **Precisione**: Definire esplicitamente attori, componenti e canali di comunicazione.
- **Hosting Visibility (OBBLIGATORIO)**: Deve essere evidente per ciascuna entità il dispositivo tecnologico che la ospita.
    - **Sequence Diagrams**: Usare `box "Device Name" #Color ... end box`.
    - **Altri Diagrammi**: Usare stereotipi (es: `<<Linux Server>>`) o raggruppamenti espliciti.

---

## 2. Mapping dei Dispositivi (Standard)
Per garantire la coerenza con l'architettura ArchiMate, attenersi al seguente mapping:
- **Cloud/Hub (Linux Server)**: Mutation Engine, L-System Generator, Persistence, Graph Expansion, Fitness Evaluator.
- **Edge Node (Linux Gateway)**: MQTT Broker, Protocol Gateway.
- **Distributed Nodes (RPi / ESP32 / STM32)**: Core Runtime, Agent FSM, Pheromone Signaling.
- **Observatory (Browser/Mobile)**: Visualization UI, Replay System.

---

## 3. Specifiche dei Diagrammi

### 2.1. Genesi: Trascrizione Genomica (`evolution_genesis.puml`)
**Tipo**: Sequence Diagram
**Flusso**:
1. `Mutation Engine` innesca il `L-System Generator`.
2. Il generatore espande la stringa (es: `G[+F]-X`).
3. `Graph Expansion` converte la stringa in un grafo normalizzato.
4. `FSM Generator` compila il grafo in una tabella di stati finiti.
5. Invio del messaggio su MQTT.
**Dati**:
- **Topic**: `ecology/birth`
- **Payload (CBOR)**: `agent_id`, `genome_string`, `fsm_table`, `generation`, `parent_id`.

### 2.2. Ciclo di Valutazione Fitness (`evolution_fitness.puml`)
**Tipo**: Communication/Flow Diagram
**Flusso**:
1. `Persistence` pubblica dati `OHLCV` su `market/it/mib/ohlcv`.
2. Il `Core Runtime` riceve i dati e li processa tramite la FSM dell'agente.
3. L'agente genera una `Prediction`.
4. `Fitness Evaluator` confronta la predizione con il tick successivo.
5. Invio aggiornamento fitness su MQTT.
**Dati**:
- **Topic**: `ecology/fitness/update`
- **Payload (CBOR)**: `agent_id`, `fitness_score`, `symbols_count`, `timestamp`.

### 2.3. Mutazione e Adattamento (`evolution_mutation.puml`)
**Tipo**: State Machine Diagram
**Stati**:
- `Active`: L'agente processa dati.
- `Under Mutation`: Innescato da bassa fitness o comando esterno.
- `Validation`: Test in sandbox locale.
- `Re-Deployed`: Trasferimento su nodo (es: STM32) rispettando vincoli di memoria/clock.
**Vincoli**: `Hardware_Constraint` (KB RAM, Clock MHz).

### 2.4. Tracciamento Discendenza (`evolution_lineage.puml`)
**Tipo**: Class Diagram (Schema CBOR)
**Attributi**:
- `UUID`: Identificativo unico agente.
- `Parent_UUID`: Riferimento al genitore (per ricostruzione DAG).
- `Generation_Index`: Livello nell'albero evolutivo.
- `Archetype_Flag`: Booleano per indicare pietre miliare.
**Persistenza**: Definizione del formato per il nodo di persistenza (Rust).

### 2.5. Simbiosi e Signaling (`evolution_symbiosis.puml`)
**Tipo**: Multi-Agent Sequence Diagram
**Scenario**:
1. `Agente A` (Specialista) rileva un pattern e invia un `Pheromone_Signal`.
2. Il segnale viene pubblicato su un topic di nicchia (es: `signals/niche/high-volatility`).
3. `Agente B` (Sottoscritto al topic) integra il segnale come input extra nella sua FSM.
4. Entrambi beneficiano del miglioramento del fitness collettivo.
**Dati**:
- **Topic**: `signals/niche/+`
- **Payload (CBOR)**: `strength` (0.0-1.0), `regime_type`.

---

## 3. Workflow di Aggiornamento
1. Creare/Modificare i file `.puml` in `diagrams/evolution/`.
2. Verificare la coerenza con i topic definiti in `protocols/mqtt-topic-structure.md`.
3. Aggiornare i link in `specs/evolution/niche-evolution-spec.md`.
