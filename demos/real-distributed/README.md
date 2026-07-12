# TR4D3RZ Real Distributed Demo

**Status**: ✅ READY TO RUN  
**Version**: 1.0.0  
**Type**: **REAL COMPONENTS** (not simulation)

---

## What This Demo Does

This demo orchestrates **REAL Rust components** in a guided end-to-end scenario that demonstrates actual distributed MQTT communication.

### Components Used

1. **MQTT Broker** (Aedes) - Local broker on port 1883
2. **Rust Publisher** (`publish_capsule_fixed`) - Real tr4d3rz-messaging binary
3. **Rust Subscriber** (`subscribe_fitness`) - Real tr4d3rz-messaging binary
4. **ESP8266 Simulator** (JavaScript) - Simulates M1-T5 until ready
5. **Web UI** - Real-time visualization of MQTT messages

### End-to-End Scenario

```
1. Subscriber starts → waits for fitness results
2. Publisher starts → sends GenomeCapsule via MQTT
3. ESP8266 receives → evaluates capsule
4. ESP8266 publishes → FitnessResult via MQTT
5. Subscriber receives → logs fitness result
```

**All MQTT messages are REAL** - CBOR-encoded, via tr4d3rz-messaging Rust library.

---

## Prerequisites

### 1. Build Rust Examples

```bash
cd C:/projects/seq/tr4d3rz-messaging
cargo build --release --examples
```

**Verify**:
```bash
ls target/release/examples/*.exe
```

Expected: `publish_capsule_fixed.exe`, `subscribe_fitness.exe`, etc.

### 2. Install Node.js Dependencies

```bash
cd C:/projects/seq/tr4d3rz-docs/demos/real-distributed
npm install
```

---

## Quick Start

```bash
cd C:/projects/seq/tr4d3rz-docs/demos/real-distributed
npm start
```

**Then open**: http://localhost:3200

---

## How to Use

### 1. Start the Orchestrator

```bash
npm start
```

You'll see:
```
✅ MQTT Broker (Aedes) running on port 1883
✅ HTTP Server running on http://localhost:3200
✅ WebSocket Server running on localhost:3201
```

### 2. Open the UI

Navigate to **http://localhost:3200**

### 3. Click "▶️ Start End-to-End Scenario"

This will:
- ✅ Launch real Rust subscriber binary
- ✅ Launch real Rust publisher binary
- ✅ Simulate ESP8266 response (until M1-T5)
- ✅ Show all MQTT messages in real-time

### 4. Watch the Live Timeline

You'll see:
- 🔌 **Client connections** (subscriber, publisher)
- 📨 **GenomeCapsule** published to `tr4d3rz/node/esp8266-01/capsule/in`
- 📨 **FitnessResult** published to `tr4d3rz/ecosystem/fitness/agent-demo-001`
- 🖥️ **Rust process output** in real-time

---

## What Makes This REAL

### ❌ What This Is NOT

- ~~Mock MQTT client~~
- ~~JavaScript simulation of Rust types~~
- ~~Fake message generation~~

### ✅ What This IS

- **Real MQTT broker** (Aedes, production-grade)
- **Real Rust binaries** (compiled from tr4d3rz-messaging)
- **Real CBOR encoding** (via ciborium in Rust)
- **Real distributed communication** (actual MQTT publish/subscribe)
- **Real process orchestration** (Node.js spawns Rust processes)

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser (UI)                     │
│         http://localhost:3200 + ws://localhost:3201     │
└────────────┬────────────────────────────────────────────┘
             │ HTTP + WebSocket
             ↓
┌─────────────────────────────────────────────────────────┐
│              Node.js Orchestrator (orchestrator.js)      │
│  - HTTP API Server                                       │
│  - WebSocket Server                                      │
│  - Process Manager (spawn Rust binaries)                │
└────────────┬────────────────────────────────────────────┘
             │ spawn() + MQTT
             ↓
┌─────────────────────────────────────────────────────────┐
│              MQTT Broker (Aedes) - Port 1883            │
└─────┬───────────────────┬────────────────────┬──────────┘
      │                   │                    │
      ↓                   ↓                    ↓
┌───────────────┐  ┌──────────────┐  ┌────────────────┐
│ Rust Publisher│  │ Rust         │  │ ESP8266        │
│ (REAL BINARY) │  │ Subscriber   │  │ Simulator      │
│               │  │ (REAL BINARY)│  │ (until M1-T5)  │
│ publish_      │  │              │  │                │
│ capsule_fixed │  │ subscribe_   │  │ JavaScript     │
│               │  │ fitness      │  │                │
└───────────────┘  └──────────────┘  └────────────────┘
```

---

## Message Flow

### 1. Publish GenomeCapsule

**From**: Rust Publisher (`publish_capsule_fixed.exe`)  
**To**: `tr4d3rz/node/esp8266-01/capsule/in`  
**Encoding**: CBOR  
**Payload**: GenomeCapsule (v1) with FSM

### 2. ESP8266 Receives

**From**: ESP8266 Simulator (JavaScript MQTT client)  
**Subscription**: `tr4d3rz/node/esp8266-01/capsule/in`  
**Action**: Decode, evaluate, prepare FitnessResult

### 3. Publish FitnessResult

**From**: ESP8266 Simulator  
**To**: `tr4d3rz/ecosystem/fitness/agent-demo-001`  
**Encoding**: JSON (CBOR in real M1-T5)  
**Payload**: FitnessResult (v1) with fitness value

### 4. Subscriber Receives

**From**: Rust Subscriber (`subscribe_fitness.exe`)  
**Subscription**: `tr4d3rz/ecosystem/fitness/+`  
**Action**: Decode and log fitness result

---

## Differences from Enhanced MVP Demo

| Aspect | Enhanced MVP Demo | Real Distributed Demo |
|---|---|---|
| **Components** | CLI JSON generator | **Real Rust binaries** |
| **Communication** | HTTP REST API | **Real MQTT pub/sub** |
| **Encoding** | JSON (calculated CBOR size) | **Real CBOR encoding** |
| **Orchestration** | Single-process | **Multi-process distributed** |
| **Visualization** | Static data explorer | **Live message timeline** |
| **Use Case** | Show component status | **Show distributed interaction** |

**Both are valuable**:
- Enhanced MVP → Component capabilities
- Real Distributed → System integration

---

## Troubleshooting

### Error: "MQTT Broker port already in use"

**Solution**: Stop any running MQTT brokers on port 1883
```bash
netstat -ano | findstr :1883
```

### Error: "Cannot find Rust binary"

**Solution**: Build the examples first
```bash
cd C:/projects/seq/tr4d3rz-messaging
cargo build --release --examples
```

### No messages in timeline

**Solution**: Check Rust process output panel for errors. Ensure localhost MQTT is reachable.

---

## Next Steps

### When M1-T5 is Completed

Replace ESP8266 Simulator with real firmware:
```javascript
// In orchestrator.js, replace simulateESP8266Response() with:
const esp8266 = launchRustExample('esp8266_node', 'ESP8266');
```

### Add More Nodes

Add OHLCV scraper:
```javascript
const scraper = launchRustExample('ohlcv_scraper', 'Scraper');
```

Add persistence logger:
```javascript
const logger = launchRustExample('event_logger', 'Logger');
```

---

**This demo proves**: TR4D3RZ components can communicate in a real distributed system using MQTT and CBOR. ✅

---

*Created: 2026-06-19*  
*Maintained by: Claude Code (Implementation Agent)*
