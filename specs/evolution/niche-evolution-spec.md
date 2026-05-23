# Specifica Tecnica: Emergenza Ecologica e Ambienti Locali

**ID Spec**: SPEC-EVO-002
**Stato**: Proposta
**Owner**: Manus (Chief Architect)

---

## 1. Visione
In TR4D3RZ, le nicchie di mercato non sono predefinite staticamente. Esse **emergono** dall'interazione tra la popolazione degli agenti e i dati finanziari. Un **Ambiente Locale (Bioma)** è il risultato di un accoppiamento stabile tra una famiglia di agenti (Genetica) e un cluster di titoli (Mercato) in cui tale famiglia ha dimostrato un successo predittivo superiore alla media.

---

## 2. Il Ciclo di Emergenza (Agent-Driven)

### Fase A: Accumulo di Segnali di Successo
Il sistema monitora il topic `tr4d3rz/ecosystem/fitness/{agent_id}`.
*   **Input**: `(Agent_ID, Symbol, Fitness_Value, Timestamp)`.
*   **Aggregazione**: L'engine di emergenza raggruppa gli agenti per similarità genetica (lineage) e i titoli per coincidenza di successo.

### Fase B: Rilevamento della "Densità di Successo"
Un Ambiente Locale emerge quando:
1.  **Consenso**: Almeno $N$ agenti di una stessa stirpe hanno fitness $> T$ sugli stessi titoli.
2.  **Stabilità**: Il successo persiste per un numero minimo di campioni temporali.
3.  **Specificità**: La stirpe performa significativamente meglio su quel set di titoli rispetto al resto del mercato.

### Fase C: Dichiarazione dell'Ambiente (Bioma)
Viene emesso un messaggio `tr4d3rz/ecosystem/environment/{env_id}/definition`:
```json
{
  "env_id": "bio-energy-stable-2026",
  "symbols": ["ENI.MI", "ENEL.MI", "ERG.MI"],
  "agent_family": "lin-78f2-a1",
  "regime_signature": "low-vol-bull",
  "confidence": 0.85
}
```

---

## 3. Meccanismi di Bias e Specializzazione

Una volta dichiarato un ambiente, il sistema applica una "pressione locale" per accelerare la specializzazione:

### 3.1 Bias Evolutivo (L-System & Mutation)
*   **Topology Bias**: L'L-System riceve istruzioni per favorire moduli strutturali presenti negli agenti di successo dell'ambiente.
*   **Mutation Focus**: Le mutazioni per la `agent_family` coinvolta vengono testate prioritariamente sui `symbols` dell'ambiente.

### 3.2 Bias di Runtime (Phenotype)
*   **Context Awareness**: L'agente riceve un segnale di "Local Bias" che può attivare nodi della FSM specifici per quel contesto.
*   **Resource Allocation**: I nodi `tr4d3rz-embedded` prioritizzano l'elaborazione dei dati appartenenti all'ambiente locale attivo.

---

## 4. Dinamica delle Nicchie

Gli ambienti locali non sono eterni e seguono un ciclo vitale:
1.  **Nascita (Emergence)**: Identificazione iniziale.
2.  **Espansione (Drift)**: Inclusione di nuovi titoli correlati o stirpi affini.
3.  **Stabilità (Climax)**: Alta fitness costante e bassa varianza genetica.
4.  **Collasso (Extinction)**: Declino della fitness dovuto a cambi strutturali del mercato (es. cambio di regime da Bull a Bear).

---

## 5. Visualizzazione (Observatory)
L'Observatory deve rappresentare gli Ambienti Locali come **"Galassie" o "Biomi"** colorati:
* I nodi degli agenti migrano visivamente verso il centro del bioma.
* Gli archi tra agenti e titoli diventano più spessi e luminosi per indicare la forza della nicchia.

---

## 6. Documentazione Visuale dei Meccanismi

Per il dettaglio tecnico dei processi evolutivi, fare riferimento ai seguenti diagrammi PlantUML. I diagrammi usano la gerarchia MQTT canonica `tr4d3rz/...` definita in [`protocols/mqtt-topic-structure.md`](../../protocols/mqtt-topic-structure.md), riportano nei footer i topic coinvolti con la struttura del payload CBOR e rendono esplicito il dispositivo tecnologico che ospita ciascuna entità tramite box, stereotipi o raggruppamenti coerenti con il mapping Cloud/Hub, Edge Node, Distributed Node e Observatory.

1.  **Trascrizione Genomica**: [evolution_genesis.puml](../../diagrams/evolution/evolution_genesis.puml) - Processo da L-System a FSM e pubblicazione dell'evento di nascita.
2.  **Valutazione Fitness**: [evolution_fitness.puml](../../diagrams/evolution/evolution_fitness.puml) - Flusso dati OHLCV, predizione FSM e aggiornamento del punteggio.
3.  **Mutazione e Adattamento**: [evolution_mutation.puml](../../diagrams/evolution/evolution_mutation.puml) - Ciclo di vita dell'agente sotto pressione evolutiva, validazione sandbox e redeploy embedded.
4.  **Persistenza Lineage**: [evolution_lineage.puml](../../diagrams/evolution/evolution_lineage.puml) - Struttura CBOR e persistenza Rust per il tracciamento della discendenza come DAG.
5.  **Simbiosi e Segnalazione**: [evolution_symbiosis.puml](../../diagrams/evolution/evolution_symbiosis.puml) - Cooperazione multi-agente via segnali feromonici e integrazione come input extra della FSM.

