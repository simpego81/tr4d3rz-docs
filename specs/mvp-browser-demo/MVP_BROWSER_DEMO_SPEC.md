# TR4D3RZ — MVP Browser Demo Specification

**Status**: Draft  
**Author**: Claude Code  
**Date**: 2026-06-05  
**Purpose**: Validate M1 architectural intent with browser-based simulation before real hardware implementation

---

## 1. Objectives

### 1.1 Primary Goals

1. **Validate Architectural Intent**: Demonstrate that the M1 distributed topology (Single RPi2, Evolution Nodes, Embedded Nodes, Observatory) works as designed
2. **Test MQTT Message Flow**: Simulate all MVP MQTT topics with realistic payloads
3. **Visualize System Behavior**: Show genome capsule lifecycle, fitness evaluation, and node status
4. **Debug Protocol Contracts**: Validate that MVP_INTERFACE_CONTRACTS.md schemas are practical
5. **Stakeholder Demo**: Provide interactive demo for understanding the system before hardware investment

### 1.2 Non-Goals

- ❌ Real OHLCV data scraping
- ❌ Actual L-System genome generation
- ❌ Production-grade performance
- ❌ Embedded hardware simulation at instruction level
- ❌ Real evolutionary algorithms (fitness is mocked)

---

## 2. Architecture Overview

### 2.1 Technology Stack

| Component | Technology | Rationale |
|---|---|---|
| **MQTT Broker** | Aedes (Node.js in-process broker) | Lightweight, runs in browser Node.js environment |
| **Backend Services** | Node.js + Express | Simulates RPi2 services (scraper, relay, logger) |
| **MQTT Client Library** | MQTT.js (browser + Node.js) | Universal MQTT client |
| **Frontend UI** | HTML5 + CSS3 + Vanilla JS | No build step, fast iteration |
| **Data Serialization** | JSON (not CBOR) | Human-readable for demo/debug |
| **State Management** | In-memory JS objects | Ephemeral demo state |
| **3D Visualization** | Three.js (optional MVP Galaxy view) | Future-compatible with Observatory design |

### 2.2 Simulated Nodes

The demo simulates **7 virtual nodes**:

| Node ID | Simulated Device | Role | Responsibilities |
|---|---|---|---|
| `rpi2-broker` | Raspberry Pi 2 (Broker) | Broker | MQTT broker, WebSocket endpoint |
| `rpi2-scraper` | Raspberry Pi 2 (Scraper) | Data Provider | Publishes mock OHLCV data |
| `rpi2-logger` | Raspberry Pi 2 (Logger) | Persistence | Subscribes to all events, logs to memory |
| `linux-evolution-01` | Linux PC | Evolution | Creates genome capsules, listens for fitness |
| `esp8266-01` | ESP8266 | Embedded/Optimization | Receives capsules, returns fitness |
| `esp8266-02` | ESP8266 | Embedded/Optimization | Receives capsules, returns fitness |
| `browser-observatory` | Browser | Observatory | Visualizes ecosystem state |

---

## 3. System Components

### 3.1 Backend (Node.js)

**File**: `demo-backend.js`

Responsibilities:
- Run Aedes MQTT broker on port 1883
- Serve HTTP on port 3000 (static files + WebSocket bridge)
- Simulate RPi2 services:
  - **Scraper**: Publishes mock OHLCV data every 5 seconds to `tr4d3rz/data/ohlcv/history/IT0001233417`
  - **Logger**: Subscribes to `tr4d3rz/#`, logs all messages with timestamp
  - **Relay**: (Optional) Could transcode messages, but demo uses JSON everywhere
- Simulate Evolution Node:
  - Publishes genome capsule to `tr4d3rz/node/esp8266-01/capsule/in` every 10 seconds
  - Subscribes to `tr4d3rz/ecosystem/fitness/+` for fitness results
