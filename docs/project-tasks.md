# TR4D3RZ — Project Tasks

**Owner**: Manus  
**Current milestone**: M1 — Foundational Backbone  
**Workflow**: Multi-agent Markdown-driven coordination

---

## 1. Milestone tracker

| Milestone | Titolo | Stato | Criterio di completamento |
|---|---|---|---|
| M0 | Fondazioni architetturali | IN_PROGRESS | ADR-0005, diagrammi deploy/component/event flow e contratti mancanti completati. |
| M1 | Foundational Backbone Single RPi2 | READY | Demo end-to-end Linux PC → RPi2 → edge node → browser con persistenza eventi. |
| M2 | Embedded Edge | PLANNED | Firmware reale STM32/ESP e controllo mobile validati. |
| M3 | High-Performance Ecology | PLANNED | Nicchie, archetipi e visualizzazione avanzata integrate. |

---

## 2. Task M1

| Task | Agent | Titolo | Milestone | Stato | Repo |
|---|---|---|---|---|---|
| M1-T0 | Manus | Organizzazione MVP, contratti e task queue | M1 | COMPLETED | `tr4d3rz-docs` |
| M1-T1 | Claude Code | Core Rust types, capsule e FSM skeleton | M1 | COMPLETED | `tr4d3rz-core` |
| M1-T2 | Claude Code | Broker MQTT e backbone consolidato RPi2 | M1 | COMPLETED | `tr4d3rz-messaging` |
| M1-T3 | Claude Code | Event logger SQLite su RPi2 | M1 | PENDING | `tr4d3rz-persistence` |
| M1-T4 | Claude Code | Evolution CLI publisher/listener | M1 | PENDING | `tr4d3rz-evolution` |
| M1-T5 | GitHub Copilot | Edge node simulator/ESP fitness worker | M1 | PENDING | `tr4d3rz-embedded` |
| M1-T6 | Antigravity | Observatory MVP dashboard | M1 | PENDING | `tr4d3rz-observatory` |
| M1-T7 | Antigravity | Cross-repo architectural audit | M1 | PENDING | Cross-repo |

---

## 3. Sequenza critica

La sequenza raccomandata è T0 → T1/T2 in parallelo controllato → T3 → T4/T5 → T6 → T7. Se T1 ritarda, T2 può usare gli esempi JSON-debug di `MVP_INTERFACE_CONTRACTS.md`, ma deve aprire un TODO esplicito per sostituire i duplicati con il crate `tr4d3rz-core` appena disponibile.
