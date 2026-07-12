# Milestone 0: Fondazioni

**Status**: In Progress
**Owner**: Manus

---

## Obiettivo

Stabilire le fondamenta architetturali e operative del progetto TR4D3RZ. Questa milestone non produce codice funzionante, ma produce le strutture, i contratti e i documenti che rendono possibile lo sviluppo parallelo e integrato nelle milestone successive.

---

## Deliverables

### Infrastruttura GitHub

- [x] Repository `tr4d3rz-docs` creato e inizializzato
- [x] Repository `tr4d3rz-core` creato
- [x] Repository `tr4d3rz-messaging` creato
- [x] Repository `tr4d3rz-evolution` creato
- [x] Repository `tr4d3rz-observatory` creato
- [x] Repository `tr4d3rz-persistence` creato
- [x] Repository `tr4d3rz-embedded` creato

### Documentazione Architetturale

- [x] ADR-0001: Repository Structure
- [x] ADR-0002: Technology Stack
- [x] ADR-0003: MQTT Broker & Data Source Node
- [x] ADR-0004: OHLCV Data Contract
- [ ] ADR-0005: FSM Runtime Interface

### Diagrammi

- [ ] Deploy Architecture Map (nodi, ruoli, connettività)
- [ ] System Component Diagram
- [ ] Genome Pipeline Diagram (L-System → Graph → FSM → Phenotype)
- [ ] Event Flow Diagram

### Protocolli e Contratti Dati

- [ ] Definizione eventi MQTT (topic structure, payload schema)
- [ ] Definizione Genome Capsule format (CBOR schema)
- [ ] Definizione Fitness Result schema
- [ ] Definizione Event Sourcing schema (mutation, death, signal, niche, migration, lineage, archetype)

### Setup Multi-Agent

- [x] Definizione ruoli AI (Manus, Claude Code, Antigravity, GitHub Copilot)
- [x] Definizione regole operative multi-agent
- [x] Template di task assignment per Claude Code
- [x] Template di task assignment per Antigravity

---

## Dipendenze

Nessuna dipendenza esterna. Questa milestone è il prerequisito per tutte le successive.

---

## Criteri di Completamento

La Milestone 0 è completata quando tutti i deliverables sopra sono marcati come completati e il team multi-agent è pronto a iniziare la Milestone 1 con contratti e interfacce chiari.
