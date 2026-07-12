/**
 * TR4D3RZ Real Distributed Demo - Orchestrator
 *
 * This orchestrates REAL Rust components in a guided end-to-end scenario:
 * 1. Starts local MQTT broker (Aedes)
 * 2. Launches real Rust publisher (publish_capsule)
 * 3. Launches real Rust subscriber (subscribe_fitness)
 * 4. Simulates ESP8266 response (since ESP8266 not yet implemented)
 * 5. Visualizes all MQTT messages in real-time
 */

const aedes = require('aedes')();
const { createServer } = require('net');
const { spawn } = require('child_process');
const express = require('express');
const WebSocket = require('ws');
const mqtt = require('mqtt');
const path = require('path');

const MQTT_PORT = 1883;
const HTTP_PORT = 3200;
const WS_PORT = 3201;

// State
const mqttMessages = [];
const rustProcesses = [];
let wsClients = [];

// ============================================================================
// 1. MQTT Broker (Aedes)
// ============================================================================

const mqttServer = createServer(aedes.handle);

mqttServer.listen(MQTT_PORT, () => {
    console.log('✅ MQTT Broker (Aedes) running on port', MQTT_PORT);
});

// Log all MQTT messages
aedes.on('publish', (packet, client) => {
    if (packet.topic.startsWith('$SYS')) return; // Skip system messages

    const message = {
        timestamp: new Date().toISOString(),
        topic: packet.topic,
        payload: packet.payload.toString('base64'), // CBOR is binary
        payloadPreview: tryDecodeCBOR(packet.payload),
        qos: packet.qos,
        retain: packet.retain,
        clientId: client ? client.id : 'broker'
    };

    mqttMessages.push(message);

    // Broadcast to WebSocket clients
    broadcastToClients({
        type: 'mqtt_message',
        data: message
    });

    console.log(`📨 [${packet.topic}] from ${message.clientId}`);
});

aedes.on('client', (client) => {
    console.log(`🔌 Client connected: ${client.id}`);
    broadcastToClients({
        type: 'client_connected',
        data: { clientId: client.id, timestamp: new Date().toISOString() }
    });
});

aedes.on('clientDisconnect', (client) => {
    console.log(`❌ Client disconnected: ${client.id}`);
    broadcastToClients({
        type: 'client_disconnected',
        data: { clientId: client.id, timestamp: new Date().toISOString() }
    });
});

// ============================================================================
// 2. HTTP API Server
// ============================================================================

const app = express();
app.use(express.static('public'));
app.use(express.json());

// Get all MQTT messages
app.get('/api/messages', (req, res) => {
    res.json({ messages: mqttMessages });
});

// Get scenario status
app.get('/api/status', (req, res) => {
    res.json({
        broker: { running: true, port: MQTT_PORT },
        rustProcesses: rustProcesses.map(p => ({
            name: p.name,
            running: !p.process.killed,
            pid: p.process.pid
        })),
        messagesCount: mqttMessages.length
    });
});

