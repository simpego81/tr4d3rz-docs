# TR4D3RZ: Distributed Evolutionary Signal Ecology
## Proposta per Marketing Tecnico

### 1. Vision: L'Algoritmo che "Respira"
TR4D3RZ non è un software statico, ma un'**ecologia biologica artificiale**. È un sistema distribuito (da microcontrollori ESP32 a server Linux) dove la logica di trading non viene scritta a mano, ma **evolve** per sopravvivere ai dati finanziari in tempo reale.

---

### 2. Roadmap Evolutiva: Da Zero al Segnale

#### Fase 1: Il Brodo Primordiale (Infrastruttura)
*   **Azione:** Distribuiamo milioni di "semi" (Genomi basati su **L-Systems**) su una rete MQTT.
*   **Nodi Coinvolti:**
    *   **tr4d3rz-core (Rust):** Genera i genomi iniziali e definisce le regole grammaticali.
    *   **tr4d3rz-messaging (Python):** Funge da sistema nervoso, trasportando i genomi via MQTT/NATS verso i nodi di calcolo.
    *   **tr4d3rz-embedded (C/C++):** Riceve i semi su dispositivi come ESP32/STM32 e "compila" il genoma in una FSM leggera pronta all'uso.
*   **Esempio:** Un nodo su un ESP8266 riceve un genoma `[A->B, B->C]`. Lo trasforma in un automa che osserva i prezzi di *Eni*.

#### Fase 2: Selezione Naturale (Fitness)
*   **Azione:** I nodi confrontano le predizioni delle FSM con i dati reali della Borsa Italiana.
*   **Nodi Coinvolti:**
    *   **tr4d3rz-embedded & tr4d3rz-core:** Eseguono la logica della FSM in locale sui dati in streaming. Calcolano in tempo reale il punteggio di fitness.
    *   **tr4d3rz-persistence (Python):** Archivia lo storico delle performance degli agenti per garantire che i dati di fitness siano consistenti anche dopo un riavvio.
*   **Esempio:** Un'agente predice "BUY" su *Stellantis*. Il prezzo scende. L'agente perde energia e rischia l'estinzione (cancellazione dal nodo).

#### Fase 3: Mutazione e Adattamento (Evoluzione)
*   **Azione:** Gli agenti più "ricchi" (alta fitness) si riproducono.
*   **Nodi Coinvolti:**
    *   **tr4d3rz-evolution (Rust):** Il motore evolutivo principale. Raccoglie i genomi migliori dai nodi distribuiti, applica mutazioni e crossover, e genera una nuova "prole".
    *   **tr4d3rz-messaging:** Ridistribuisce la nuova generazione di agenti potenziati attraverso l'ecologia.
*   **Esempio:** Due FSM che performano bene in mercati laterali si fondono. Il figlio risultante potrebbe scoprire una nuova regola che funziona anche in trend rialzista.

#### Fase 4: Emergenza Ecologica (Biomi)
*   **Azione:** Il sistema non cerca "l'algoritmo perfetto", ma una popolazione diversificata. Le nicchie di mercato **emergono** dall'interazione tra agenti e dati finanziari.
*   **Ciclo di Emergenza (Agent-Driven):**
    1.  **Accumulo di Segnali:** Il sistema monitora `tr4d3rz/ecosystem/fitness/{agent_id}` raccogliendo coppie `(Agent_ID, Symbol, Fitness, Timestamp)`.
    2.  **Rilevamento Densità:** Un **Ambiente Locale (Bioma)** emerge quando:
        *   **Consenso:** Almeno N agenti della stessa stirpe (lineage) hanno fitness elevata sugli stessi titoli.
        *   **Stabilità:** Il successo persiste per un numero minimo di campioni temporali.
        *   **Specificità:** La stirpe performa significativamente meglio su quel set di titoli rispetto al resto del mercato.
    3.  **Dichiarazione del Bioma:** L'Emergence Engine pubblica su `tr4d3rz/ecosystem/environment/{env_id}/definition` (CBOR, QoS 2):
        ```json
        {
          "env_id": "bio-energy-stable-2026",
          "symbols": ["ENI.MI", "ENEL.MI", "ERG.MI"],
          "agent_family": "lin-78f2-a1",
          "regime_signature": "low-vol-bull",
          "confidence": 0.85
        }
        ```
*   **Nodi Coinvolti:**
    *   **tr4d3rz-evolution (Niche Discovery):** Component `evo_niche` analizza i dati di fitness, rileva pattern di successo, dichiara ambienti emergenti.
    *   **tr4d3rz-observatory (TS/Three.js):** Visualizza i biomi come galassie colorate. Gli agenti migrano visivamente verso il centro del bioma.
    *   **tr4d3rz-persistence:** Salva gli "archetipi" (pattern archetipali FSM) che definiscono la firma di successo.
