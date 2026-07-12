# TR4D3RZ MVP Browser Demo

**Purpose**: Validate M1 architectural design with browser-based simulation before hardware implementation  
**Status**: Design Complete, Ready for Implementation  
**Author**: Claude Code  
**Date**: 2026-06-05

---

## Overview

The TR4D3RZ MVP Browser Demo is a **full-stack simulation** of the M1 Foundational Backbone milestone. It runs entirely on a single machine (Node.js backend + browser frontend) and simulates:

- **Raspberry Pi 2 Infrastructure** (MQTT broker, scraper, logger)
- **Linux Evolution Node** (genome capsule generation)
- **ESP8266 Embedded Nodes** (fitness evaluation)
- **Browser Observatory** (real-time visualization)

The demo validates that:
1. The distributed topology works as designed
2. MQTT message flow is correct
3. MVP interface contracts are practical
4. UI can effectively visualize the ecosystem

---

## Documentation Structure

```
mvp-browser-demo/
├── README.md                              # This file
├── MVP_BROWSER_DEMO_SPEC.md               # Detailed specification
├── MVP_DEMO_IMPLEMENTATION_PLAN.md        # Step-by-step implementation guide
└── diagrams/                              # UML diagrams (PlantUML format)
    ├── component-diagram.puml             # System components and relationships
    ├── sequence-diagram.puml              # Evolution cycle message flow
    ├── deployment-diagram.puml            # Runtime deployment structure
    ├── class-diagram.puml                 # Data model and simulator classes
    ├── state-diagram.puml                 # Node state machine
    ├── activity-diagram.puml              # End-to-end activity flow
    └── network-topology.puml              # MQTT network and message routing
```

---

## Key Features

### Simulated Nodes (7 total)

| Node ID | Role | Simulates | MQTT Topics |
|---|---|---|---|
| `rpi2-broker` | Broker | MQTT infrastructure | N/A (broker itself) |
| `rpi2-scraper` | Data Provider | OHLCV data feed | `tr4d3rz/data/ohlcv/history/{isin}` |
| `rpi2-logger` | Persistence | Event logging | Subscribes to `tr4d3rz/#` |
| `linux-evolution-01` | Evolution | Genome capsule generation | `tr4d3rz/node/{esp_id}/capsule/in`<br>`tr4d3rz/ecosystem/fitness/+` |
| `esp8266-01` | Embedded | Fitness evaluation | `tr4d3rz/node/esp8266-01/capsule/in`<br>`tr4d3rz/ecosystem/fitness/{agent_id}` |
| `esp8266-02` | Embedded | Fitness evaluation | `tr4d3rz/node/esp8266-02/capsule/in`<br>`tr4d3rz/ecosystem/fitness/{agent_id}` |
| `browser-observatory` | UI | Real-time visualization | All topics (multi-subscribe) |

### Mock Data

- **OHLCV**: 30 bars of mock daily data (realistic price movements)
- **Genome Capsules**: Simple 3-state FSM (idle → long → flat)
- **Fitness Results**: Random values 0.0-1.0 with 5% error rate
- **Node Status**: Heartbeats every 5 seconds with uptime tracking

### UI Components

1. **Node Status Panel**: Live status of all 7 nodes (colored indicators)
2. **System Topology Diagram**: SVG visualization of node connections
3. **Event Timeline**: Scrolling log of MQTT messages (auto-scroll)
4. **Genome Capsule Inspector**: JSON viewer for current capsule
5. **Fitness Chart**: Line chart showing fitness over generations
6. **Controls**: Start/stop, speed control, clear logs

---

## Technology Stack

| Layer | Technology | Port/Protocol |
|---|---|---|
| **MQTT Broker** | Aedes (Node.js) | 1883 (MQTT), 9001 (WebSocket) |
| **Backend** | Node.js + Express | 3000 (HTTP) |
| **MQTT Client** | MQTT.js | WebSocket |
| **Frontend** | HTML5 + CSS3 + Vanilla JS | Browser |
| **Charts** | Chart.js (optional) | N/A |
| **Serialization** | JSON (not CBOR for demo) | N/A |

---

## Implementation Timeline

**Total Effort**: 16 hours (2 days)

