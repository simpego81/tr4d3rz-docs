# .ecosystem — Decisions Log

**Date**: 2026-07-10  
**Decision Maker**: Human Operator (U422756) + HRA

---

## Decision 1: Veto Enforcement Mechanism

**Question**: Automated (git hooks), Manual (checklist), or Hybrid?

**Decision**: **Manual** (checklist in cognitive boards)  
**Rationale**: Start simple, validate workflow, automate later  
**Timeline**: Phase 1 (M1) manual, Phase 2 (M1-T7) automated for critical gates

---

## Decision 2: .ecosystem Location

**Question**: Workspace root or `tr4d3rz-docs/`?

**Decision**: **`tr4d3rz-docs/.ecosystem/`** (versioned with documentation)  
**Rationale**: Single source of truth, git history for boards and rules, easier cross-machine sync  
**Implementation**: Moved from workspace root to `tr4d3rz-docs/.ecosystem/` on 2026-07-10

---

## Decision 3: Convergence Audit Cadence

**Question**: Weekly, monthly, or event-triggered?

**Decision**: **Event-triggered**  
**Triggers**:
- >5 tasks marked COMPLETED without git commits
- Requirement churn >3 for any task
- Rework ratio >0.4
- Cognitive loop detected
- Human requests audit
- End of milestone (M1-T7, M2, etc.)

**Rationale**: Optimize for signal-to-noise. Weekly audits may be noisy during stable periods.  
**Baseline**: First audit completed 2026-07-10 (transition event)

---

## Decision 4: M1-T2-B Hardware Validation

**Question**: Was Heartbeat Probe tested on Raspberry Pi 2?

**Decision**: **YES — Tested and OK**  
**Date**: Confirmed 2026-07-10  
**Impact**: M1-T5 (ESP8266) now UNBLOCKED  
**Action**: Document in `tr4d3rz-messaging/COMMUNICATION/VALIDATION_REPORT.md`

---

## Decision 5: Git Commit M1-T1/M1-T2

**Question**: Approve immediate commit and push to GitHub?

**Decision**: **APPROVED**  
**Date**: 2026-07-10 20:15 UTC  
**Commits**:
- `tr4d3rz-core`: e8ecad4 (feat(M1-T1): Implement core Rust types and FSM skeleton)
- `tr4d3rz-messaging`: af19bee (feat(M1-T2): Implement Rust MQTT client library)

**Impact**: Git commit deficit resolved, M1-T1/M1-T2 now traceable and available on GitHub

---

*Decisions logged by HRA for auditability and continuity*
