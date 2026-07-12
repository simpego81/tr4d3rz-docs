# TR4D3RZ — RISKS & MITIGATIONS

---

## Active Risks

| ID | Risk | Severity | Mitigation |
|---|---|---|---|
| R-001 | RPi 2 Performance Bottlenecks | HIGH | Use NanoMQ, SQLite WAL mode, process priority management. |
| R-002 | Agent Handoff Drift | MEDIUM | Artifact-based handoff, Shared Project Memory (Migration). |
| R-003 | Embedded Network Stability | MEDIUM | Delay-tolerant messaging, CBOR compression, local buffering. |
| R-004 | Documentation/Spec Stale | LOW | Documentation Agent role, single source of truth (`tr4d3rz-docs`). |

---

## Technical Debt

- [ ] `tr4d3rz-messaging` tests coverage needs improvement (current 12/13).
- [ ] `MVP Browser Demo` code is currently inside `specs/` (Needs relocation).
- [ ] Lack of automated CI/CD for cross-repo validation.
