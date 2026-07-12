# TR4D3RZ MVP Browser Demo - Implementation Plan

**Status**: Ready for Implementation  
**Author**: Claude Code  
**Date**: 2026-06-05  
**Estimated Effort**: 13 hours  
**Target Completion**: 2 days

---

## 1. Overview

This document provides a step-by-step implementation plan for the TR4D3RZ MVP Browser Demo, a simulation environment that validates the M1 architectural design before real hardware implementation.

---

## 2. Prerequisites

### 2.1 Development Environment

- Node.js v18+ installed
- npm v9+ installed
- Modern web browser (Chrome, Firefox, or Edge)
- Text editor (VS Code recommended)
- Git (for version control)

### 2.2 Required Knowledge

- JavaScript (ES6+)
- Node.js event-driven programming
- MQTT protocol basics
- HTML/CSS fundamentals
- Async/await patterns

---

## 3. Phase-by-Phase Implementation

### Phase 1: Project Setup (30 minutes)

**Objective**: Create project structure and install dependencies

**Tasks**:

1. Create project directory structure
```bash
mkdir -p mvp-browser-demo/public
cd mvp-browser-demo
```

2. Initialize npm project
```bash
npm init -y
```

3. Install dependencies
```bash
npm install aedes express mqtt ws
```

4. Create `package.json` scripts
```json
{
  "scripts": {
    "start": "node demo-backend.js",
    "dev": "node --watch demo-backend.js"
  }
}
```

5. Create `.gitignore`
```
node_modules/
*.log
.DS_Store
```

**Deliverable**: ✅ Project scaffold with dependencies installed

---

### Phase 2: Backend MQTT Broker (2 hours)

**Objective**: Implement Aedes MQTT broker with WebSocket support

**File**: `demo-backend.js` (Part 1)

**Tasks**:

1. Import dependencies
```javascript
const aedes = require('aedes')();
const server = require('net').createServer(aedes.handle);
const httpServer = require('http').createServer();
const ws = require('websocket-stream');
const express = require('express');
const mqtt = require('mqtt');
```

2. Start MQTT broker on port 1883
```javascript
const MQTT_PORT = 1883;
server.listen(MQTT_PORT, () => {
  console.log(`MQTT broker listening on port ${MQTT_PORT}`);
});
```

3. Add WebSocket bridge on port 9001
```javascript
const WS_PORT = 9001;
ws.createServer({ server: httpServer }, aedes.handle);
httpServer.listen(WS_PORT, () => {
  console.log(`WebSocket bridge listening on port ${WS_PORT}`);
});
```

4. Add broker event logging
```javascript
aedes.on('client', (client) => {
  console.log(`[BROKER] Client connected: ${client.id}`);
});

aedes.on('clientDisconnect', (client) => {
  console.log(`[BROKER] Client disconnected: ${client.id}`);
});

aedes.on('publish', (packet, client) => {
  if (client) {
    console.log(`[BROKER] ${client.id} -> ${packet.topic}`);
  }
});
```

5. Test broker connectivity
```bash
# Install mosquitto_pub for testing
mosquitto_pub -h localhost -t test/topic -m "Hello"
```

**Deliverable**: ✅ Working MQTT broker with WebSocket support

---

### Phase 3: Mock Data Generators (1.5 hours)

**Objective**: Create functions to generate realistic mock data

**File**: `demo-backend.js` (Part 2)

**Tasks**:

1. Implement OHLCV generator
```javascript
function generateMockOhlcv(isin, bars = 30) {
  const data = [];
  let basePrice = 2.50;
  let ts = Date.now() - (bars * 86400000);
  
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
    
    basePrice = c;
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

2. Implement Genome Capsule generator
```javascript
let generation = 0;