// Start scenario
app.post('/api/scenario/start', async (req, res) => {
    try {
        mqttMessages.length = 0; // Clear previous messages

        // Kill existing processes
        rustProcesses.forEach(p => p.process.kill());
        rustProcesses.length = 0;

        // Wait for cleanup
        await sleep(500);

        console.log('\n🎬 Starting End-to-End Scenario...\n');

        // Step 1: Start subscriber (waits for fitness results)
        const subscriber = launchRustExample('subscribe_fitness', 'Subscriber');
        rustProcesses.push(subscriber);
        await sleep(2000);

        // Step 2: Start publisher (sends genome capsule)
        const publisher = launchRustExample('publish_capsule_fixed', 'Publisher');
        rustProcesses.push(publisher);
        await sleep(2000);

        // Step 3: Simulate ESP8266 response (until M1-T5 is implemented)
        simulateESP8266Response();

        res.json({ success: true, message: 'Scenario started' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Stop scenario
app.post('/api/scenario/stop', (req, res) => {
    rustProcesses.forEach(p => p.process.kill());
    rustProcesses.length = 0;
    res.json({ success: true });
});

app.listen(HTTP_PORT, () => {
    console.log(`✅ HTTP Server running on http://localhost:${HTTP_PORT}`);
});

// ============================================================================
// 3. WebSocket Server (for real-time UI updates)
// ============================================================================

const wss = new WebSocket.Server({ port: WS_PORT });

wss.on('connection', (ws) => {
    wsClients.push(ws);
    console.log('🔗 WebSocket client connected');

    // Send current state
    ws.send(JSON.stringify({
        type: 'initial_state',
        data: {
            messages: mqttMessages,
            status: {
                broker: { running: true, port: MQTT_PORT },
                rustProcesses: rustProcesses.map(p => ({
                    name: p.name,
                    running: !p.process.killed,
                    pid: p.process.pid
                }))
            }
        }
    }));

    ws.on('close', () => {
        wsClients = wsClients.filter(client => client !== ws);
        console.log('❌ WebSocket client disconnected');
    });
});

console.log(`✅ WebSocket Server running on ws://localhost:${WS_PORT}`);

// ============================================================================
// Helper Functions
// ============================================================================

function launchRustExample(exampleName, displayName) {
    const exePath = path.join(__dirname, '../../..', 'tr4d3rz-messaging/target/release/examples', exampleName + '.exe');

    console.log(`🚀 Launching ${displayName}: ${exampleName}`);

    const process = spawn(exePath, [], {
        cwd: path.join(__dirname, '../../..', 'tr4d3rz-messaging'),
        env: { ...process.env, RUST_LOG: 'info' }
    });

    process.stdout.on('data', (data) => {
        const output = data.toString().trim();
        console.log(`[${displayName}] ${output}`);
        broadcastToClients({
            type: 'rust_output',
            data: { name: displayName, output, timestamp: new Date().toISOString() }
        });
    });

    process.stderr.on('data', (data) => {
        const output = data.toString().trim();
        console.error(`[${displayName}] ERROR: ${output}`);
        broadcastToClients({
            type: 'rust_error',
            data: { name: displayName, output, timestamp: new Date().toISOString() }
        });
    });

    process.on('close', (code) => {
        console.log(`[${displayName}] Process exited with code ${code}`);
        broadcastToClients({
            type: 'rust_exit',
            data: { name: displayName, code, timestamp: new Date().toISOString() }
        });
    });

    return { name: displayName, process };
}

function simulateESP8266Response() {
    // This simulates the ESP8266 node response until M1-T5 is implemented
    // It subscribes to capsule topics and publishes fitness results

    setTimeout(() => {
        console.log('🤖 ESP8266 Simulator: Publishing fitness result...');

        const client = mqtt.connect(`mqtt://localhost:${MQTT_PORT}`, {
            clientId: 'esp8266-simulator'
        });

        client.on('connect', () => {
            // Subscribe to capsule input
            client.subscribe('tr4d3rz/node/esp8266-01/capsule/in');

            client.on('message', (topic, message) => {
                console.log(`🤖 ESP8266 Simulator: Received capsule on ${topic}`);

                // Decode CBOR (simplified - would use real decoder)
                // For now, just create a valid fitness result

                const fitnessResult = {
                    v: 1,
                    ts: Date.now(),
                    node: 'esp8266-01',
                    type: 'fitness_result',
                    agent_id: 'agent-demo-001',
                    genome_hash: 'sha256:example-hash',
                    fitness: 0.75 + Math.random() * 0.2,
                    status: 'ok'
                };

                // Encode to CBOR (would use ciborium in real implementation)
                // For demo, publish as JSON
                const fitnessPayload = Buffer.from(JSON.stringify(fitnessResult));

                setTimeout(() => {
                    client.publish('tr4d3rz/ecosystem/fitness/agent-demo-001', fitnessPayload, { qos: 1 });
                    console.log('✅ ESP8266 Simulator: Published fitness result');
                }, 1000);
            });
        });
    }, 3000);
}

function tryDecodeCBOR(buffer) {
    try {
        // Try to decode as UTF-8 first (for debug messages)
        const str = buffer.toString('utf-8');
        if (str.length < 200 && !str.includes('\x00')) {
            return str;
        }

        // Otherwise indicate it's CBOR
        return `[CBOR binary, ${buffer.length} bytes]`;
    } catch {
        return `[Binary data, ${buffer.length} bytes]`;
    }
}

function broadcastToClients(message) {
    const payload = JSON.stringify(message);
    wsClients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(payload);
        }
    });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================================================
// Startup Message
// ============================================================================

console.log('\n' + '='.repeat(70));
console.log('  TR4D3RZ Real Distributed Demo - Orchestrator');
console.log('='.repeat(70));
console.log('');
console.log('📦 Components:');
console.log('  1. MQTT Broker (Aedes) - localhost:1883');
console.log('  2. HTTP API Server - localhost:3200');
console.log('  3. WebSocket Server - localhost:3201');
console.log('');
console.log('🎯 Scenario:');
console.log('  1. Rust Publisher publishes GenomeCapsule (real tr4d3rz-messaging)');
console.log('  2. ESP8266 Simulator receives and evaluates (until M1-T5 ready)');
console.log('  3. ESP8266 publishes FitnessResult');
console.log('  4. Rust Subscriber receives FitnessResult (real tr4d3rz-messaging)');
console.log('');
console.log('🌐 Open browser: http://localhost:3200');
console.log('');
console.log('='.repeat(70) + '\n');
