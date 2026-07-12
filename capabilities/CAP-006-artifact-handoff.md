# CAP-006: Multi-Agent Artifact Handoff

**Capability ID**: CAP-006  
**Category**: Workflow  
**Status**: ACTIVE  
**Created**: 2026-07-12  
**Last Updated**: 2026-07-12  
**Last Used**: M1-T2-B (Validation gate)  
**Reuse Count**: 3 (M1-T2, M1-T2-B, M1-T3)

---

## Purpose

**What does this capability solve?**

In the TR4D3RZ AI-Native Collaborative Software Studio, work passes between specialized agents (Architect → Implementation → QA → Documentation). Without a standardized handoff protocol, information is lost, requirements are misunderstood, and validation is incomplete.

**Why is this capability reusable?**

Every feature implementation follows this pattern: spec → implementation → validation → documentation. The artifact handoff protocol ensures mutual verification ("the previous agent may have made mistakes") and maintains traceability.

---

## Prerequisites

**Before using this capability, you must have**:

- [x] Understanding of TR4D3RZ agent roles ([AI_ROLES.md](../AI_ROLES.md))
- [x] Access to `tr4d3rz-docs/artifacts/features/` directory
- [x] Task assigned with clear ID (e.g., M1-T2-B)
- [x] Feature artifact template ([TEMPLATE.md](../artifacts/features/TEMPLATE.md))

**Knowledge dependencies**:

- [AI_ROLES.md](../AI_ROLES.md) § Mutual Verification Protocol
- [AGENTS.md](../AGENTS.md) § Protocollo di handover

---

## Procedure

### Step 1: Create Feature Artifact Directory

**What**: Create dedicated directory for feature with unique ID

**How**:
```bash
cd tr4d3rz-docs/artifacts/features/
mkdir FEATURE-<MILESTONE>-<TASK>-<NAME>

# Example
mkdir FEATURE-M1-T2-B
```

**Expected output**: New directory in `artifacts/features/`

**Common issues**: None

---

### Step 2: Architecture Agent — Create Specification

**What**: Document feature requirements, architecture, interfaces, acceptance criteria

**How**:

Create `artifacts/features/FEATURE-<ID>/spec.md`:

```markdown
# Feature Specification: <Feature Name>

**Feature ID**: FEATURE-<ID>  
**Owner**: Architecture Agent  
**Status**: PROPOSED  
**Created**: YYYY-MM-DD

## Purpose

[Why this feature exists, what problem it solves]

## Requirements

### Functional Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Non-Functional Requirements
- [ ] Performance: [target]
- [ ] Reliability: [target]

## Architecture

[Architecture diagrams, component interactions]

## Interfaces

### Input
[Data structures, MQTT topics, API endpoints]

### Output
[Data structures, MQTT topics, API endpoints]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Dependencies

- Depends on: [Other features]
- Blocks: [Other features]

---

**Handoff to**: Implementation Agent  
**Next Step**: Implementation in `<repository>`
```

**Expected output**: Complete specification ready for implementation

**Common issues**: 
- **Issue**: Vague requirements
- **Solution**: Implementation Agent MUST reject and request clarification (Mutual Verification Protocol)

---

### Step 3: Implementation Agent — Implement Feature

**What**: Implement feature according to spec, create tests, document code

**How**:

1. **Read spec carefully**:
```bash
cat tr4d3rz-docs/artifacts/features/FEATURE-<ID>/spec.md
```

2. **If spec is vague, REJECT**:
```markdown
# Implementation Blocked

**Reason**: Specification unclear on [specific issue]  
**Requested**: Clarification on [what needs to be specified]  
**Blocker**: Cannot proceed until resolved
```

3. **If spec is clear, implement**:
```bash
# In target repository
git checkout -b feature/<ID>-<name>

# Implement feature
# Write tests
# Update documentation
```

4. **Create implementation report**:

Create `artifacts/features/FEATURE-<ID>/implementation_report.md`:

```markdown
# Implementation Report: <Feature Name>

**Feature ID**: FEATURE-<ID>  
**Implementer**: Implementation Agent  
**Status**: IMPLEMENTED  
**Date**: YYYY-MM-DD

## What Was Implemented

- [Component 1]: [Description]
- [Component 2]: [Description]

## Files Changed

- `path/to/file1.rs` — [What changed]
- `path/to/file2.rs` — [What changed]

## Tests Added

- `test_scenario_1` — [What it tests]
- `test_scenario_2` — [What it tests]

## Deviations from Spec

[Any intentional deviations with rationale, or "None"]

## Open Questions

[Any uncertainties for QA to verify, or "None"]

---

**Handoff to**: QA Agent  
**Next Step**: Validation
```

**Expected output**: Feature implemented, tests passing, implementation report complete

**Common issues**:
- **Issue**: Tests not written
- **Solution**: QA Agent MUST reject (Mutual Verification)

---

### Step 4: QA Agent — Validate Feature

**What**: Verify feature meets spec, test error handling, validate documentation

**How**:

Create `artifacts/features/FEATURE-<ID>/qa_report.md`:

```markdown
# QA Report: <Feature Name>

**Feature ID**: FEATURE-<ID>  
**QA Agent**: [Agent Name]  
**Status**: [PASS | FAIL]  
**Date**: YYYY-MM-DD

## Validation Checklist

### Functional Correctness
- [ ] Requirement 1 verified
- [ ] Requirement 2 verified

### Error Handling
- [ ] Invalid input rejected gracefully
- [ ] Error messages are clear
- [ ] No panics or crashes

### Documentation
- [ ] README updated
- [ ] Rustdoc/JSDoc complete
- [ ] Examples provided

### Testing
- [ ] Unit tests exist
- [ ] Integration tests exist
- [ ] All tests pass
- [ ] Edge cases covered

### Acceptance Criteria
- [ ] Criterion 1 met
- [ ] Criterion 2 met

## Issues Found

[List issues, or "None"]

## Verdict

**[APPROVED | REJECTED]**

[If rejected, list blockers]

---

**Handoff to**: [Documentation Agent if approved, Implementation Agent if rejected]  
**Next Step**: [Documentation update | Fix issues]
```

**Expected output**: Feature validated, verdict clear

**Common issues**:
- **Issue**: QA too lenient, doesn't challenge assumptions
- **Solution**: QA Agent mandate is "behave destructively" (Mutual Verification)

---

### Step 5: Documentation Agent — Update Documentation

**What**: Update relevant documentation, ensure consistency, link cross-references

**How**:

Create `artifacts/features/FEATURE-<ID>/documentation_report.md`:

```markdown
# Documentation Report: <Feature Name>

**Feature ID**: FEATURE-<ID>  
**Documentation Agent**: [Agent Name]  
**Status**: COMPLETED  
**Date**: YYYY-MM-DD

## Documentation Updated

- [ ] README.md updated with new feature
- [ ] CHANGELOG.md entry added
- [ ] Cross-references added to related docs
- [ ] Knowledge Base updated (if applicable)

## Files Modified

- `path/to/README.md` — [What changed]
- `path/to/CHANGELOG.md` — [Version entry]

## Inconsistencies Detected

[Any documentation inconsistencies found, or "None"]

## Recommendations

[Suggestions for future documentation improvements, or "None"]

---

**Handoff to**: Manus (Chief Architect)  
**Next Step**: Mark task COMPLETED in PROJECT_STATE.md
```

**Expected output**: Documentation complete, feature ready for closure

**Common issues**:
- **Issue**: Documentation Agent rewrites everything unnecessarily
- **Solution**: Mandate is "Read before writing, never rewrite everything"

---

### Step 6: Manus — Close Feature

**What**: Update project state, mark task completed, update dashboard

**How**:

1. **Update PROJECT_STATE.md**:
```markdown
### Task Completed

✅ **M1-T<N>**: <Feature Name> (Implementation Agent)

**Deliverable**:
- [Deliverable 1]
- [Deliverable 2]

**Artifacts**: `artifacts/features/FEATURE-<ID>/`
```

2. **Update TASK_QUEUE.md**:
```markdown
| M1-T<N> | `<repo>` | Implementation Agent | ✅ COMPLETED | ...
```

3. **Update DASHBOARD.md** (if Librarian Agent available):
- Move task from "Current Work" to "Recently Completed"
- Update milestone completion percentage

