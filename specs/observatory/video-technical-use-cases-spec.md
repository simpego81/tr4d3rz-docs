# Specifica Tecnica: Video Use Case TR4D3RZ
**ID Spec**: SPEC-OBS-VIDEO-001  
**Stato**: Draft  
**Owner**: Manus (Video Production)  
**Destinatario**: Technical audience (developers, architects, quant traders)  
**Durata Target**: 4-5 minuti  
**Data Richiesta**: 2026-05-17

---

## 1. Obiettivi del Video

**Obiettivo Primario**: Dimostrare visivamente come TR4D3RZ implementa un'ecologia evolutiva distribuita per generare segnali di trading attraverso emergenza spontanea di nicchie di mercato.

**Obiettivi Secondari**:
1. Mostrare la distribuzione eterogenea del carico computazionale (ESP8266 → Linux server)
2. Visualizzare il ciclo completo: Genome → FSM → Fitness → Mutation → Biome Emergence
3. Dimostrare il flusso MQTT tra i nodi
4. Mostrare l'emergenza di un Bioma reale con dati simulati

**NON-Obiettivi** (da NON includere):
- Marketing generico senza dettagli tecnici
- Animazioni astratte senza riferimento al codice/architettura reale
- UI/UX polishing dell'Observatory (mostrare la versione attuale anche se grezza)

---

## 2. Struttura Narrativa (Scene-by-Scene)

### SCENA 1: Titolo e Contesto (0:00 - 0:20)
**Durata**: 20 secondi

**Visualizzazione**:
- Titolo: "TR4D3RZ: Distributed Evolutionary Signal Ecology"
- Subtitle: "From Genome to Biome: A Technical Walkthrough"
- Mostrare mappa della rete con i 14 device types come nodi geograficamente distribuiti
- Overlay: "Heterogeneous Computing: ESP8266 (80MHz) → Linux (x86_64)"

**Device Mostrati**:
- Tutti i 14 device in una vista d'insieme (usa `docs/index.html` grid come riferimento)

**Audio/Narrazione** (testo esatto da sintetizzare):
> "TR4D3RZ is a distributed evolutionary ecology running on heterogeneous hardware. From 80MHz microcontrollers to x86 servers, each node participates in evolving trading strategies through natural selection on real financial data."

---

### SCENA 2: Fase 1 - Genome Generation (0:20 - 1:00)
**Durata**: 40 secondi

**Visualizzazione**:
- Split screen 3 pannelli:
  - **Pannello Sinistra**: Device Linux PC con codice Rust `tr4d3rz-core/lsystem`
  - **Pannello Centro**: Visualizzazione grafica di un L-System che genera un albero/grafo
  - **Pannello Destra**: MQTT topic `tr4d3rz/genome/new/{genome_id}` con payload CBOR (mostrare hex dump)

**Sequence**:
1. (0:20-0:30) Mostrare codice L-System che genera un genoma:
   ```rust
   // Esempio di produzione L-System (NON SIMULARE, usare questo snippet)
   Axiom: A
   Rules: A -> B[+A][-A]
   Iterations: 3
   ```
2. (0:30-0:40) Animare l'espansione del grafo L-System step-by-step (3 iterazioni)
3. (0:40-0:50) Mostrare serializzazione CBOR e pubblicazione MQTT
4. (0:50-1:00) Mostrare il genoma che viaggia attraverso la rete verso ESP8266 e STM32F3

**Device Mostrati**:
- **Linux PC** (generatore genoma)
- **MQTT Broker** (nodo centrale)
- **ESP8266, STM32F3** (riceventi)

**MQTT Topics da Mostrare** (in overlay):
```
PUBLISH tr4d3rz/node/linux-evo-01/capsule/out
  Payload: <CBOR binary genome> (mostrare primi 64 bytes in hex)
  QoS: 1
```

**Audio/Narrazione**:
> "Phase one: genome generation. The L-System generator on a Linux node produces a hybrid graph genome. This genome is serialized to CBOR and published via MQTT to distributed computation nodes, including low-power ESP8266 devices."

---

### SCENA 3: Fase 2 - FSM Compilation & Phenotype Runtime (1:00 - 1:50)
**Durata**: 50 secondi

