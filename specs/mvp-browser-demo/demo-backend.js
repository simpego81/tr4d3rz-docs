/**
 * TR4D3RZ MVP Browser Demo - Backend
 *
 * Simulates the complete M1 distributed system:
 * - MQTT Broker (Aedes)
 * - RPi2 Scraper (OHLCV publisher)
 * - RPi2 Logger (Event logger)
 * - Linux Evolution Node (Genome capsule generator)
 * - ESP8266 Embedded Nodes (Fitness evaluators)
 */

const aedes = require('aedes')();
const net = require('net');
const http = require('http');
const WebSocket = require('ws');
const express = require('express');
const mqtt = require('mqtt');
const path = require('path');

// ============================================================================
// CONFIGURATION
// ============================================================================

const MQTT_PORT = 1883;
const WS_PORT = 9001;
const HTTP_PORT = 3000;

const nodeStartTime = Date.now();
let generation = 0;
const eventLog = [];

// ============================================================================
// MQTT BROKER SETUP
// ============================================================================

const mqttServer = net.createServer(aedes.handle);
const httpServer = http.createServer();

// Start MQTT broker
mqttServer.listen(MQTT_PORT, () => {
  console.log(`[BROKER] MQTT broker listening on port ${MQTT_PORT}`);
});

// Start WebSocket bridge
const wss = new WebSocket.Server({ server: httpServer });
wss.on('connection', (socket) => {
  const stream = WebSocket.createWebSocketStream(socket);
  aedes.handle(stream, {});
});
httpServer.listen(WS_PORT, () => {
  console.log(`[BROKER] WebSocket bridge listening on port ${WS_PORT}`);
});

// Broker event logging
aedes.on('client', (client) => {
  console.log(`[BROKER] Client connected: ${client.id}`);
});

aedes.on('clientDisconnect', (client) => {
  console.log(`[BROKER] Client disconnected: ${client.id}`);
});

aedes.on('publish', (packet, client) => {
  if (client && !packet.topic.startsWith('$SYS')) {
    console.log(`[BROKER] ${client.id} -> ${packet.topic}`);
  }
});

aedes.on('subscribe', (subscriptions, client) => {
  console.log(`[BROKER] ${client.id} subscribed to ${subscriptions.map(s => s.topic).join(', ')}`);
});

// ============================================================================
// MOCK DATA GENERATORS
// ============================================================================

/**
 * Generate mock OHLCV history data
 */