- Simulate Embedded Nodes:
  - Subscribe to `tr4d3rz/node/esp8266-01/capsule/in` and `tr4d3rz/node/esp8266-02/capsule/in`
  - Simulate FSM evaluation (random delay 500-2000ms)
  - Publish fitness result to `tr4d3rz/ecosystem/fitness/{agent_id}`
- Publish node status heartbeats every 5 seconds

### 3.2 Frontend (Browser)

**File**: `demo-frontend.html`

Responsibilities:
- Connect to MQTT broker via WebSocket (ws://localhost:9001)
- Subscribe to relevant topics for Observatory view
- Display:
  - **Node Status Panel**: Live status of all 7 simulated nodes
  - **Event Timeline**: Scrolling log of MQTT events (genome capsule, fitness, OHLCV)
  - **Genome Capsule Inspector**: Shows current capsule being evaluated
  - **Fitness Chart**: Line chart showing fitness over time per agent
  - **System Topology Diagram**: SVG visualization of nodes and message flow
  - (Optional) **3D Galaxy View**: Three.js visualization of agents in fitness space

---

## 4. Message Flow Simulation

### 4.1 Startup Sequence

```
T+0s:  [rpi2-broker] MQTT broker starts
T+1s:  [rpi2-scraper] Publishes node status (role: broker, state: ready)
T+1s:  [rpi2-logger] Subscribes to tr4d3rz/#
T+2s:  [linux-evolution-01] Publishes node status (role: evolution, state: ready)
T+2s:  [esp8266-01] Publishes node status (role: embedded, state: ready)
T+2s:  [esp8266-02] Publishes node status (role: embedded, state: ready)
T+3s:  [browser-observatory] Connects via WebSocket, subscribes to topics
```

### 4.2 Evolution Cycle (Repeats every 10s)

```
T+0s:  [linux-evolution-01] Generates mock genome capsule
       └─> agent_id: "agent-demo-001"
       └─> generation: incrementing counter
       └─> fsm: { states: ["idle", "long", "flat"], transitions: [...] }
       └─> Publishes to: tr4d3rz/node/esp8266-01/capsule/in

T+0.5s: [esp8266-01] Receives capsule
        └─> Simulates FSM execution (random delay 500-2000ms)

T+1.2s: [esp8266-01] Publishes fitness result
        └─> fitness: random float 0.0 - 1.0
        └─> status: "ok"
        └─> metrics: { trades: 5, drawdown: 0.12 }
        └─> Publishes to: tr4d3rz/ecosystem/fitness/agent-demo-001

T+1.3s: [linux-evolution-01] Receives fitness result
        └─> Logs result
        └─> (In real system: would trigger mutation/selection)
```

### 4.3 OHLCV Data Feed (Repeats every 5s)

```
T+0s:  [rpi2-scraper] Publishes mock OHLCV history
       └─> isin: "IT0001233417" (Telecom Italia)
       └─> data: Array of 30 mock OhlcvBar objects
       └─> Publishes to: tr4d3rz/data/ohlcv/history/IT0001233417
```

### 4.4 Heartbeat Cycle (Repeats every 5s)

All nodes publish status to `tr4d3rz/node/{node_id}/status`

---

## 5. Mock Data Generation

### 5.1 Mock OHLCV Generator

```javascript
function generateMockOhlcv(isin, bars = 30) {
  const data = [];
  let basePrice = 2.50;
  let ts = Date.now() - (bars * 86400000); // Start 30 days ago
  
  for (let i = 0; i < bars; i++) {
    const volatility = 0.02;
    const o = basePrice;
    const c = o * (1 + (Math.random() - 0.5) * volatility);
    const h = Math.max(o, c) * (1 + Math.random() * volatility);
    const l = Math.min(o, c) * (1 - Math.random() * volatility);
    
    data.push({
      ts: ts + (i * 86400000),
      o: parseFloat(o.toFixed(3)),
      h: parseFloat(h.toFixed(3)),
      l: parseFloat(l.toFixed(3)),
      c: parseFloat(c.toFixed(3)),
      v: Math.floor(Math.random() * 20000000) + 5000000,
      t: Math.floor(Math.random() * 5000) + 1000
    });
    
    basePrice = c; // Next day opens at previous close
  }
  
  return {
    v: 1,
    type: "ohlcv_history",
    isin: isin,
    mic: "MTAA",
    resolution: "1D",
    data: data
  };
}
```

### 5.2 Mock Genome Capsule Generator

```javascript
let generation = 0;

function generateMockGenomeCapsule(agentId) {
  const fsm = {
    states: ["idle", "long", "flat"],
    initial: "idle",
    transitions: [
      { from: "idle", to: "long", when: "close_gt_open" },
      { from: "long", to: "flat", when: "close_lt_open" },
      { from: "flat", to: "idle", when: "volume_low" }
    ]
  };
  
  return {
    v: 1,
    ts: Date.now(),
    node: "linux-evolution-01",
    type: "genome_capsule",
    agent_id: agentId,
    generation: generation++,
    genome_hash: `sha256:mock-${Date.now()}`,
    fsm: fsm,
    budget: {
      max_ticks: 128,
      max_ms: 1000
    }
  };
}
```

### 5.3 Mock Fitness Evaluator

```javascript
function evaluateMockFitness(capsule, nodeId) {
  // Simulate evaluation delay (500-2000ms)
  const delay = 500 + Math.random() * 1500;
  
  setTimeout(() => {
    const fitness = Math.random(); // Random fitness 0.0 - 1.0
    const status = Math.random() > 0.95 ? "error" : "ok"; // 5% error rate
    
    const result = {
      v: 1,
      ts: Date.now(),
      node: nodeId,
      type: "fitness_result",
      agent_id: capsule.agent_id,
      genome_hash: capsule.genome_hash,
      fitness: status === "ok" ? parseFloat(fitness.toFixed(4)) : 0.0,
      metrics: status === "ok" ? {
        trades: Math.floor(Math.random() * 20) + 1,
        drawdown: parseFloat((Math.random() * 0.3).toFixed(3)),
        latency_ms: parseFloat((Math.random() * 50).toFixed(2))
      } : undefined,
      status: status
    };
    
    publishToMqtt(`tr4d3rz/ecosystem/fitness/${capsule.agent_id}`, result);
  }, delay);
}
```

---

## 6. UI Layout

### 6.1 Page Structure

```
┌─────────────────────────────────────────────────────────────┐
│                  TR4D3RZ MVP Browser Demo                   │
│                    M1 Simulation Preview                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────────────────────┐ │
│  │  Node Status     │  │   System Topology                │ │
│  │  Panel           │  │   (SVG Diagram)                  │ │
│  │                  │  │                                  │ │
│  │ • rpi2-broker    │  │   [RPi2] ───┬──→ [ESP8266-01]  │ │
│  │   ✓ Ready        │  │      ↓      └──→ [ESP8266-02]  │ │
│  │ • rpi2-scraper   │  │   [Linux]                       │ │
│  │   ✓ Ready        │  │      ↓                          │ │
│  │ • linux-evo-01   │  │   [Observatory]                 │ │
│  │   ✓ Ready        │  │                                 │ │
│  │ • esp8266-01     │  │                                 │ │
│  │   ✓ Ready        │  │                                 │ │
│  └──────────────────┘  └──────────────────────────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Event Timeline (Live MQTT Messages)                   │ │
│  │  ─────────────────────────────────────────────────────│ │
│  │  [12:34:56] OHLCV Published: IT0001233417 (30 bars)   │ │
│  │  [12:34:58] Genome Capsule: agent-demo-001 gen=5      │ │
│  │  [12:35:00] Fitness Result: agent-demo-001 f=0.8234   │ │
│  │  [12:35:01] Node Status: esp8266-01 Ready             │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─────────────────────┐  ┌──────────────────────────────┐ │
│  │ Genome Capsule      │  │  Fitness Over Time           │ │
│  │ Inspector           │  │  (Line Chart)                │ │
│  │                     │  │                              │ │
│  │ Agent: demo-001     │  │  1.0 ┤                      │ │
│  │ Generation: 5       │  │      │    ╭─╮               │ │
│  │ Hash: sha256:...    │  │  0.5 ┤  ╭─╯ ╰╮              │ │
│  │                     │  │      │╭─╯    ╰─╮            │ │
│  │ FSM:                │  │  0.0 ┼────────────────────  │ │
│  │  States: 3          │  │      0   5   10  15  20     │ │
│  │  Transitions: 3     │  │      Generation             │ │
│  │                     │  │                              │ │
│  └─────────────────────┘  └──────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 UI Components

| Component | Technology | Purpose |
|---|---|---|
| **Node Status Panel** | HTML + CSS grid | Shows all 7 nodes with colored status indicators |
| **System Topology** | SVG | Static diagram showing node connections |
| **Event Timeline** | Auto-scrolling `<div>` | Live MQTT message log |
| **Genome Inspector** | JSON viewer (collapsible) | Shows current capsule details |
| **Fitness Chart** | Chart.js or vanilla SVG | Line chart tracking fitness over generations |
| **Controls** | Buttons | Start/Stop simulation, Clear logs, Speed control |

---

## 7. Deployment

### 7.1 File Structure

```
mvp-browser-demo/
├── package.json              # Node.js dependencies
├── demo-backend.js           # Node.js MQTT broker + simulators
├── public/
│   ├── index.html            # Main UI page
│   ├── style.css             # Styling
│   ├── app.js                # Frontend MQTT client + UI logic
│   ├── chart.min.js          # Chart.js (optional)
│   └── three.min.js          # Three.js (optional for galaxy view)
└── README.md                 # Setup instructions
```

### 7.2 Dependencies

```json
{
  "name": "tr4d3rz-mvp-demo",
  "version": "0.1.0",
  "dependencies": {
    "aedes": "^0.50.0",
    "express": "^4.18.2",
    "mqtt": "^5.3.0",
    "ws": "^8.14.2"
  }
}
```

### 7.3 Launch Instructions

```bash
cd mvp-browser-demo
npm install
node demo-backend.js
# Open browser to http://localhost:3000
```

---

## 8. Success Criteria

The demo is considered successful if:

1. ✅ All 7 simulated nodes publish heartbeats and show "Ready" status
2. ✅ OHLCV data is published every 5 seconds and visible in timeline
3. ✅ Genome capsules are created and routed to correct embedded nodes
4. ✅ Fitness results are returned and logged by evolution node
5. ✅ UI updates in real-time without page refresh
6. ✅ Message flow matches M1 sequence diagrams
7. ✅ All payloads conform to MVP_INTERFACE_CONTRACTS.md schemas
8. ✅ Demo runs for 5+ minutes without crashes

---

## 9. Future Enhancements (Post-Demo)

- Replace mock OHLCV with real scraper data
- Implement actual L-System genome generation
- Add mutation/selection logic to evolution node
- Real FSM evaluation (not random fitness)
- Persistence layer (SQLite in Node.js)
- Multi-agent population (10+ agents competing)
- 3D Galaxy visualization with clustering

---

## 10. Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| **Phase 1**: UML Diagrams | 2h | Component, Sequence, Deployment diagrams |
| **Phase 2**: Backend Implementation | 4h | MQTT broker, simulators, mock data generators |
| **Phase 3**: Frontend UI | 4h | HTML/CSS layout, MQTT client, real-time updates |
| **Phase 4**: Integration Testing | 2h | End-to-end message flow validation |
| **Phase 5**: Documentation | 1h | README, setup guide, demo script |

**Total Estimated Effort**: 13 hours

---

## 11. Next Steps

1. Create UML diagrams (Component, Sequence, Deployment)
2. Implement backend simulator
3. Build frontend UI
4. Validate against MVP contracts
5. Present demo to stakeholders
6. Use lessons learned to refine M1 implementation plan

---

**Document Status**: Draft for Review  
**Prepared by**: Claude Code  
**Review by**: Manus (Chief Architect)