function generateMockGenomeCapsule(agentId, targetNode) {
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
    genome_hash: `sha256:mock-${Date.now()}-${Math.random()}`,
    fsm: fsm,
    budget: {
      max_ticks: 128,
      max_ms: 1000
    }
  };
}
```

3. Implement Fitness Result generator
```javascript
function generateMockFitnessResult(capsule, nodeId) {
  const fitness = Math.random();
  const status = Math.random() > 0.95 ? "error" : "ok";
  
  return {
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
}
```

4. Implement Node Status generator
```javascript
const nodeStartTime = Date.now();

function generateNodeStatus(nodeId, role, state = "ready") {
  return {
    v: 1,
    ts: Date.now(),
    node: nodeId,
    type: "node_status",
    role: role,
    state: state,
    uptime_s: Math.floor((Date.now() - nodeStartTime) / 1000)
  };
}
```

**Deliverable**: ✅ Mock data generators tested and validated

---

### Phase 4: Backend Simulators (3 hours)

**Objective**: Implement all node simulators

**File**: `demo-backend.js` (Part 3)

**Tasks**:

1. Scraper Simulator
```javascript
function startScraperSimulator() {
  const client = mqtt.connect('mqtt://localhost:1883', {
    clientId: 'rpi2-scraper'
  });
  
  client.on('connect', () => {
    console.log('[SCRAPER] Connected');
    
    // Publish initial status
    client.publish(
      'tr4d3rz/node/rpi2-scraper/status',
      JSON.stringify(generateNodeStatus('rpi2-scraper', 'broker', 'ready'))
    );
    
    // Publish OHLCV every 5 seconds
    setInterval(() => {
      const ohlcv = generateMockOhlcv('IT0001233417', 30);
      client.publish(
        'tr4d3rz/data/ohlcv/history/IT0001233417',
        JSON.stringify(ohlcv),
        { qos: 0 }
      );
      console.log('[SCRAPER] Published OHLCV data');
    }, 5000);
    
    // Publish status heartbeat every 5 seconds
    setInterval(() => {
      client.publish(
        'tr4d3rz/node/rpi2-scraper/status',
        JSON.stringify(generateNodeStatus('rpi2-scraper', 'broker', 'ready'))
      );
    }, 5000);
  });
}
```

2. Evolution Simulator
```javascript
function startEvolutionSimulator() {
  const client = mqtt.connect('mqtt://localhost:1883', {
    clientId: 'linux-evolution-01'
  });
  
  client.on('connect', () => {
    console.log('[EVOLUTION] Connected');
    
    // Subscribe to fitness results
    client.subscribe('tr4d3rz/ecosystem/fitness/+', (err) => {
      if (!err) {
        console.log('[EVOLUTION] Subscribed to fitness results');
      }
    });
    
    // Publish genome capsules every 10 seconds
    setInterval(() => {
      const capsule = generateMockGenomeCapsule('agent-demo-001', 'esp8266-01');
      client.publish(
        'tr4d3rz/node/esp8266-01/capsule/in',
        JSON.stringify(capsule),
        { qos: 1 }
      );
      console.log(`[EVOLUTION] Published capsule gen=${capsule.generation}`);
    }, 10000);
  });
  
  client.on('message', (topic, message) => {
    const payload = JSON.parse(message.toString());
    console.log(`[EVOLUTION] Fitness received: ${payload.agent_id} = ${payload.fitness}`);
  });
}
```

3. Embedded Node Simulators (ESP8266-01 and ESP8266-02)
```javascript
function startEmbeddedSimulator(nodeId) {
  const client = mqtt.connect('mqtt://localhost:1883', {
    clientId: nodeId
  });
  
  client.on('connect', () => {
    console.log(`[${nodeId}] Connected`);
    
    // Subscribe to capsule topic
    client.subscribe(`tr4d3rz/node/${nodeId}/capsule/in`, (err) => {
      if (!err) {
        console.log(`[${nodeId}] Subscribed to capsule/in`);
      }
    });
  });
  
  client.on('message', (topic, message) => {
    const capsule = JSON.parse(message.toString());
    console.log(`[${nodeId}] Received capsule: ${capsule.agent_id}`);
    
    // Simulate evaluation delay
    const delay = 500 + Math.random() * 1500;
    setTimeout(() => {
      const fitness = generateMockFitnessResult(capsule, nodeId);
      client.publish(
        `tr4d3rz/ecosystem/fitness/${capsule.agent_id}`,
        JSON.stringify(fitness),
        { qos: 1 }
      );
      console.log(`[${nodeId}] Published fitness: ${fitness.fitness}`);
    }, delay);
  });
}
```

4. Logger Simulator
```javascript
const eventLog = [];

function startLoggerSimulator() {
  const client = mqtt.connect('mqtt://localhost:1883', {
    clientId: 'rpi2-logger'
  });
  
  client.on('connect', () => {
    console.log('[LOGGER] Connected');
    client.subscribe('tr4d3rz/#', (err) => {
      if (!err) {
        console.log('[LOGGER] Subscribed to all topics');
      }
    });
  });
  
  client.on('message', (topic, message) => {
    const event = {
      timestamp: Date.now(),
      topic: topic,
      payload: JSON.parse(message.toString())
    };
    eventLog.push(event);
    
    // Keep only last 1000 events
    if (eventLog.length > 1000) {
      eventLog.shift();
    }
  });
}
```

5. Main startup function
```javascript
function startAllSimulators() {
  console.log('Starting TR4D3RZ MVP Demo Backend...');
  
  setTimeout(() => startScraperSimulator(), 1000);
  setTimeout(() => startEvolutionSimulator(), 2000);
  setTimeout(() => startEmbeddedSimulator('esp8266-01'), 2500);
  setTimeout(() => startEmbeddedSimulator('esp8266-02'), 3000);
  setTimeout(() => startLoggerSimulator(), 1500);
  
  console.log('All simulators started');
}

// Start simulators after broker is ready
setTimeout(startAllSimulators, 2000);
```

**Deliverable**: ✅ All backend simulators running and communicating via MQTT

---

### Phase 5: HTTP Server for Frontend (30 minutes)

**Objective**: Serve static files for the browser UI

**File**: `demo-backend.js` (Part 4)

**Tasks**:

1. Add Express server
```javascript
const app = express();
const HTTP_PORT = 3000;

app.use(express.static('public'));

app.get('/api/logs', (req, res) => {
  res.json(eventLog);
});

app.listen(HTTP_PORT, () => {
  console.log(`HTTP server listening on http://localhost:${HTTP_PORT}`);
});
```

**Deliverable**: ✅ HTTP server serving static files

---

### Phase 6: Frontend HTML Structure (1.5 hours)

**Objective**: Create responsive UI layout

**File**: `public/index.html`

**Tasks**:

1. Create HTML structure (see full implementation in spec)
2. Include MQTT.js from CDN
3. Add Chart.js for fitness visualization
4. Create responsive grid layout

**Deliverable**: ✅ Complete HTML structure with all UI panels

---

### Phase 7: Frontend CSS Styling (1 hour)

**Objective**: Style the UI with modern CSS

**File**: `public/style.css`

**Tasks**:

1. Implement CSS grid layout
2. Style node status indicators with color coding
3. Create scrolling timeline with auto-scroll
4. Style JSON inspector with syntax highlighting
5. Responsive design for mobile/tablet

**Deliverable**: ✅ Polished, professional-looking UI

---

### Phase 8: Frontend JavaScript Logic (3 hours)

**Objective**: Implement MQTT client and UI updates

**File**: `public/app.js`

**Tasks**:

1. Connect MQTT.js client to WebSocket
```javascript
const client = mqtt.connect('ws://localhost:9001');

client.on('connect', () => {
  console.log('Observatory connected to MQTT broker');
  
  // Subscribe to all relevant topics
  client.subscribe('tr4d3rz/node/+/status');
  client.subscribe('tr4d3rz/ecosystem/fitness/+');
  client.subscribe('tr4d3rz/node/+/capsule/in');
  client.subscribe('tr4d3rz/data/ohlcv/#');
});
```

2. Implement node status update handler
```javascript
function updateNodeStatus(status) {
  const nodeId = status.node;
  const elem = document.getElementById(`node-${nodeId}`);
  if (elem) {
    elem.className = `node-status ${status.state}`;
    elem.querySelector('.state').textContent = status.state;
    elem.querySelector('.uptime').textContent = `${status.uptime_s}s`;
  }
}
```

3. Implement fitness chart updater
```javascript
const fitnessData = [];

function updateFitnessChart(fitness) {
  fitnessData.push({
    generation: generation,
    fitness: fitness.fitness
  });
  
  // Re-render chart (using Chart.js or vanilla Canvas)
  renderChart(fitnessData);
}
```

4. Implement timeline append
```javascript
function appendTimeline(topic, payload) {
  const timeline = document.getElementById('timeline');
  const timestamp = new Date().toLocaleTimeString();
  
  const entry = document.createElement('div');
  entry.className = 'timeline-entry';
  entry.innerHTML = `
    <span class="time">[${timestamp}]</span>
    <span class="topic">${topic}</span>
    <span class="summary">${summarizePayload(payload)}</span>
  `;
  
  timeline.appendChild(entry);
  timeline.scrollTop = timeline.scrollHeight; // Auto-scroll
}
```

5. Wire up message handlers
```javascript
client.on('message', (topic, message) => {
  const payload = JSON.parse(message.toString());
  
  if (topic.includes('/status')) {
    updateNodeStatus(payload);
  } else if (topic.includes('/fitness/')) {
    updateFitnessChart(payload);
    appendTimeline(topic, payload);
  } else if (topic.includes('/capsule/in')) {
    displayCapsule(payload);
    appendTimeline(topic, payload);
  } else if (topic.includes('/ohlcv/')) {
    appendTimeline(topic, payload);
  }
});
```

**Deliverable**: ✅ Fully functional real-time UI

---

### Phase 9: Integration Testing (2 hours)

**Objective**: Validate end-to-end message flow

**Test Cases**:

1. ✅ All 7 nodes connect and show "Ready" status
2. ✅ OHLCV published every 5 seconds
3. ✅ Genome capsules routed to ESP8266-01
4. ✅ Fitness results returned to evolution node
5. ✅ UI updates in real-time
6. ✅ Timeline scrolls automatically
7. ✅ Capsule inspector displays correct JSON
8. ✅ Fitness chart updates with each result
9. ✅ System runs for 5+ minutes without crashes
10. ✅ Browser reconnects after WebSocket disconnect

**Deliverable**: ✅ Fully tested demo ready for presentation

---

### Phase 10: Documentation (1 hour)

**Objective**: Create setup and demo guide

**File**: `mvp-browser-demo/README.md`

**Contents**:
- Installation instructions
- Running the demo
- Understanding the UI
- Architecture overview
- Troubleshooting

**Deliverable**: ✅ Complete documentation

---

## 4. Timeline Summary

| Phase | Duration | Cumulative |
|---|---|---|
| 1. Project Setup | 0.5h | 0.5h |
| 2. MQTT Broker | 2h | 2.5h |
| 3. Mock Data Generators | 1.5h | 4h |
| 4. Backend Simulators | 3h | 7h |
| 5. HTTP Server | 0.5h | 7.5h |
| 6. Frontend HTML | 1.5h | 9h |
| 7. Frontend CSS | 1h | 10h |
| 8. Frontend JavaScript | 3h | 13h |
| 9. Integration Testing | 2h | 15h |
| 10. Documentation | 1h | 16h |

**Total**: 16 hours (2 days of focused work)

---

## 5. Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| Node connectivity | 100% (7/7 nodes) | All nodes show "Ready" status |
| Message throughput | 2-5 msg/sec | Timeline shows consistent updates |
| UI responsiveness | <100ms | Updates appear immediately |
| Demo stability | 5+ minutes | No crashes or disconnects |
| Message conformance | 100% | All payloads match MVP contracts |

---

## 6. Next Steps After Demo

1. Present demo to stakeholders
2. Gather feedback on UI/UX
3. Validate protocol contracts are practical
4. Identify gaps in specifications
5. Use lessons learned to refine M1 implementation
6. Begin real hardware implementation (M1-T2)

---

**Plan Status**: ✅ Ready for Implementation  
**Prepared by**: Claude Code  
**Approval**: Pending (Manus)