function generateMockOhlcv(isin, bars = 30) {
  const data = [];
  let basePrice = 2.50;
  let ts = Date.now() - (bars * 86400000); // Start N days ago

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

/**
 * Generate mock genome capsule
 */
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
    genome_hash: `sha256:mock-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    fsm: fsm,
    budget: {
      max_ticks: 128,
      max_ms: 1000
    }
  };
}

/**
 * Generate mock fitness result
 */
function generateMockFitnessResult(capsule, nodeId) {
  const fitness = Math.random();
  const status = Math.random() > 0.95 ? "error" : "ok"; // 5% error rate

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

/**
 * Generate node status message
 */
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

// ============================================================================
// SIMULATORS
// ============================================================================

/**
 * Scraper Simulator - Publishes mock OHLCV data
 */
function startScraperSimulator() {
  const client = mqtt.connect('mqtt://localhost:1883', {
    clientId: 'rpi2-scraper'
  });

  client.on('connect', () => {
    console.log('[SCRAPER] Connected to broker');

    // Publish initial status
    client.publish(
      'tr4d3rz/node/rpi2-scraper/status',
      JSON.stringify(generateNodeStatus('rpi2-scraper', 'broker', 'ready')),
      { qos: 0 }
    );

    // Publish OHLCV every 5 seconds
    setInterval(() => {
      const ohlcv = generateMockOhlcv('IT0001233417', 30);
      client.publish(
        'tr4d3rz/data/ohlcv/history/IT0001233417',
        JSON.stringify(ohlcv),
        { qos: 0 }
      );
      console.log('[SCRAPER] Published OHLCV data (30 bars)');
    }, 5000);

    // Publish status heartbeat every 5 seconds
    setInterval(() => {
      client.publish(
        'tr4d3rz/node/rpi2-scraper/status',
        JSON.stringify(generateNodeStatus('rpi2-scraper', 'broker', 'ready')),
        { qos: 0 }
      );
    }, 5000);
  });

  client.on('error', (err) => {
    console.error('[SCRAPER] Error:', err);
  });
}

/**
 * Evolution Simulator - Generates genome capsules
 */
function startEvolutionSimulator() {
  const client = mqtt.connect('mqtt://localhost:1883', {
    clientId: 'linux-evolution-01'
  });

  client.on('connect', () => {
    console.log('[EVOLUTION] Connected to broker');

    // Subscribe to fitness results
    client.subscribe('tr4d3rz/ecosystem/fitness/+', { qos: 1 }, (err) => {
      if (!err) {
        console.log('[EVOLUTION] Subscribed to fitness results');
      }
    });

    // Publish initial status
    client.publish(
      'tr4d3rz/node/linux-evolution-01/status',
      JSON.stringify(generateNodeStatus('linux-evolution-01', 'evolution', 'ready')),
      { qos: 0 }
    );

    // Publish genome capsules every 10 seconds
    setInterval(() => {
      const capsule = generateMockGenomeCapsule('agent-demo-001');
      client.publish(
        'tr4d3rz/node/esp8266-01/capsule/in',
        JSON.stringify(capsule),
        { qos: 1 }
      );
      console.log(`[EVOLUTION] Published capsule gen=${capsule.generation} to esp8266-01`);
    }, 10000);

    // Publish status heartbeat every 5 seconds
    setInterval(() => {
      client.publish(
        'tr4d3rz/node/linux-evolution-01/status',
        JSON.stringify(generateNodeStatus('linux-evolution-01', 'evolution', 'ready')),
        { qos: 0 }
      );
    }, 5000);
  });

  client.on('message', (topic, message) => {
    const payload = JSON.parse(message.toString());
    console.log(`[EVOLUTION] Fitness received: ${payload.agent_id} = ${payload.fitness} (status: ${payload.status})`);
  });

  client.on('error', (err) => {
    console.error('[EVOLUTION] Error:', err);
  });
}

/**
 * Embedded Node Simulator - Evaluates genome capsules
 */
function startEmbeddedSimulator(nodeId) {
  const client = mqtt.connect('mqtt://localhost:1883', {
    clientId: nodeId
  });

  client.on('connect', () => {
    console.log(`[${nodeId.toUpperCase()}] Connected to broker`);

    // Subscribe to capsule topic
    client.subscribe(`tr4d3rz/node/${nodeId}/capsule/in`, { qos: 1 }, (err) => {
      if (!err) {
        console.log(`[${nodeId.toUpperCase()}] Subscribed to capsule/in`);
      }
    });

    // Publish initial status
    client.publish(
      `tr4d3rz/node/${nodeId}/status`,
      JSON.stringify(generateNodeStatus(nodeId, 'embedded', 'ready')),
      { qos: 0 }
    );

    // Publish status heartbeat every 5 seconds
    setInterval(() => {
      client.publish(
        `tr4d3rz/node/${nodeId}/status`,
        JSON.stringify(generateNodeStatus(nodeId, 'embedded', 'ready')),
        { qos: 0 }
      );
    }, 5000);
  });

  client.on('message', (topic, message) => {
    const capsule = JSON.parse(message.toString());
    console.log(`[${nodeId.toUpperCase()}] Received capsule: ${capsule.agent_id} gen=${capsule.generation}`);

    // Simulate evaluation delay (500-2000ms)
    const delay = 500 + Math.random() * 1500;
    setTimeout(() => {
      const fitness = generateMockFitnessResult(capsule, nodeId);
      client.publish(
        `tr4d3rz/ecosystem/fitness/${capsule.agent_id}`,
        JSON.stringify(fitness),
        { qos: 1 }
      );
      console.log(`[${nodeId.toUpperCase()}] Published fitness: ${fitness.fitness} (${fitness.status})`);
    }, delay);
  });

  client.on('error', (err) => {
    console.error(`[${nodeId.toUpperCase()}] Error:`, err);
  });
}

/**
 * Logger Simulator - Logs all MQTT events
 */
function startLoggerSimulator() {
  const client = mqtt.connect('mqtt://localhost:1883', {
    clientId: 'rpi2-logger'
  });

  client.on('connect', () => {
    console.log('[LOGGER] Connected to broker');

    // Subscribe to all topics
    client.subscribe('tr4d3rz/#', { qos: 0 }, (err) => {
      if (!err) {
        console.log('[LOGGER] Subscribed to all topics (tr4d3rz/#)');
      }
    });

    // Publish initial status
    client.publish(
      'tr4d3rz/node/rpi2-logger/status',
      JSON.stringify(generateNodeStatus('rpi2-logger', 'persistence', 'ready')),
      { qos: 0 }
    );

    // Publish status heartbeat every 5 seconds
    setInterval(() => {
      client.publish(
        'tr4d3rz/node/rpi2-logger/status',
        JSON.stringify(generateNodeStatus('rpi2-logger', 'persistence', 'ready')),
        { qos: 0 }
      );
    }, 5000);
  });

  client.on('message', (topic, message) => {
    try {
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
    } catch (e) {
      // Ignore malformed messages
    }
  });

  client.on('error', (err) => {
    console.error('[LOGGER] Error:', err);
  });
}

// ============================================================================
// HTTP SERVER (Frontend)
// ============================================================================

const app = express();

// Serve static files from public/ directory
app.use(express.static(path.join(__dirname, 'public')));

// API endpoint to get event log
app.get('/api/logs', (req, res) => {
  res.json({
    count: eventLog.length,
    events: eventLog.slice(-100) // Return last 100 events
  });
});

// API endpoint to get broker stats
app.get('/api/stats', (req, res) => {
  res.json({
    clients: Object.keys(aedes.clients).length,
    uptime_s: Math.floor((Date.now() - nodeStartTime) / 1000),
    generation: generation
  });
});

app.listen(HTTP_PORT, () => {
  console.log(`[HTTP] Server listening on http://localhost:${HTTP_PORT}`);
  console.log(`[HTTP] Open browser to http://localhost:${HTTP_PORT} to view the demo`);
});

