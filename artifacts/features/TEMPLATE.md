# FEATURE ARTIFACT TEMPLATE

This is the standard structure for feature handoffs between agents.

## 1. Specification (`spec.md`)
- **Goal**: Clear, unambiguous objective.
- **Requirements**: Functional and non-functional.
- **Interfaces**: MQTT topics, CBOR schemas, API signatures.

## 2. Architecture (`architecture.md`)
- **Component Diagram**: How it fits in the system.
- **Sequence Diagram**: Key interactions.
- **Module Boundaries**: Shared vs Local.

## 3. Implementation Tasks (`tasks.md`)
- **Breakdown**: Atomic steps for Implementation Agent.
- **Definition of Done**: Specific validation criteria.

## 4. Risks & Mitigations (`risks.md`)
- **Technical Risks**: Performance, edge cases, legacy impact.
- **Assumptions**: Critical dependencies or unverified facts.

## 5. QA & Verification Report (`qa_report.md`)
- **Test Scenarios**: Destructive cases, boundary values.
- **Results**: Evidence of validation (logs, screenshots).
- **Health Check**: Demo status.

## 6. Demo Guide (`demo.md`)
- **Access**: How to run it.
- **Scenario**: Step-by-step walkthrough.
- **Observability**: What to look for.
