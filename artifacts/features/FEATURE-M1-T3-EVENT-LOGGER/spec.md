# Feature Specification — M1-T3-EVENT-LOGGER

**Owner**: Implementation Agent (Claude Code)  
**Status**: IN_PROGRESS  
**Last Update**: 2026-07-10

---

## What

SQLite-based event logger for TR4D3RZ ecosystem. Subscribes to all MQTT events (GenomeCapsule, FitnessResult, NodeStatus) and persists them in append-only SQLite database with WAL mode for safe concurrent reads.

---

## Why

**Business Motivation**: Enable Observatory UI to display event timeline, replay system evolution, and debug production issues via historical event log.

**Technical Motivation**: 
- Event sourcing pattern for distributed system observability
- Replay capability for post-mortem analysis
- Foundation for archetype memory (M3 milestone)

---

## Acceptance Criteria

- [ ] SQLite schema with append-only events table (id, timestamp, topic, event_type, payload_cbor)
- [ ] MQTT subscriber listening to `tr4d3rz/#` wildcard
- [ ] Events deserialized from CBOR and stored with metadata
- [ ] Query API: get_events(start_time, end_time, event_type filter)
- [ ] Replay API: replay_events(start_time, end_time) → iterator
- [ ] WAL mode enabled for concurrent read/write safety
- [ ] Integration test: publish 100 events → query → verify count and order
- [ ] Demo: CLI tool showing event ingestion, query, and replay
- [ ] Runbook: What to do if SQLite file corrupted or disk full

---

## Out of Scope

- Event deletion (append-only, no DELETE)
- Event schema migration (v0.1 schema is frozen)
- Compression or archival (future: M2+)
- Distributed replication (future: multi-RPi setup)

---

## Dependencies

- ✅ M1-T1 (`tr4d3rz-core`): Types for GenomeCapsule, FitnessResult, NodeStatus
- ✅ M1-T2 (`tr4d3rz-messaging`): MQTT subscriber library

---

## Open Questions

None — specifications clear from MVP_INTERFACE_CONTRACTS.md
