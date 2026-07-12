# Conflicts & Veto Registry

**Purpose**: This directory logs conflicts detected by the Panopticon Collaborativo veto system. Each conflict represents a blocked action that requires resolution or human arbitration.

---

## Conflict Types

### 1. Incomplete Handoff
**Pattern**: `{task-id}_incomplete_handoff.md`  
**Trigger**: Agent marks task COMPLETED without fulfilling Pre-Commit Check (Gate 1)  
**Resolution**: Agent completes missing deliverables (git commit, IMPLEMENTATION_LOG, demo)

### 2. Protocol Violation
**Pattern**: `protocol_violation_{protocol-name}.md`  
**Trigger**: Protocol modified without version bump, changelog, or migration plan (Gate 2)  
**Resolution**: Revert change and follow protocol update process

### 3. Token Waste
**Pattern**: `token_waste_{session-id}.md`  
**Trigger**: Session exceeds 150k tokens without justification (Gate 3)  
**Resolution**: Audit session for optimization opportunities, apply RTK/Headroom

### 4. Demo Missing
**Pattern**: `demo_missing_{task-id}.md`  
**Trigger**: Feature task completed without demo (Gate 4)  
**Resolution**: Create demo or get human approval for exemption

### 5. Requirement Churn
**Pattern**: `requirement_churn_{task-id}.md`  
**Trigger**: Specification modified >3 times (Gate 5)  
**Resolution**: Freeze spec, root cause analysis by Architect

### 6. Cognitive Loop
**Pattern**: `cognitive_loop_{task-id}.md`  
**Trigger**: Two agents iterating on same file >3 times in <1h (Gate 6)  
**Resolution**: Freeze task, human arbitration required

---

## Conflict Lifecycle

1. **Detected**: Veto gate triggered, conflict artifact generated
2. **Notified**: Stakeholders (agent, veto holder, human) alerted
3. **In Progress**: Resolution underway (fix, override, revert, or escalate)
4. **Resolved**: Conflict artifact updated with resolution, timestamp, lessons learned
5. **Archived**: After 30 days, moved to `conflicts/archive/YYYY-MM/`

---

## Active Conflicts

**As of 2026-07-10**: 0 conflicts (veto system just initialized)

---

## Archived Conflicts

*None yet*

---

## How to Resolve a Conflict

### For Agents

1. Read the conflict artifact (`{issue-type}_{task-id}.md`)
2. Review evidence and recommended resolution
3. Choose resolution path:
   - **Fix**: Address violation, update artifact with "Resolution: Fixed by {agent} on {date}"
   - **Override Request**: Add rationale to artifact, tag Antigravity for approval
   - **Revert**: Abandon approach, document in artifact
4. Update your cognitive board (`{agent}_board.md`) with veto received and resolution status

### For Human (Antigravity)

1. Review conflict artifact
2. Decide:
   - **Approve Override**: Add approval and rationale to artifact
   - **Deny**: Instruct agent to fix violation
   - **Escalate**: Move to architectural decision (ADR) if systemic issue
3. Update artifact with final decision and close conflict

---

*Conflicts directory initialized 2026-07-10 by Meta-Optimizer Agent*
