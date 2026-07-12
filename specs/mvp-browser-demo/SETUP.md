# TR4D3RZ MVP Browser Demo - Setup Instructions

**Status**: Implementation Complete  
**Version**: 0.1.0  
**Date**: 2026-06-05

---

## Quick Start

```bash
# 1. Navigate to the demo directory
cd C:\projects\seq\tr4d3rz-docs\specs\mvp-browser-demo

# 2. Install dependencies
npm install

# 3. Start the demo
npm start

# 4. Open your browser
# Navigate to: http://localhost:3000
```

That's it! The demo should now be running.

---

## Prerequisites

### Required Software

- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **Modern Web Browser**: Chrome, Firefox, or Edge (latest version)

### Check Your Versions

```bash
node --version  # Should be v18.0.0 or higher
npm --version   # Should be v9.0.0 or higher
```

### Installing Node.js (if needed)

**Windows**:
- Download from [nodejs.org](https://nodejs.org/)
- Run the installer
- Restart your terminal

**macOS** (using Homebrew):
```bash
brew install node
```

**Linux** (Ubuntu/Debian):
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## Installation

### Step 1: Navigate to Demo Directory

```bash
cd C:\projects\seq\tr4d3rz-docs\specs\mvp-browser-demo
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install:
- `aedes` - MQTT broker
- `express` - HTTP server
- `mqtt` - MQTT client library
- `ws` - WebSocket library

Expected output:
```
added 50 packages, and audited 51 packages in 3s
```

### Step 3: Verify Installation

Check that `node_modules/` directory was created:
```bash
ls node_modules  # Should show aedes, express, mqtt, ws
```

---

## Running the Demo

### Start the Backend

```bash
npm start
```

Expected console output:
```
=======================================================
TR4D3RZ MVP Browser Demo - Backend Starting...
=======================================================

[BROKER] MQTT broker listening on port 1883
[BROKER] WebSocket bridge listening on port 9001
[HTTP] Server listening on http://localhost:3000
[HTTP] Open browser to http://localhost:3000 to view the demo

[STARTUP] Starting scraper simulator...
[STARTUP] Starting logger simulator...
[STARTUP] Starting evolution simulator...
[STARTUP] Starting ESP8266-01 simulator...
[STARTUP] Starting ESP8266-02 simulator...

[SCRAPER] Connected to broker
[LOGGER] Connected to broker
[EVOLUTION] Connected to broker
[ESP8266-01] Connected to broker
[ESP8266-02] Connected to broker

=======================================================
All simulators started successfully!
Open http://localhost:3000 in your browser
=======================================================
```

### Open the UI

1. Open your web browser
2. Navigate to: **http://localhost:3000**
3. You should see the TR4D3RZ MVP Demo interface

---

## What You Should See

### In the Browser

**Header**:
- Title: "🧬 TR4D3RZ MVP Browser Demo"
- Connection status (green dot = connected)

**Left Panel - Node Status**:
- 7 nodes should appear
- After a few seconds, all should show state: "ready" (green)

**Center Panel - System Topology**:
- SVG diagram showing node connections

**Center Bottom - Event Timeline**:
- Live scrolling log of MQTT messages
- Should start filling with events within 5 seconds

**Right Panel - Fitness Chart**:
- Line chart showing fitness over time
- Should update every ~10 seconds after first capsule/fitness pair

**Footer**:
- Connected Nodes: Should show "7/7" when all nodes are ready
- Messages: Counter incrementing as events are received

### In the Console (Backend)

You should see periodic log messages:
```
[SCRAPER] Published OHLCV data (30 bars)
[EVOLUTION] Published capsule gen=0 to esp8266-01
[ESP8266-01] Received capsule: agent-demo-001 gen=0
[ESP8266-01] Published fitness: 0.7234 (ok)
[EVOLUTION] Fitness received: agent-demo-001 = 0.7234 (status: ok)
```

---

## Stopping the Demo

Press `Ctrl+C` in the terminal where the backend is running.

Expected output:
```
[SHUTDOWN] Shutting down gracefully...
```

---

## Troubleshooting

### Problem: "npm: command not found"

**Solution**: Install Node.js (see Prerequisites section above)

---

### Problem: Port 1883, 9001, or 3000 already in use

**Error**:
```
Error: listen EADDRINUSE: address already in use :::1883
```

**Solution**:

**Option 1**: Stop the conflicting process
```bash
# Windows
netstat -ano | findstr :1883
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :1883
kill -9 <PID>
```

**Option 2**: Change the ports in `demo-backend.js`
```javascript
const MQTT_PORT = 1884;  // Change from 1883
const WS_PORT = 9002;    // Change from 9001
const HTTP_PORT = 3001;  // Change from 3000
```

Also update `public/app.js`:
```javascript
mqttClient = mqtt.connect('ws://localhost:9002', { // Update WebSocket port
```

---

### Problem: Browser shows "Disconnected"

**Symptoms**:
- Red dot in header
- Status text: "Disconnected"
- No events in timeline

**Solution**:

1. **Check backend is running**:
   ```bash
   # Should show "Server listening on http://localhost:3000"
   ```

2. **Check browser console for errors**:
   - Press F12 in browser
   - Check Console tab for WebSocket errors

3. **Verify WebSocket port**:
   - Backend should show: "WebSocket bridge listening on port 9001"
   - Browser connects to: `ws://localhost:9001`

4. **Try refreshing the page** (F5)

---

### Problem: No MQTT messages appearing

**Symptoms**:
- All nodes show "ready"
- But timeline is empty
- Message count stays at 0

**Solution**:

1. **Check backend console** - Should see periodic messages like:
   ```
   [SCRAPER] Published OHLCV data
   [EVOLUTION] Published capsule gen=X
   ```

2. **Check browser subscriptions** - Browser console should show:
   ```
   Subscribed to tr4d3rz/node/+/status
   Subscribed to tr4d3rz/ecosystem/fitness/+
   ...
   ```

3. **Restart the backend** (Ctrl+C, then `npm start`)

---

### Problem: Fitness chart not updating

**Symptoms**:
- Timeline shows fitness events
- But chart remains empty

**Solution**:

1. **Wait for at least one full cycle** (~10-15 seconds after startup)
2. **Check browser console for JavaScript errors** (F12 → Console)
3. **Verify canvas element exists**: Open DevTools → Elements, search for `<canvas id="fitness-chart">`

---

### Problem: Dependencies failed to install

**Error**:
```
npm ERR! code ENOENT
npm ERR! syscall open
```

**Solution**:

1. **Delete `node_modules` and `package-lock.json`**:
   ```bash
   rm -rf node_modules package-lock.json  # macOS/Linux
   rmdir /s node_modules & del package-lock.json  # Windows
   ```

2. **Clear npm cache**:
   ```bash
   npm cache clean --force
   ```

3. **Reinstall**:
   ```bash
   npm install
   ```

---

## Testing the Demo

### Manual Test Checklist

Run through this checklist to validate the demo:

- [ ] Backend starts without errors
- [ ] All 7 nodes connect to broker (check console logs)
- [ ] Browser loads at http://localhost:3000
- [ ] Connection status shows green dot "Connected"
- [ ] All 7 nodes show state "ready" (green badges)
- [ ] Connected Nodes footer shows "7/7"
- [ ] Event Timeline starts populating within 5 seconds
- [ ] OHLCV events appear every ~5 seconds
- [ ] Genome capsule events appear every ~10 seconds
- [ ] Fitness result events appear 0.5-2s after capsule
- [ ] Genome Capsule Inspector shows JSON when capsule arrives
- [ ] Fitness chart updates and shows line graph
- [ ] Chart stats update (Generation, Best Fitness, Avg Fitness)
- [ ] Timeline auto-scrolls to bottom
- [ ] "Clear" button clears timeline
- [ ] Demo runs for 5+ minutes without crashes
- [ ] All payloads match MVP_INTERFACE_CONTRACTS.md schemas

---

## Architecture Recap

### Ports

| Service | Port | Protocol | Purpose |
|---|---|---|---|
| MQTT Broker | 1883 | MQTT/TCP | Native MQTT connections |
| WebSocket Bridge | 9001 | WebSocket | Browser MQTT connections |
| HTTP Server | 3000 | HTTP | Serves frontend static files |

### Nodes

| Node ID | Simulates | Connection |
|---|---|---|
| `rpi2-broker` | Raspberry Pi 2 (Broker) | N/A (is the broker) |
| `rpi2-scraper` | Raspberry Pi 2 (Scraper) | MQTT TCP :1883 |
| `rpi2-logger` | Raspberry Pi 2 (Logger) | MQTT TCP :1883 |
| `linux-evolution-01` | Linux PC (Evolution) | MQTT TCP :1883 |
| `esp8266-01` | ESP8266 (Embedded) | MQTT TCP :1883 |
| `esp8266-02` | ESP8266 (Embedded) | MQTT TCP :1883 |
| `browser-observatory` | Browser (Observatory) | WebSocket :9001 |

### Message Flow

```
Every 5s:  [Scraper] --OHLCV--> [Broker] --> [Logger, Browser]
Every 10s: [Evolution] --Capsule--> [Broker] --> [ESP8266-01, Logger, Browser]
Every 0.5-2s: [ESP8266-01] --Fitness--> [Broker] --> [Evolution, Logger, Browser]
Every 5s:  [All Nodes] --Status--> [Broker] --> [Logger, Browser]
```

---

## Next Steps

After successfully running the demo:

1. **Observe the System**:
   - Watch the message flow for 5+ minutes
   - Note the timing and patterns

2. **Validate Against Specs**:
   - Compare message payloads to `MVP_INTERFACE_CONTRACTS.md`
   - Verify MQTT topics match `mqtt-topic-structure.md`

3. **Experiment**:
   - Try clearing the timeline
   - Watch the fitness chart evolve
   - Inspect genome capsules in the JSON viewer

4. **Provide Feedback**:
   - Does the UI make sense?
   - Are MQTT topics well-structured?
   - Are payload schemas practical?

5. **Prepare for M1 Implementation**:
   - Use lessons learned from this demo
   - Proceed with M1-T2 (tr4d3rz-messaging) implementation

---

## Support

**Issues**: Report to `tr4d3rz-docs/COMMUNICATION/`  
**Documentation**: See `README.md` and `MVP_BROWSER_DEMO_SPEC.md`  
**Architecture**: Review UML diagrams in `diagrams/`

---

**Setup Instructions Version**: 1.0  
**Last Updated**: 2026-06-05  
**Prepared by**: Claude Code