**Visualizzazione**:
- Split screen 2 pannelli:
  - **Pannello Sinistra**: ESP8266 device (mostrare board fisica o render 3D)
  - **Pannello Destra**: Visualizzazione FSM (state machine diagram con stati e transizioni)

**Sequence**:
1. (1:00-1:10) ESP8266 riceve il genoma via MQTT
2. (1:10-1:30) Mostrare la trasformazione: Genome → Graph Expansion → FSM Generator
   - Visualizzare il grafo che viene "compilato" in una tabella di stati
   - Mostrare output: `State Table: [S0, S1, S2] | Transitions: [(S0->S1, cond_ohlcv_high), ...]`
3. (1:30-1:50) Mostrare FSM in esecuzione:
   - Input: OHLCV stream (mostrare candlestick chart di ENI.MI che scorre)
   - Condition evaluation: `cond_ohlcv_high == TRUE` (highlight del nodo FSM che si attiva)
   - Output: Signal emesso su MQTT `tr4d3rz/ecosystem/signal/agent-esp-001`

**Device Mostrati**:
- **ESP8266** (esecuzione FSM)
- **MQTT Broker** (ricezione segnali)

**MQTT Topics da Mostrare**:
```
SUBSCRIBE tr4d3rz/node/esp-001/capsule/in
SUBSCRIBE tr4d3rz/data/ohlcv/ENI.MI
PUBLISH tr4d3rz/ecosystem/signal/agent-esp-001
  Payload: {agent_id: "agent-esp-001", symbol: "ENI.MI", signal: "BUY", confidence: 0.67}
  QoS: 0
```

**Audio/Narrazione**:
> "Phase two: phenotype execution. The ESP8266 compiles the genome into a finite state machine. As OHLCV data streams in, the FSM evaluates conditions and emits cooperative signals when trading opportunities are detected."

---

### SCENA 4: Fase 3 - Fitness Evaluation (1:50 - 2:30)
**Durata**: 40 secondi

**Visualizzazione**:
- Split screen 3 pannelli:
  - **Pannello Sinistra**: Candlestick chart con segnali BUY/SELL sovrapposti
  - **Pannello Centro**: Fitness calculator (mostrare formula)
  - **Pannello Destra**: MQTT topic `tr4d3rz/ecosystem/fitness/{agent_id}` con payload

**Sequence**:
1. (1:50-2:00) Mostrare 3 agenti diversi che emettono segnali su ENI.MI
   - Agent A: BUY → Prezzo sale → Fitness +0.8
   - Agent B: SELL → Prezzo sale → Fitness -0.5
   - Agent C: HOLD → Fitness 0.0
2. (2:00-2:20) Mostrare calcolo fitness su Linux PC (tr4d3rz-evolution):
   ```
   Fitness = predictive_power(0.8) + niche_strength(0.3) 
             + cooperation_value(0.2) - computational_cost(0.1)
   Total: 1.2
   ```
3. (2:20-2:30) Pubblicazione fitness su MQTT

**Device Mostrati**:
- **ESP8266, Android, STM32F3** (agenti che emettono segnali)
- **Linux PC** (fitness calculator)
- **MQTT Broker**

**MQTT Topics da Mostrare**:
```
PUBLISH tr4d3rz/ecosystem/fitness/agent-esp-001
  Payload: {
    agent_id: "agent-esp-001",
    symbol: "ENI.MI",
    fitness: 1.2,
    lineage: "lin-78f2-a1",
    timestamp: 1747459200
  }
  QoS: 1
```

**Audio/Narrazione**:
> "Phase three: fitness evaluation. A Linux node compares agent predictions against actual price movements. Fitness is calculated using a multi-dimensional function: predictive power, niche strength, cooperation value, minus computational cost."

---

### SCENA 5: Fase 4 - Biome Emergence (2:30 - 3:40)
**Durata**: 70 secondi

**Visualizzazione**:
- **Vista principale**: Observatory holistic view (docs/holistic_view.html) che mostra:
  - Nodi agenti come particelle colorate
  - Simboli di mercato (ENI.MI, ENEL.MI, ERG.MI) come attrattori gravitazionali
  - Formazione graduale di un "cluster" (galassia colorata)