**Expected output**: Feature officially closed, traceability maintained

**Common issues**: None

---

## Expected Outcomes

**After completing this capability, you should have**:

- ✅ Feature artifact directory created with unique ID
- ✅ Specification complete and unambiguous
- ✅ Implementation matches spec
- ✅ QA validation passed
- ✅ Documentation updated
- ✅ Feature closed in PROJECT_STATE.md

**Validation criteria**:

- [ ] `artifacts/features/FEATURE-<ID>/spec.md` exists and complete
- [ ] `artifacts/features/FEATURE-<ID>/implementation_report.md` exists
- [ ] `artifacts/features/FEATURE-<ID>/qa_report.md` verdict is APPROVED
- [ ] `artifacts/features/FEATURE-<ID>/documentation_report.md` exists
- [ ] PROJECT_STATE.md shows task as COMPLETED

---

## Examples

### Example 1: M1-T2-B (Validation Gate)

**Context**: Heartbeat probe for MQTT validation (PC-to-RPi connectivity testing)

**Artifact Directory**: `artifacts/features/FEATURE-M1-T2-B/`

**Handoff Chain**:
1. Manus → Created spec defining validation requirements
2. Claude Code → Implemented `remote_validation_probe.rs`
3. GitHub Copilot → Validated error handling, documentation, exit codes
4. Manus → Closed task, unblocked M1-T5

**Result**: Clean handoff, validation gate operational, M1-T5 unblocked

---

### Example 2: M1-T3 (Event Logger)

**Context**: SQLite event sourcing logger for Observatory

**Artifact Directory**: `artifacts/features/FEATURE-M1-T3-EVENT-LOGGER/`

**Handoff Chain**:
1. Manus → Created spec with schema, MQTT subscription, query API
2. Claude Code → Implements logger (in progress)
3. QA Agent → Will validate persistence and replay
4. Documentation Agent → Will update COMMUNICATION/

**Result**: (In progress)

---

## Common Issues and Troubleshooting

### Issue 1: Implementation Agent accepts vague spec

**Symptoms**: Feature implemented but doesn't match expectations

**Cause**: Mutual Verification Protocol not followed

**Solution**: 
- Implementation Agent MUST reject vague specs
- Architecture Agent must clarify before implementation proceeds
- Add explicit acceptance criteria to spec

---

### Issue 2: QA Agent too lenient

**Symptoms**: Feature passes QA but has issues in production

**Cause**: QA Agent not challenging assumptions

**Solution**:
- QA Agent mandate: "Behave destructively, attempt to break the code"
- Add explicit error handling checks to QA template
- Require edge case testing

---

### Issue 3: Documentation Agent rewrites everything

**Symptoms**: Unnecessary churn in documentation, lost time

**Cause**: Documentation Agent not following "Read before writing" mandate

**Solution**:
- Documentation Agent MUST read existing docs before modifying
- Only update sections relevant to new feature
- Preserve existing structure and style

---

### Issue 4: Information lost between agents

**Symptoms**: Implementation doesn't match spec, QA doesn't test critical requirements

**Cause**: Artifact handoff incomplete

**Solution**:
- Every agent MUST create their artifact report
- Next agent MUST read previous agent's report before starting
- Traceability chain must be complete

---

## Related Capabilities

- [Mutual Verification Protocol](../AI_ROLES.md#mutual-verification-protocol) — Foundational principle
- [Demo-Driven Development](../KNOWLEDGE_BASE.md#reusable-patterns) — Demo creation as part of handoff

---

## History

**Created**: 2026-07-12 by Librarian Agent (Claude Code)  
- Extracted from M1-T2-B, M1-T3 artifact handoff workflows
- Formalized mutual verification protocol
- Standardized artifact report templates

---

## Maintenance Notes

**Maintainer**: Librarian Agent

**Review frequency**: After each milestone completion

**Deprecation criteria**: If agent roles or workflow significantly changes

**Known Variations**:
- Meta-layer agents (Meta-Optimizer, Debug Intelligence, Librarian) have different handoff patterns (orthogonal to feature development)
- Some features may skip Documentation Agent if no user-facing changes

---

**Capability Version**: 1.0  
**Last Updated**: 2026-07-12

