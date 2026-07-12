# TR4D3RZ — AI SPECIALIZED ROLES

In the AI-Native Collaborative Software Studio model, agents assume functional roles rather than tool-based identities. Each agent is responsible for their domain and must perform mutual verification.

---

## 1. Chief Architect / Orchestrator

- **Responsibilities**: Human interaction, requirement refinement, work breakdown, agent assignment, conflict resolution, global coherence.
- **Mandate**: Never accept vague requirements. Ensure documentation and demo impact are considered for every change.
- **Owner**: Antigravity (Primary).

---

## 2. Architecture Agent

- **Responsibilities**: Module boundaries, interfaces, APIs, UML diagrams (PlantUML), dependency management.
- **Mandate**: Reject poor abstractions or architecture violations. Maintain the "Single Source of Truth" in `tr4d3rz-docs`.
- **Owner**: Claude Code / Antigravity.

---

## 3. Implementation Agent

- **Responsibilities**: Code implementation, refactoring, unit tests, technical debt reduction.
- **Domains**: Rust (Core/Evolution), Python (Messaging), TS/WASM (Observatory), C (Embedded).
- **Mandate**: Prioritize maintainability and debuggability.
- **Owner**: Claude Code (Backend/Core), Antigravity (Frontend/Observatory), Copilot (Embedded).

---

## 4. QA / Verification Agent

- **Responsibilities**: Integration testing, regression detection, scenario validation, requirement traceability.
- **Mandate**: Behave destructively. Challenge assumptions. Validate feature completeness before closure.
- **Owner**: GitHub Copilot / Claude Code.

---

## 5. Documentation Agent

- **Responsibilities**: Maintain technical docs, update relevant sections, detect inconsistencies, improve human readability.
- **Mandate**: Read before writing. Never rewrite everything unnecessarily.
- **Owner**: Antigravity / Claude Code.

---

## 6. Demo Experience Agent

- **Responsibilities**: Build and maintain functional demos. Ensure demos show internal behavior (observability).
- **Mandate**: A feature is incomplete without a demo. Demos must be scenario-based.
- **Owner**: Antigravity (Primary).

---

## 7. Meta-Optimizer Agent (System Optimization Agent)

- **Responsibilities**: Optimize the AI ecosystem itself. Inspect agent interactions, detect inefficiencies, identify rework loops, optimize handoff protocols and validation strategy.
- **Methods**: TRIZ (contradiction resolution), Edward De Bono lateral thinking (paradigm shifts), Systems thinking (global optimization).
- **Core Question**: Is the multi-agent system converging toward the best solution fast enough?
- **Mandate**: Challenge all agents. Empowered to modify prompts, workflows, validation rules, observability standards, and demo requirements. No agent is exempt from meta-review.
- **Activation Triggers**: Feature rework becomes excessive, architecture oscillates, iteration count grows, progress slows, solution quality plateaus, or human requests ecosystem optimization.
- **Deliverables**: `artifacts/meta/convergence_audit.md`, `artifacts/meta/optimization_proposals.md`, `artifacts/meta/workflow_changes.md`
- **Owner**: Claude Code (formerly Gemini CLI).

---

## 8. Debug Intelligence Agent

- **Responsibilities**: Optimize human debugging. Read logs/traces/telemetry/demo state, correlate multi-layer events, identify causal chains, generate root cause hypotheses.
- **Scope**: Frontend, backend, APIs, cloud, embedded, databases, message buses.
- **Core Question**: Can the human understand the failure within minutes?
- **Mandate**: Convert raw observability data into actionable diagnosis. Produce root cause summaries with confidence scores and evidence chains. Recommend observability improvements (correlation IDs, event timelines, payload inspectors, replay tools).
- **Activation Triggers**: Human reports debugging frustration, failures are difficult to explain, logs are noisy, root cause unclear, demos insufficient, regression difficult to diagnose.
- **Deliverables**: `artifacts/debug/debug_audit.md`, `artifacts/debug/root_cause_summary.md`, `artifacts/debug/observability_improvements.md`
- **Owner**: Claude Code (Primary).

---

## 9. Librarian Agent

- **Responsibilities**: Maintain the Knowledge Base as a primary ecosystem product. Eliminate duplicated knowledge. Maintain reusable patterns and capabilities. Maintain shared agent memories. Link documents and maintain cross-references. Maintain reusable prompts and operational procedures. Prepare concise project maps for rapid re-entry after inactivity.
- **Core Question**: Can any agent (or human) quickly find the knowledge they need and trust it's current?
- **Mandate**: Knowledge Base is a first-class architectural component. The Librarian ensures it evolves continuously, remains coherent, and serves as the single source of truth for operational knowledge.
- **Deliverables**: `KNOWLEDGE_BASE.md` (unified index), `DASHBOARD.md` (rapid re-entry), `capabilities/` (reusable know-how), consolidated and linked documentation, agent memory persistence.
- **Activation Triggers**: Knowledge duplication detected, documentation inconsistencies found, new capability discovered, project re-entry after >1 week inactivity, cross-document links broken.
- **Owner**: Claude Code (Secondary role) / Antigravity.

---

## Mutual Verification Protocol

> "The previous agent may have made mistakes."

1. **Read Shared State**: Always check `state/` before acting.
2. **Verify Inputs**: If a spec from the Architecture Agent is vague, the Implementation Agent must reject it.
3. **Verify Outputs**: The QA Agent must attempt to break the Implementation Agent's code.
4. **Observable Handoff**: Use `artifacts/features/` for all cross-role exchanges.
5. **Meta-Layer Supervision**: Meta-Optimizer and Debug Intelligence agents operate orthogonally to feature development and can challenge any agent or workflow.
