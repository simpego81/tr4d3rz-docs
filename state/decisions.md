# TR4D3RZ — ARCHITECTURAL DECISIONS

This log tracks key architectural decisions and their impact. For full details, see `adr/`.

---

## Decisions Log

| ID | Date | Decision | Status | ADR |
|---|---|---|---|---|
| D-001 | 2026-06-01 | Use 7 specialized repositories | ACCEPTED | ADR-0001 |
| D-002 | 2026-06-02 | Rust as primary implementation language | ACCEPTED | ADR-0002 |
| D-003 | 2026-06-03 | MQTT as primary messaging protocol | ACCEPTED | ADR-0003 |
| D-004 | 2026-06-04 | CBOR for binary serialization | ACCEPTED | ADR-0004 |
| D-005 | 2026-06-10 | Single RPi 2 as master node | ACCEPTED | - |
| D-006 | 2026-06-14 | Remote Validation Probe mandatory | ACCEPTED | - |
| D-007 | 2026-06-16 | AI-Native Collaborative Studio migration | ACCEPTED | - |

---

## Key Principles

1. **Interfaces Before Code**: Contracts must be defined in `protocols/` or `specs/`.
2. **Open-Ended Evolution**: No hard limits on genome complexity; use fitness pressure.
3. **Asynchronous Ecology**: Delay-tolerant, non-blocking messaging.
4. **Observable by Design**: Every event must be serializable and replayable.