**Sequence**:
1. (2:30-2:50) Mostrare accumulo di fitness signals:
   - 100+ agenti della famiglia "lin-78f2-a1" pubblicano fitness > 0.7 su ENI.MI, ENEL.MI, ERG.MI
   - Visualizzare in real-time i punti che si accumulano nell'Observatory
   - Overlay: "Consensus Detection: 127 agents | Stability: 15 time windows | Specificity: 0.85"

2. (2:50-3:10) Rilevamento del Bioma:
   - Mostrare il componente `evo_niche` (Niche Discovery) su Linux PC che analizza i dati
   - Visualizzare algoritmo di clustering (usa un semplice K-means con K=1 per questo cluster)
   - Risultato: "Biome Detected: bio-energy-stable-2026"

3. (3:10-3:30) Dichiarazione del Bioma:
   - MQTT publish su `tr4d3rz/ecosystem/environment/bio-energy-stable-2026/definition`
   - Mostrare payload CBOR decodificato:
     ```json
     {
       "env_id": "bio-energy-stable-2026",
       "symbols": ["ENI.MI", "ENEL.MI", "ERG.MI"],
       "agent_family": "lin-78f2-a1",
       "regime_signature": "low-vol-bull",
       "confidence": 0.85
     }
     ```
   - Nell'Observatory: il cluster si illumina, appare una label "bio-energy-stable-2026"

4. (3:30-3:40) Local Bias in azione:
   - Split screen:
     - Sinistra: L-System Generator riceve "topology bias signal" → favorisce moduli simili agli agenti di successo
     - Destra: Phenotype Runtime riceve "context awareness signal" → attiva nodi FSM specifici per low-vol-bull regime

**Device Mostrati**:
- **Linux PC** (Niche Discovery component)
- **Observatory** (browser visualization)
- **MQTT Broker**
- **Linux PC** (L-System con bias)
- **ESP8266** (Phenotype con context awareness)

**MQTT Topics da Mostrare**:
```
PUBLISH tr4d3rz/ecosystem/environment/bio-energy-stable-2026/definition
  Payload: <JSON sopra in CBOR>
  QoS: 2

PUBLISH tr4d3rz/ecosystem/environment/bio-energy-stable-2026/bias
  Payload: {
    env_id: "bio-energy-stable-2026",
    agent_family: "lin-78f2-a1",
    bias_type: "topology",
    target_component: "lsystem"
  }
  QoS: 1

PUBLISH tr4d3rz/ecosystem/environment/bio-energy-stable-2026/bias
  Payload: {
    env_id: "bio-energy-stable-2026",
    regime: "low-vol-bull",
    bias_type: "context",
    target_component: "phenotype"
  }
  QoS: 1
```

**Audio/Narrazione**:
> "Phase four: biome emergence. The niche discovery component detects consensus: 127 agents from the same lineage consistently succeed on Italian energy stocks. The system declares a new local environment: bio-energy-stable-2026. This triggers local bias mechanisms. The L-System generator now favors topologies similar to successful agents. Phenotype runtimes activate regime-specific FSM nodes. The ecology self-organizes around discovered market structure."

---

### SCENA 6: Ciclo Vitale del Bioma (3:40 - 4:20)
**Durata**: 40 secondi

**Visualizzazione**:
- Timeline orizzontale che mostra il ciclo vitale del Bioma:
  - **Birth** (t=0): Primo rilevamento
  - **Expansion** (t=1-3 days): Nuovi simboli aggiunti (A2A.MI si unisce al cluster)
  - **Climax** (t=4-10 days): Fitness stabile, alta popolazione
  - **Collapse** (t=11 days): Cambio di regime → fitness crolla → Bioma muore

**Sequence**:
1. (3:40-3:50) Birth: Come mostrato in scena 5
2. (3:50-4:00) Expansion: 
   - Grafico fitness vs tempo: curva che sale
   - Observatory: nuovi agenti migrano verso il centro del Bioma
   - Nuovo simbolo A2A.MI si unisce (correlazione rilevata)
