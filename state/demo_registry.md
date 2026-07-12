# TR4D3RZ — DEMO REGISTRY

This registry tracks all functional demos, their purpose, and health status.

---

## Demo Registry

| ID | Title | Purpose | Status | Location |
|---|---|---|---|---|
| DEMO-001 | MVP Browser Demo | Validate M1 Architecture Simulation | ✅ HEALTHY | `tr4d3rz-docs/specs/mvp-browser-demo/` |
| DEMO-002 | Enhanced MVP Demo | Real Rust Component Integration | ✅ READY | `tr4d3rz-docs/demos/enhanced-mvp/` |

---

## Demo Details

### DEMO-001: MVP Browser Demo

- **Goal**: Full-stack simulation of M1 backbone (Scraper, Evolution, ESP, Logger).
- **Technology**: Node.js, Aedes MQTT, Browser UI.
- **Scenario**:
    1. Start Backend.
    2. Open UI.
    3. Observe simulated message flows between 5 nodes.
- **Observability**: Real-time event log, node status map, payload inspector.
- **Access**: `npm run demo` (in target dir).

---

## Demo Details

### DEMO-002: Enhanced MVP Demo

- **Goal**: Demonstrate real tr4d3rz-core component integration and M1 progress
- **Technology**: Node.js, Rust CLI bridge, tr4d3rz-core
- **Scenario**:
    1. Start server (`npm start`)
    2. Open http://localhost:3100
    3. Explore component status, M1 progress, and Rust data structures
- **Observability**: Component metrics, test status, CBOR size comparison, interactive data explorers
- **Access**: `cd tr4d3rz-docs/demos/enhanced-mvp && npm start`
- **Key Features**:
    - Real tr4d3rz-core types (not mocked)
    - Actual CBOR serialization
    - M1 task progress tracking
    - Interactive GenomeCapsule/FitnessResult/OHLCV explorers

---

## Future Demos (Planned)

| ID | Title | Milestone |
|---|---|---|
| DEMO-003 | Real MQTT Backbone | M1 |
| DEMO-004 | Evolution Loop | M2 |
| DEMO-005 | Galaxy Viewer | M4 |