*   **Esempio:** Gli agenti "scoprono" autonomamente che i titoli energetici italiani reagiscono in modo correlato a certi regimi di volatilità, creando il bioma `bio-energy-stable-2026` senza intervento umano.

---

### 3. L'Ecologia Intelligente: Il Mercato si Rivela attraverso il Successo
A differenza dei sistemi tradizionali, TR4D3RZ non impone cluster di mercato (es. "Settore Energetico").

#### 3.1 Emergenza Spontanea
Il mercato viene segmentato **solo quando gli agenti dimostrano di saperlo prevedere**. Un Bioma rappresenta l'accoppiamento stabile tra:
*   **Genetica:** Una famiglia di agenti (lineage) con FSM strutturalmente simili.
*   **Mercato:** Un cluster di titoli dove quella famiglia ha dimostrato successo predittivo superiore.

#### 3.2 Meccanismi di Local Bias (Specializzazione Accelerata)
Una volta dichiarato un Bioma, il sistema applica una "pressione locale" per accelerare la specializzazione:

**A. Bias Evolutivo:**
*   **Topology Bias:** L'L-System Generator (`lsystem`) riceve segnali di bias topologico, favorendo moduli strutturali presenti negli agenti di successo del Bioma.
*   **Mutation Focus:** Le mutazioni per la `agent_family` coinvolta vengono testate **prioritariamente** sui `symbols` dell'ambiente.

**B. Bias di Runtime:**
*   **Context Awareness:** Il Phenotype Runtime riceve segnali di "Local Bias" che attivano nodi FSM specifici per quel contesto di mercato.
*   **Resource Allocation:** I nodi embedded prioritizzano l'elaborazione dei dati (OHLCV) appartenenti all'ambiente locale attivo.

#### 3.3 Dinamica delle Nicchie (Ciclo Vitale)
Gli Ambienti Locali non sono eterni e seguono un ciclo biologico:
1.  **Nascita (Emergence):** Identificazione iniziale del pattern di successo.
2.  **Espansione (Drift):** Inclusione di nuovi titoli correlati o stirpi affini.
3.  **Stabilità (Climax):** Alta fitness costante e bassa varianza genetica.
4.  **Collasso (Extinction):** Declino della fitness dovuto a cambi strutturali del mercato (es. cambio regime da Bull a Bear).

#### 3.4 Resilienza e Memoria
Se una nicchia collassa, gli agenti specializzati muoiono, ma il "codice genetico" di successo viene conservato nell'**Archetype Memory** per future rinascite quando condizioni di mercato simili si ripresentano.

---

### 4. Output Finale: Segnali Predittivi "Validati dal Bioma"
Il risultato non è un singolo indicatore, ma un **consenso ecologico** stratificato per Bioma:
1.  **Segnale Specializzato:** 1.000 agenti appartenenti al Bioma `bio-energy-stable-2026` emettono contemporaneamente un segnale di "Acquisto" su `ENI.MI` via `tr4d3rz/ecosystem/signal/{agent_id}` (CBOR, QoS 0).
2.  **Affidabilità Multifattoriale:** Il sistema calcola la **Confidence Score** basata su:
    *   **Lineage:** Età e stabilità genetica della famiglia di agenti.
    *   **Niche Strength:** Quanto forte è il Bioma (consensus + stability + specificity).
    *   **Cooperation Value:** Quanti agenti indipendenti del Bioma concordano sul segnale.
3.  **Esecuzione:** Il segnale aggregato viene inviato:
    *   **Observatory:** Visualizzazione delle galassie di Biomi attivi.
    *   **Replay System:** Validazione storica confrontando segnali passati con dati reali.
    *   **Prediction Service:** Output finale per decisioni di investimento.

---

### Perché TR4D3RZ è Unico?
- **Emergenza Ecologica:** Le nicchie di mercato non sono predefinite da esperti umani, ma **emergono spontaneamente** dall'interazione tra agenti e dati finanziari. Il sistema scopre segmentazioni di mercato che gli analisti tradizionali potrebbero non vedere.
- **Resilienza Distribuita:** Se un server cade, l'evoluzione continua sui piccoli nodi embedded.
- **Auto-Riparazione:** Se il mercato cambia natura, la vecchia popolazione muore e una nuova, adattata alle nuove condizioni, evolve in ore. Gli archetipi di successo rimangono in memoria per rinascite future.
- **Zero Bias Umano:** Le strategie non sono influenzate da pregiudizi, ma solo dalla sopravvivenza economica verificata empiricamente su dati reali.