// ============================================================================
// STARTUP SEQUENCE
// ============================================================================

function startAllSimulators() {
  console.log('\n=======================================================');
  console.log('TR4D3RZ MVP Browser Demo - Backend Starting...');
  console.log('=======================================================\n');

  setTimeout(() => {
    console.log('[STARTUP] Starting scraper simulator...');
    startScraperSimulator();
  }, 1000);

  setTimeout(() => {
    console.log('[STARTUP] Starting logger simulator...');
    startLoggerSimulator();
  }, 1500);

  setTimeout(() => {
    console.log('[STARTUP] Starting evolution simulator...');
    startEvolutionSimulator();
  }, 2000);

  setTimeout(() => {
    console.log('[STARTUP] Starting ESP8266-01 simulator...');
    startEmbeddedSimulator('esp8266-01');
  }, 2500);

  setTimeout(() => {
    console.log('[STARTUP] Starting ESP8266-02 simulator...');
    startEmbeddedSimulator('esp8266-02');
  }, 3000);

  setTimeout(() => {
    console.log('\n=======================================================');
    console.log('All simulators started successfully!');
    console.log('Open http://localhost:3000 in your browser');
    console.log('=======================================================\n');
  }, 4000);
}

// Start simulators after broker is ready
setTimeout(startAllSimulators, 2000);

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n[SHUTDOWN] Shutting down gracefully...');
  mqttServer.close();
  httpServer.close();
  process.exit(0);
});
