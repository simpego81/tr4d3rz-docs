# TR4D3RZ MVP Browser Demo - UML Diagrams Index

**Purpose**: Quick reference guide for all UML diagrams  
**Format**: PlantUML (.puml)  
**Rendering**: Use PlantUML extension in VS Code or [plantuml.com](http://www.plantuml.com/plantuml/uml/)

---

## Diagram Catalog

### 1. Component Diagram
**File**: `diagrams/component-diagram.puml`  
**Type**: C4 Component Diagram  
**Purpose**: Shows system components, their responsibilities, and relationships

**Key Elements**:
- Browser Environment (UI, MQTT Client, Chart Engine)
- Node.js Backend (HTTP Server, MQTT Broker, WebSocket Bridge)
- Simulators (Scraper, Evolution, Embedded x2, Logger)
- Event Log (In-Memory Database)

**Use Case**: Understanding the overall architecture and component interactions

---

### 2. Sequence Diagram
**File**: `diagrams/sequence-diagram.puml`  
**Type**: UML Sequence Diagram  
**Purpose**: Illustrates the message flow during a complete evolution cycle

**Key Flows**:
1. Startup Phase (CONNECT, SUBSCRIBE)
2. Heartbeat Phase (Node Status messages)
3. Evolution Cycle (Capsule → Evaluation → Fitness)
4. OHLCV Data Feed (parallel to evolution)

**Use Case**: Validating MQTT message ordering and timing

---

### 3. Deployment Diagram
**File**: `diagrams/deployment-diagram.puml`  
**Type**: C4 Deployment Diagram  
**Purpose**: Shows runtime deployment on localhost with ports and protocols

**Key Elements**:
- Node.js Process (MQTT Broker :1883, WebSocket :9001, HTTP :3000)
- Simulator Threads (setTimeout/setInterval)
- Browser Tab (WebSocket client)
- Network Protocols (MQTT, WebSocket, HTTP)

**Use Case**: Understanding the runtime environment and network topology

---

### 4. Class Diagram
**File**: `diagrams/class-diagram.puml`  
**Type**: UML Class Diagram  
**Purpose**: Defines data models and simulator class structure

**Key Packages**:
1. **MVP Interface Contracts v0.1**:
   - OhlcvBar, OhlcvHistory
   - GenomeCapsule, FsmMvp, Transition, Budget
   - FitnessResult, FitnessStatus
   - NodeStatus, NodeRole, NodeState

2. **Demo Simulators**:
   - MqttBrokerSimulator
   - ScraperSimulator
   - EvolutionSimulator
   - EmbeddedSimulator
   - LoggerSimulator
   - MqttEvent

3. **Frontend UI**:
   - ObservatoryUI
   - ChartEngine
   - TimelineView
   - CapsuleInspector

**Use Case**: Understanding data structures and OOP design

---

### 5. State Diagram
**File**: `diagrams/state-diagram.puml`  
**Type**: UML State Machine Diagram  
**Purpose**: Models node lifecycle states and transitions

**States**:
- Disconnected (initial state)
- Connecting (MQTT handshake)
- Booting (initialization)
- Ready (fully operational)
- Degraded (partial functionality)
- Offline (connection lost)

**Transitions**:
- start() → Connecting
- CONNACK → Booting
- Initialization complete → Ready
- Error detected → Degraded
- Connection lost → Offline
- Reconnect attempt → Connecting

**Use Case**: Understanding node health management and failure recovery

---

### 6. Activity Diagram
**File**: `diagrams/activity-diagram.puml`  
**Type**: UML Activity Diagram  
**Purpose**: End-to-end activity flow for all simulators and browser UI

**Swimlanes**:
1. Backend (broker startup)
2. Scraper Simulator (OHLCV publishing loop)
3. Evolution Simulator (capsule generation loop)
4. ESP8266-01 Simulator (evaluation loop)
5. ESP8266-02 Simulator (evaluation loop)
6. Logger Simulator (event logging loop)
7. Heartbeat Scheduler (status publishing loop)
8. Browser (UI subscription loops)

**Use Case**: Understanding concurrent activities and parallel message flows

---

### 7. Network Topology Diagram
**File**: `diagrams/network-topology.puml`  
**Type**: Custom Network Topology Diagram  
**Purpose**: Visualizes MQTT network, message routing, and QoS levels

**Key Elements**:
- MQTT Broker (Topic Router, WebSocket Bridge, Retained Messages)
- Backend Simulators (Scraper, Evolution, ESP x2, Logger)
- Browser UI (MQTT Client, UI Components, Local State)
- HTTP Server (Static File Server)
- Message Flow Arrows (with QoS and frequency annotations)

**Legend**:
- MQTT Topics (complete list)
- QoS Levels (QoS 0 vs QoS 1)
- Message Rates (5s, 10s, etc.)

**Use Case**: Understanding network communication patterns and message routing

---

## Rendering Instructions

### Option 1: VS Code (Recommended)

1. Install "PlantUML" extension by jebbs
2. Open any `.puml` file
3. Press `Alt+D` (Windows/Linux) or `Option+D` (Mac) to preview
4. Export to PNG/SVG: Right-click → "Export Current Diagram"

### Option 2: Online Renderer

1. Open [plantuml.com](http://www.plantuml.com/plantuml/uml/)
2. Copy-paste the `.puml` file content
3. View rendered diagram
4. Download as PNG/SVG

### Option 3: Command Line

```bash
# Install PlantUML (requires Java)
brew install plantuml  # macOS
apt-get install plantuml  # Ubuntu/Debian

# Render all diagrams
cd tr4d3rz-docs/specs/mvp-browser-demo/diagrams
plantuml *.puml

# Output: PNG files in the same directory
```

### Option 4: Docker

```bash
docker run --rm -v $(pwd):/data plantuml/plantuml:latest *.puml
```

---

## Diagram Usage Matrix

| Diagram | Stakeholder Presentation | Technical Implementation | Architecture Review | Testing/Validation |
|---|---|---|---|---|
| Component | ✅ High-level overview | ✅ Component boundaries | ✅ Responsibility clarity | ❌ |
| Sequence | ✅ Message flow demo | ✅ MQTT topic validation | ✅ Timing analysis | ✅ Integration tests |
| Deployment | ✅ Infrastructure view | ✅ Port/protocol setup | ✅ Scalability review | ❌ |
| Class | ❌ Too detailed | ✅ Data model reference | ✅ OOP design review | ✅ Unit tests |
| State | ✅ Node lifecycle | ✅ State management code | ✅ Resilience analysis | ✅ State transitions |
| Activity | ✅ Concurrent flows | ✅ Parallel processing | ✅ Race condition analysis | ❌ |
| Network Topology | ✅ Network overview | ✅ MQTT setup | ✅ Message routing | ✅ QoS validation |

---

## Exporting Diagrams for Documentation

For inclusion in Markdown docs or presentations:

```bash
# Export all diagrams to PNG
plantuml -tpng diagrams/*.puml

# Export to SVG (better for web)
plantuml -tsvg diagrams/*.puml

# Export to PDF (for print)
plantuml -tpdf diagrams/*.puml
```

Then reference in Markdown:
```markdown
![Component Diagram](diagrams/component-diagram.png)
```

---

## Diagram Maintenance

When updating diagrams:

1. **Edit the `.puml` file** (source of truth)
2. **Re-render** to verify syntax
3. **Update this index** if adding new diagrams
4. **Commit both** `.puml` source and rendered output
5. **Update related specs** if diagram changes reflect design changes

---

## Cross-References

These diagrams illustrate concepts from:

- `MVP_BROWSER_DEMO_SPEC.md` - Overall specification
- `MVP_DEMO_IMPLEMENTATION_PLAN.md` - Implementation phases
- `tr4d3rz-docs/protocols/MVP_INTERFACE_CONTRACTS.md` - Data schemas
- `tr4d3rz-docs/protocols/mqtt-topic-structure.md` - MQTT topics

---

**Last Updated**: 2026-06-05  
**Maintained by**: Claude Code  
**Diagram Count**: 7
