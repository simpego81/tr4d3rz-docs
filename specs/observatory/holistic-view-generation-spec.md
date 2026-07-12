# Specifica Tecnica: Holistic Concentric ArchiMate View

**ID Task**: SPEC-OBS-001
**Owner**: Claude (Implementation) / Antigravity (Review/Integration)
**Repository**: `tr4d3rz-docs`
**Stato**: Proposto

---

## 1. Visione e Obiettivo
Implementare una nuova visualizzazione "olistica" dell'architettura TR4D3RZ basata su un grafo radiale a cerchi concentrici. L'obiettivo è permettere agli stakeholder e agli altri agenti AI di comprendere a colpo d'occhio le dipendenze tra i layer (Motivation, Business, Application, Technology) e il posizionamento dei componenti sui diversi hardware (Technology Devices).

## 2. Architettura dei Dati (Data Refactoring)
Attualmente, i dati ArchiMate sono iniettati staticamente nelle singole pagine HTML. Per supportare la vista olistica, è necessario un approccio basato sui dati.

### 2.1 Estrazione in JSON
Creare un processo (script Python) che scansioni i file `.puml` in `diagrams/per-device/` e generi un file `docs/archimate_data.json` con la seguente struttura:

```json
{
  "elements": {
    "element_id": {
      "title": "Titolo Breve",
      "full_caption": "Descrizione completa...",
      "type": "ArchiMate_Type",
      "layer": "Motivation|Business|Application|Technology",
      "aspect": "Active|Behavior|Passive|Motivation",
      "tech": "Dettagli tecnici...",
      "role": "Ruolo nel sistema..."
    }
  },
  "relationships": [
    { "from": "id1", "to": "id2", "type": "Rel_Type", "label": "Etichetta" }
  ]
}
```

### 2.2 Migrazione Generator
- Sostituire la logica di estrazione embedded in `generate_docs.ps1` con un parser Python robusto (es. `generate_site_v3.py`).
- Le pagine dei singoli device (`docs/*.html`) devono caricare i dati dinamicamente dal JSON o essere rigenerate partendo da esso.

## 3. Implementazione Vista Olistica
Creare `docs/holistic_view.html` utilizzando **D3.js**.

### 3.1 Layout Radiale (Concentric Circles)
I nodi devono essere vincolati a distanze radiali fisse dal centro in base al loro layer ArchiMate:
1.  **Centro (R1)**: `Motivation Layer` (Goals, Drivers, Principles).
2.  **Cerchio 2 (R2)**: `Business Layer` (Processes, Actors).
3.  **Cerchio 3 (R3)**: `Application Layer` (Components, Services).
4.  **Cerchio 4 (R4)**: `Technology Layer` (Infrastructure, System Software).
5.  **Periferia (R5)**: `Technology Devices` (Hardware fisici come nodi terminali).

### 3.2 Dinamiche del Grafo (Force-Directed)
- **Forze**: Applicare `d3.forceRadial` per i layer, `d3.forceLink` per le relazioni e `d3.forceCollide` per prevenire sovrapposizioni di etichette.
- **Visualizzazione**: Gli archi (link) devono rappresentare le relazioni ArchiMate (Composition, Realization, Flow, ecc.) con stili differenziati.

### 3.3 Interazione e UX
- **Node Captions (Revisione 01)**: Per gestire l'alta densità di nodi, implementare una logica di "Short Caption" per le etichette visualizzate nel grafo:
    - **Pulizia**: Rimuovere le parti di testo racchiuse tra parentesi (es. "Application Component (Core)" -> "Application Component").
    - **Wrapping**: Se la somma dei caratteri di due parole consecutive supera i 10 caratteri, inserire un ritorno a capo (`\n`) tra di esse.
    - **Full Text**: Il testo originale completo deve rimanere disponibile per il tooltip e il modale.
- **Focus Mode (Revisione 01)**: Al click su un elemento, l'evidenziazione deve essere selettiva:
    - **Upstream (Motivation)**: Evidenziare il percorso unico (unique path) che risale dall'elemento verso il Motivation Layer.
    - **Downstream (Technology)**: Evidenziare tutti i percorsi ramificati (tree structure) che discendono dall'elemento verso i Technology Devices.
    - **Visualizzazione**: Sbiadire (opacity = 0.1) tutti gli altri nodi e archi.
    - **Mouseover Bug Fix**: Assicurarsi che l'interazione di mouseover (tooltip/highlight temporaneo) continui a funzionare correttamente anche dopo che un nodo è stato selezionato (click).
- **Semantic Zoom**:
    - Zoom basso: Solo icone o punti colorati.
    - Zoom medio: Caption brevi.
    - Zoom alto: Caption complete e dettagli tecnici.
- **Tooltip/Modali**: Al mouseover mostrare la `full_caption`; al click aprire il modale ArchiMate standard con i dettagli completi (`role`, `tech`, `relations`).

## 4. Requisiti Non Funzionali
- **Static Hosting**: La soluzione deve funzionare interamente client-side su GitHub Pages.
- **Performance**: Il grafo deve essere fluido (~60fps) su dispositivi moderni con almeno 150-200 nodi e relative relazioni.
- **Integrazione**: Aggiungere un link alla "Holistic View" nel menu di navigazione principale (`index.html`).

---

**Riferimenti**:
- `pseudo-archimate-concentric-graph.md` (Requisiti Utente)
- `ANTIGRAVITY.md` (Workflow e ownership)