3. (4:00-4:10) Climax:
   - Fitness stabile a 0.9
   - Popolazione: 200 agenti specializzati
   - Overlay: "Genetic Variance: LOW (specialized)"
4. (4:10-4:20) Collapse:
   - Evento esterno: "Market Regime Change: Bull → Bear"
   - Fitness crolla da 0.9 a 0.2
   - Agenti muoiono (particles scompaiono dall'Observatory)
   - Archetype Memory: "Saving archetype bio-energy-stable-2026 to persistence layer"

**Device Mostrati**:
- **Observatory** (visualizzazione ciclo vitale)
- **Linux PC** (tr4d3rz-persistence)
- **MQTT Broker**

**MQTT Topics da Mostrare**:
```
PUBLISH tr4d3rz/ecosystem/environment/bio-energy-stable-2026/lifecycle
  Payload: {status: "COLLAPSE", reason: "regime-change", timestamp: 1747545600}
  QoS: 2

PUBLISH tr4d3rz/lineage/archetype/arch-bio-energy-stable-2026
  Payload: {
    archetype_id: "arch-bio-energy-stable-2026",
    env_id: "bio-energy-stable-2026",
    fsm_signature: "<binary CBOR>",
    agent_family: "lin-78f2-a1",
    symbols: ["ENI.MI", "ENEL.MI", "ERG.MI"],
    fitness_avg: 0.9,
    lifespan_days: 11
  }
  QoS: 2
```

**Audio/Narrazione**:
> "Biomes follow a lifecycle. After birth, bio-energy-stable expands as correlated symbols join. It reaches climax with 200 specialized agents and low genetic variance. When market regime shifts from bull to bear, fitness collapses. Agents die, but the successful FSM archetype is saved to persistence. When similar conditions return, the ecology can resurrect proven strategies."

---

### SCENA 7: Output Finale - Prediction Service (4:20 - 4:50)
**Durata**: 30 secondi

**Visualizzazione**:
- Dashboard finale che mostra:
  - **Pannello 1**: Segnali aggregati per Bioma
    ```
    Biome: bio-energy-stable-2026
    Signal: BUY ENI.MI
    Consensus: 187/200 agents (93.5%)
    Confidence Score: 0.89
      - Lineage: 0.92 (avg age: 45 generations)
      - Niche Strength: 0.85
      - Cooperation Value: 0.91
    ```
  - **Pannello 2**: Replay validation (grafico storico che mostra segnali passati vs prezzo reale)
  - **Pannello 3**: Observatory galaxy view con Biomi attivi evidenziati

**Sequence**:
1. (4:20-4:30) Aggregazione segnali: 187 agenti convergono su BUY ENI.MI
2. (4:30-4:40) Calcolo Confidence Score (mostrare formula breakdown)
3. (4:40-4:50) Output finale:
   - MQTT publish su `tr4d3rz/prediction/daily`
   - Visualizzazione nell'Observatory
   - Archivio nel Replay System

**Device Mostrati**:
- **Linux PC** (Prediction Service)
- **Browser** (Observatory + Replay System)
- **MQTT Broker**

**MQTT Topics da Mostrare**:
```
PUBLISH tr4d3rz/ecosystem/prediction/daily
  Payload: {
    biome_id: "bio-energy-stable-2026",
    symbol: "ENI.MI",
    signal: "BUY",
    consensus: 0.935,
    confidence: 0.89,
    components: {
      lineage: 0.92,
      niche_strength: 0.85,
      cooperation_value: 0.91
    },
    timestamp: 1747459200
  }
  QoS: 1
```

**Audio/Narrazione**:
> "The final output is not a single indicator, but ecological consensus. 187 specialized agents within bio-energy-stable agree: buy ENI. The confidence score combines lineage stability, niche strength, and cooperation value. The prediction service publishes the signal. The replay system validates it against historical data. The observatory visualizes active biomes in real-time."

---

### SCENA 8: Chiusura e Key Takeaways (4:50 - 5:00)
**Durata**: 10 secondi

**Visualizzazione**:
- Ritorno alla vista d'insieme della rete (come Scena 1)
- Overlay con bullet points:
  ```
  ✓ Distributed Evolution (ESP8266 → Linux)
  ✓ Emergent Specialization (Agent-Driven Biomes)
  ✓ Self-Repair (Lifecycle: Birth → Collapse)
  ✓ Zero Human Bias (Market-Validated Strategies)
  ```

**Audio/Narrazione**:
> "TR4D3RZ: an evolutionary ecology that discovers market structure through distributed computation, emergent specialization, and continuous adaptation. No predefined strategies. No human bias. Only survival."

---

## 3. Requisiti Tecnici di Produzione

### 3.1 Assets Richiesti

**CRITICAL**: NON CREARE assets da zero. Utilizzare gli assets esistenti nel repository:

1. **ArchiMate Diagrams**:
   - Source: `docs/linux.html`, `docs/android.html`, `docs/esp.html`, etc.
   - Usare le visualizzazioni HTML esistenti (screenshot o screen recording)
   - NON ridisegnare i diagrammi

2. **Holistic View**:
   - Source: `docs/holistic_view.html`
   - Screen recording della visualizzazione D3.js
   - Simulare interazioni (hover per evidenziare path)

3. **Device Hardware**:
   - ESP8266: Usare foto stock di "ESP8266 NodeMCU" (licenza CC0)
   - STM32F3: Usare foto stock di "STM32F3 Discovery Board"
   - Linux PC: Usare icona generica server rack
   - Android: Usare icona generica smartphone

4. **Code Snippets**:
   - NON mostrare code fittizio
   - Usare snippet reali dai repository (anche se non ancora implementati, usa le spec):
     - L-System: `specs/core/lsystem-genome-spec.md`
     - FSM: `specs/core/fsm-runtime-spec.md`
     - Fitness: `specs/evolution/fitness-calculation-spec.md`

5. **MQTT Messages**:
   - Usare i topic definiti in `protocols/mqtt-topic-structure.md`
   - Usare schemi CBOR definiti negli ADR

### 3.2 Stile Visivo

**Palette Colori** (da rispettare esattamente):
- Background: `#FFFFFF` (bianco)
- Testo principale: `#000000` (nero)
- Accenti primari: `#333333` (grigio scuro)
- Highlight success: `#4CAF50` (verde)
- Highlight failure: `#F44336` (rosso)
- Biome clusters: Usare palette da `docs/holistic_view.html` (layer colors già definiti)

**Typography**:
- Font principale: `Courier New` (monospace, coerente con i diagrammi)
- Titoli: `12pt bold`
- Code: `11pt regular`
- Narrazione: `10pt regular`

**Layout**:
- Risoluzione: 1920x1080 (Full HD)
- Safe area: 1820x980 (margini 50px)
- Split screen: divisione verticale esatta a 960px (centro schermo)

### 3.3 Audio

**Narrazione**:
- Voce: TTS professionale (es. Amazon Polly "Joanna" o Google Cloud TTS "en-US-Wavenet-F")
- Velocità: 150 parole/minuto (comprensibile per contenuto tecnico)
- Formato: WAV 48kHz stereo

**Musica di sottofondo** (opzionale, volume -30dB rispetto alla voce):
- Genere: Ambient electronic / Minimal techno
- BPM: 80-100 (ritmo lento, non distraente)
- Licenza: CC0 o royalty-free

**Sound Effects** (usare con parsimonia):
- MQTT publish: Leggero "ping" (200ms)
- Biome emergence: Crescendo sintetizzato (1s)
- Collapse: Decrescendo (0.5s)

### 3.4 Animazioni

**Transizioni tra scene**:
- Tipo: Hard cut (NO fade, NO dissolve)
- Durata: 0 frame (istantaneo)
- Eccezione: Scena 1→2 e 7→8 possono usare fade 0.5s

**Animazioni interne**:
- L-System expansion: 30 FPS, interpolazione lineare
- MQTT message flow: Percorso lineare con velocità costante 500px/s
- Fitness graph: Line chart con animazione da sinistra a destra, 1s per completare
- Biome emergence: Particles che si muovono verso il centro con easing `cubic-bezier(0.4, 0.0, 0.2, 1)`, durata 2s

**Regole generali**:
- NO animazioni superflue (no bounce, no elastic, no rotation senza motivo)
- Ogni animazione deve avere uno scopo informativo
- Frame rate: 30 FPS costante (NO variazioni)

### 3.5 Overlay e Annotations

**MQTT Topic Overlay** (quando mostrati):
- Posizione: Top-right corner, margine 20px
- Background: `rgba(0, 0, 0, 0.8)` (nero semi-trasparente)
- Testo: `#00FF00` (verde terminal-style)
- Font: `Courier New 10pt`
- Formato:
  ```
  [MQTT] PUBLISH tr4d3rz/topic/here
         QoS: 1 | Size: 256 bytes
  ```

**Device Labels**:
- Posizione: Below/above device visualization
- Formato: `[Device Type] - [Architecture]`
- Esempio: `[ESP8266] - 80MHz ARM`

**Metrics Overlay** (per fitness/confidence):
- Posizione: Bottom-left corner
- Formato: Box con bordo `#333333`, padding 10px
- Contenuto: Key-value pairs, allineati a sinistra

---

## 4. Deliverables

**Output Richiesti**:

1. **Video Finale**:
   - Formato: MP4 (H.264, AAC audio)
   - Risoluzione: 1920x1080
   - Frame rate: 30 FPS
   - Bitrate: 8 Mbps (video), 192 Kbps (audio)
   - Durata: 4:50 - 5:10 (accettabile range)

2. **Transcript** (file .srt):
   - Sottotitoli sincronizzati con narrazione
   - Formato SubRip (.srt)
   - Include anche annotation dei topic MQTT (come testo alternativo)

3. **Scene Breakdown Document**:
   - File Markdown con timestamp esatti per ogni scena
   - Lista di tutti gli assets utilizzati
   - Note su eventuali deviazioni dalla spec

4. **Source Files** (opzionale, ma consigliato):
   - Project file del video editor utilizzato (Premiere/DaVinci)
   - Assets separati (PNG, SVG, audio clips)

---

## 5. Criteri di Accettazione

Il video sarà considerato completo se e solo se:

1. ✅ Tutte le 8 scene sono presenti e rispettano i timing (±5s tolleranza)
2. ✅ I MQTT topic mostrati corrispondono esattamente a quelli in `protocols/mqtt-topic-structure.md`
3. ✅ Gli assets utilizzati provengono dal repository (NO creazione arbitraria)
4. ✅ La narrazione segue esattamente i testi forniti (±5% parole accettabile)
5. ✅ Il Biome `bio-energy-stable-2026` è mostrato con i simboli specificati: ENI.MI, ENEL.MI, ERG.MI
6. ✅ Il calcolo della Confidence Score mostra i 3 fattori: lineage, niche_strength, cooperation_value
7. ✅ Il ciclo vitale del Bioma mostra le 4 fasi: Birth, Expansion, Climax, Collapse
8. ✅ L'audio è comprensibile (voce chiara, musica non invasiva)

**Criteri di Rifiuto** (se presenti, il video deve essere rifatto):

1. ❌ Topic MQTT inventati o non corrispondenti alle spec
2. ❌ Device non esistenti nella documentazione (es. "Raspberry Pi 5" quando nel repo c'è solo Pi 1 e 2)
3. ❌ Animazioni/transizioni che violano le regole (es. fade tra scene interne)
4. ❌ Durata totale < 4:30 o > 5:30 (troppo breve/lungo)
5. ❌ Narrazione che contraddice SPEC-EVO-002 (es. "nicchie predefinite")

---

## 6. Note per l'Implementazione

### 6.1 Simulazione dei Dati

Dato che il sistema non è completamente implementato, utilizzare i seguenti dati simulati (ESATTAMENTE come specificato):

**Simboli di Mercato**:
- ENI.MI (Eni S.p.A.)
- ENEL.MI (Enel S.p.A.)
- ERG.MI (ERG S.p.A.)
- A2A.MI (A2A S.p.A.) - usato solo in fase di Expansion

**Agenti Simulati**:
- Popolazione iniziale: 500 agenti
- Lineage principale: `lin-78f2-a1` (150 agenti)
- Lineage secondari: `lin-a3f1-b4`, `lin-c9e2-d7` (175 agenti ciascuno)
- Agents che partecipano al Bioma: 127 → 200 (durante expansion) → 87 (dopo collapse)

**Fitness Values**:
- Range: [0.0, 1.0]
- Media population: 0.4
- Media Bioma (climax): 0.9
- Post-collapse: 0.2

**Timeline**:
- t=0: Birth del Bioma
- t=3 days: Expansion (A2A.MI si unisce)
- t=7 days: Climax (fitness stabile)
- t=11 days: Regime change → Collapse
- t=12 days: Archetype salvato

### 6.2 Troubleshooting

**Se non trovi un asset nel repository**:
1. Controlla `docs/` folder prima
2. Controlla `specs/` per descrizioni testuali
3. Se ancora non esiste: usa placeholder testuale (es. "[L-System Diagram]" invece di creare un'immagine fake)
4. NON INVENTARE contenuto tecnico

**Se una specifica è ambigua**:
1. NON interpretare liberamente
2. Segnala l'ambiguità nel Scene Breakdown Document
3. Usa il comportamento più conservativo (es. se non è chiaro il QoS, usa QoS 1)

**Se il timing non torna**:
1. Priorità agli elementi tecnici (MQTT topics, formule, dati)
2. Riduci le transizioni/pause
3. Accelera leggermente la narrazione (max 160 parole/min)
4. NON tagliare contenuto tecnico per rispettare il timing

---

## 7. Riferimenti

**Documenti da Consultare** (in ordine di priorità):

1. `TR4D3RZ_MARKETING_PRESENTATION.md` - Narrativa principale
2. `specs/evolution/niche-evolution-spec.md` - Dettagli emergenza Biomi
3. `protocols/mqtt-topic-structure.md` - Topic MQTT ufficiali
4. `docs/holistic_view.html` - Visualizzazione Observatory
5. `docs/linux.html` - ArchiMate Linux device (Evolution Node principale)
6. `specs/evolution/architecture-alignment-analysis.md` - Gap analysis (per capire cosa è implementato)

**NON CONSULTARE** (sono outdated o irrilevanti):
- README.md (troppo generico)
- File di codice non ancora implementati (usare le spec invece)

---

## 8. Budget e Timing

**Effort Stimato**: 12-16 ore
**Deadline**: 2026-05-24 (7 giorni da oggi)

**Checkpoint** (per review intermedia):
- 2026-05-20: Scene 1-4 completate (video parziale + storyboard scene 5-8)
- 2026-05-22: Scene 5-8 completate (video completo senza audio)
- 2026-05-23: Audio + final polish
- 2026-05-24: Delivery finale

**Formato Checkpoint Delivery**:
- Video WIP in formato MP4 (anche se incompleto)
- Markdown document con status: `[✓] Done | [WIP] In Progress | [TODO] Not Started` per ogni scena

---

## 9. Contatto e Feedback Loop

**Durante la produzione**:
- Se hai domande tecniche → consulta `specs/` folder
- Se hai domande di design → segui le regole in sezione 3.2
- Se hai bisogno di chiarimenti → documenta la domanda nel Scene Breakdown Document e procedi con l'opzione più conservativa

**Dopo la consegna del checkpoint**:
- Il video WIP sarà revisionato entro 24h
- Feedback sarà fornito in formato: `[Scena X] [Timestamp] [Issue] → [Azione richiesta]`
- Esempio: `[Scena 5] [2:45] Topic MQTT errato (tr4d3rz/biome/... invece di tr4d3rz/ecosystem/environment/...) → Correggere overlay`

---

**END OF SPEC**

Manus: questa specifica è vincolante. Ogni deviazione non giustificata comporterà un rifiuto del deliverable e un re-work completo. Leggi attentamente tutte le sezioni, in particolare:
- Sezione 2 (scene-by-scene) per contenuto
- Sezione 3 (requisiti tecnici) per vincoli di produzione
- Sezione 5 (criteri di accettazione) per validazione

Il video deve essere tecnicamente accurato, visivamente coerente con l'architettura esistente, e narrativamente allineato a SPEC-EVO-002. Non c'è spazio per interpretazioni creative che contraddicano le specifiche.