| Phase | Duration | Status |
|---|---|---|
| 1. Project Setup | 0.5h | ✅ Complete |
| 2. MQTT Broker | 2h | ✅ Complete |
| 3. Mock Data Generators | 1.5h | ✅ Complete |
| 4. Backend Simulators | 3h | ✅ Complete |
| 5. HTTP Server | 0.5h | ✅ Complete |
| 6. Frontend HTML | 1.5h | ✅ Complete |
| 7. Frontend CSS | 1h | ✅ Complete |
| 8. Frontend JavaScript | 3h | ✅ Complete |
| 9. Integration Testing | 2h | 🔲 Ready for Testing |
| 10. Documentation | 1h | ✅ Complete |

---

## UML Diagrams

All diagrams are in PlantUML format (`.puml` files) and can be rendered using:

1. **Online**: [PlantUML Web Server](http://www.plantuml.com/plantuml/uml/)
2. **VS Code**: Install "PlantUML" extension
3. **Command Line**: `plantuml diagrams/*.puml`

### Available Diagrams

1. **Component Diagram**: Shows system components (UI, broker, simulators) and their relationships
2. **Sequence Diagram**: Evolution cycle message flow (capsule → evaluation → fitness)
3. **Deployment Diagram**: Runtime deployment on localhost (ports, processes, containers)
4. **Class Diagram**: Data models (OHLCV, GenomeCapsule, FitnessResult) and simulator classes
5. **State Diagram**: Node state machine (disconnected → connecting → booting → ready)
6. **Activity Diagram**: End-to-end activity flow for all simulators
7. **Network Topology**: MQTT network with message routing and QoS levels

---

## Success Criteria

The demo is successful when:

- ✅ All 7 simulated nodes connect and show "Ready" status
- ✅ OHLCV data published every 5 seconds
- ✅ Genome capsules routed to correct ESP8266 nodes
- ✅ Fitness results returned and logged
- ✅ UI updates in real-time without refresh
- ✅ Message flow matches sequence diagrams
- ✅ All payloads conform to `MVP_INTERFACE_CONTRACTS.md`
- ✅ Demo runs for 5+ minutes without crashes

---

## How to Use This Documentation

### For Implementation

1. Read `MVP_BROWSER_DEMO_SPEC.md` for architectural overview
2. Follow `MVP_DEMO_IMPLEMENTATION_PLAN.md` step-by-step
3. Reference UML diagrams for design clarity
4. Validate against MVP contracts in `tr4d3rz-docs/protocols/`

### For Presentation

1. Render UML diagrams to PNG/SVG
2. Include in slide deck with architectural narrative
3. Run live demo during stakeholder meeting
4. Use Event Timeline to show real-time message flow

### For Validation

1. Compare demo behavior to M1 specifications
2. Verify MQTT topics match `mqtt-topic-structure.md`
3. Validate payload schemas against `MVP_INTERFACE_CONTRACTS.md`
4. Test edge cases (node disconnect, message loss, high load)

---

## Next Steps After Demo

1. **Gather Feedback**: Stakeholder input on UI/UX
2. **Validate Contracts**: Confirm MVP schemas are practical
3. **Identify Gaps**: Update specs based on lessons learned
4. **Refine M1 Plan**: Adjust task breakdown if needed
5. **Begin Real Implementation**: Start M1-T2 (tr4d3rz-messaging)

---

## Dependencies on TR4D3RZ Docs

This demo references:

- `protocols/MVP_INTERFACE_CONTRACTS.md` (data schemas)
- `protocols/mqtt-topic-structure.md` (topic hierarchy)
- `specs/manus_master_spec.md` (architectural principles)
- `specs/RESTRUCTURING_INSTRUCTIONS_SINGLE_RPI2.md` (topology)
- `adr/ADR-0002-technology-stack.md` (tech choices)
- `adr/ADR-0004-ohlcv-data-contract.md` (OHLCV format)

---

## Contributing

When implementing the demo:

1. Follow the implementation plan phases sequentially
2. Commit after each phase completion
3. Test each component in isolation before integration
4. Document any deviations from the spec
5. Update this README with actual implementation notes

---

## License

This demo is part of the TR4D3RZ project.

---

**Status**: ✅ **IMPLEMENTATION COMPLETE**  
**Testing**: 🔲 **READY FOR TESTING**  
**Prepared by**: Claude Code  
**Review by**: Manus (Chief Architect)

---

## Quick Start (Implementation Complete!)

```bash
cd C:\projects\seq\tr4d3rz-docs\specs\mvp-browser-demo
npm install
npm start
# Open browser to http://localhost:3000
```

See **SETUP.md** for detailed setup instructions and troubleshooting.
