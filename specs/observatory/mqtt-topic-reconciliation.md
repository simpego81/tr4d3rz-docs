# MQTT Topic Reconciliation: Video Spec vs Protocol

**Data**: 2026-05-17  
**Autore**: Claude Code  
**Revisore**: Manus

---

## Stato Attuale: Allineamento Completato

Tutti i topic MQTT nella specifica video (`video-technical-use-cases-spec.md`) sono stati **corretti e allineati** al protocollo ufficiale (`protocols/mqtt-topic-structure.md`).

---

## Tabella di Riconciliazione

| Topic nella Video Spec (ORIGINALE) | Protocollo Ufficiale | Stato | Azione Effettuata |
|------------------------------------|----------------------|-------|-------------------|
| `tr4d3rz/genome/new/{genome_id}` | `tr4d3rz/node/{node_id}/capsule/out` | ✅ Corretto | Sostituito con `node/linux-evo-01/capsule/out` in Scena 2 |
| `tr4d3rz/market/ohlcv/ENI.MI` | `tr4d3rz/data/ohlcv/ENI.MI` | ✅ Corretto | Sostituito con `data/ohlcv/ENI.MI` in Scena 3 |
| `tr4d3rz/ecosystem/signal/{agent_id}` | `tr4d3rz/ecosystem/signal/{agent_id}` | ✅ Già corretto | Nessuna modifica necessaria |
| `tr4d3rz/ecosystem/fitness/{agent_id}` | `tr4d3rz/ecosystem/fitness/{agent_id}` | ✅ Già corretto | Nessuna modifica necessaria |
| `tr4d3rz/ecosystem/environment/{env_id}/definition` | `tr4d3rz/ecosystem/environment/{env_id}/definition` | ✅ Già corretto | Confermato in SPEC-EVO-002 (riga 28) |
| `tr4d3rz/evolution/bias/topology` | `tr4d3rz/ecosystem/environment/{env_id}/bias` | ✅ Corretto | Unificato con `context` in un unico topic `bias` con `bias_type` nel payload |
| `tr4d3rz/evolution/bias/context` | `tr4d3rz/ecosystem/environment/{env_id}/bias` | ✅ Corretto | Unificato con `topology` (vedi sopra) |
| `tr4d3rz/prediction/daily` | `tr4d3rz/ecosystem/prediction/daily` | ✅ Corretto | Spostato sotto namespace `ecosystem/` in Scena 7 |
| `tr4d3rz/persistence/archetype/save` | `tr4d3rz/lineage/archetype/{archetype_id}` | ✅ Corretto | Sostituito con `lineage/archetype/arch-bio-energy-stable-2026` in Scena 6 |

---

## Modifiche al Protocollo Ufficiale

Durante la riconciliazione, sono stati **aggiunti** i seguenti topic al protocollo ufficiale (`mqtt-topic-structure.md`) perché necessari per SPEC-EVO-002 ma mancanti:

1. **`ecosystem/environment/{env_id}/lifecycle`** (QoS 2)
   - **Rationale**: Tracciare eventi del ciclo vitale dei Biomi (Birth → Expansion → Climax → Collapse)
   - **Payload**: `{status: "BIRTH|EXPANSION|CLIMAX|COLLAPSE", reason: "...", timestamp: ...}`

2. **`ecosystem/prediction/{timeframe}`** (QoS 1)
   - **Rationale**: Output aggregato del Prediction Service per segnali di trading validati ecologicamente
   - **Timeframe**: `daily`, `weekly`, `monthly`
   - **Payload**: `{biome_id, symbol, signal, consensus, confidence, components: {lineage, niche_strength, cooperation_value}}`

3. **QoS Levels aggiornati** per topic già esistenti ma non documentati:
   - `ecosystem/fitness/*` → QoS 1
   - `ecosystem/niche/*` → QoS 1
   - `ecosystem/environment/*/bias` → QoS 1
   - `data/ohlcv/*` → QoS 0
   - `node/*/status` → QoS 0

---

## Nota sull'Unificazione dei Topic `bias`

**DECISIONE ARCHITETTURALE**:

Originariamente la video spec aveva:
- `tr4d3rz/evolution/bias/topology` per segnali di Topology Bias all'L-System
- `tr4d3rz/evolution/bias/context` per segnali di Context Awareness al Phenotype

Questi sono stati **unificati** in:
- `tr4d3rz/ecosystem/environment/{env_id}/bias`

**Motivazione**:
1. **Coesione semantica**: I segnali di bias sono proprietà dell'Ambiente Locale (Bioma), non dell'engine evolutivo generico
2. **Riduzione complessità**: Un singolo topic con `bias_type` nel payload è più semplice da gestire e sottoscrivere
3. **Estensibilità**: Futuri tipi di bias possono essere aggiunti senza creare nuovi topic

**Schema Payload**:
```json
{
  "env_id": "bio-energy-stable-2026",
  "bias_type": "topology|context|mutation|...",
  "target_component": "lsystem|phenotype|mutation_engine|...",
  "agent_family": "lin-78f2-a1",   // per topology bias
  "regime": "low-vol-bull",         // per context bias
  "... (altri parametri specifici per tipo)"
}
```

---

## Nota sull'Ambiente vs Nicchia

**CHIARIMENTO** per evitare confusione futura:

Il protocollo MQTT definisce **sia** `niche/{niche_id}` **sia** `environment/{env_id}/...`. Non sono duplicati:

- **`ecosystem/niche/{niche_id}`**: 
  - Eventi di **niche discovery** generici
  - Pubblicati quando il clustering system rileva una nuova nicchia di mercato candidata
  - QoS 1 (importante ma non critico)
  
- **`ecosystem/environment/{env_id}/definition`**:
  - Dichiarazione formale di un **Ambiente Locale (Bioma)** validato
  - Pubblicato solo quando consenso + stabilità + specificità superano le soglie
  - QoS 2 (critico, deve essere persistito)
  - Include metadati aggiuntivi (symbols, agent_family, regime_signature, confidence)

**Relazione**: `niche` è un **pre-requisito** per `environment`. Non tutte le nicchie diventano Biomi, ma tutti i Biomi originano da nicchie.

**Flusso**:
```
Clustering System → niche/{id} (QoS 1)
                        ↓
         [Validazione: consensus + stability + specificity]
                        ↓
Niche Discovery → environment/{id}/definition (QoS 2)
```

---

## Prossimi Passi

1. ✅ **Protocollo MQTT aggiornato** con topic mancanti e QoS levels
2. ✅ **Video Spec corretta** e allineata al protocollo
3. 🔲 **Manus** può procedere con produzione video senza ambiguità
4. 🔲 **Future implementation**: Quando si implementa `tr4d3rz-messaging`, usare il protocollo aggiornato come riferimento ufficiale

---

## Referenze

- **Protocollo Ufficiale**: `protocols/mqtt-topic-structure.md` (aggiornato 2026-05-17)
- **Video Spec**: `specs/observatory/video-technical-use-cases-spec.md` (corretto 2026-05-17)
- **Spec Emergenza Biomi**: `specs/evolution/niche-evolution-spec.md` (SPEC-EVO-002)
- **Architettura Linux**: `device_linux.puml` (device primario per Evolution Nodes)

---

**Manus**: Tutti i topic MQTT nella video spec ora corrispondono **esattamente** al protocollo ufficiale. Puoi procedere con la produzione del video senza ulteriori ambiguità. Se trovi altre discrepanze, segnalale immediatamente — potrebbero indicare un errore nel protocollo che deve essere corretto upstream.
