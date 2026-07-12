/**
 * TR4D3RZ MVP Browser Demo - Frontend Application
 */

// ============================================================================
// GLOBAL STATE
// ============================================================================

let mqttClient = null;
let browserStartTime = Date.now();
let messageCount = 0;
let connectedNodes = new Set();
let fitnessHistory = [];
let currentGeneration = 0;

// ============================================================================
// MQTT CONNECTION
// ============================================================================

function connectToMqtt() {
    console.log('Connecting to MQTT broker via WebSocket...');

    mqttClient = mqtt.connect('ws://localhost:9001', {
        clientId: 'browser-observatory-' + Math.random().toString(16).substr(2, 8)
    });

    mqttClient.on('connect', () => {
        console.log('Connected to MQTT broker');
        updateConnectionStatus(true);
        updateBrowserNodeStatus('ready');

        // Subscribe to all relevant topics
        const topics = [
            'tr4d3rz/node/+/status',
            'tr4d3rz/ecosystem/fitness/+',
            'tr4d3rz/node/+/capsule/in',
            'tr4d3rz/data/ohlcv/#'
        ];

        topics.forEach(topic => {
            mqttClient.subscribe(topic, { qos: 1 }, (err) => {
                if (!err) {
                    console.log(`Subscribed to ${topic}`);
                }
            });
        });
    });

    mqttClient.on('message', (topic, message) => {
        handleMqttMessage(topic, message);
    });

    mqttClient.on('error', (err) => {
        console.error('MQTT error:', err);
        updateConnectionStatus(false);
        updateBrowserNodeStatus('degraded');
    });

    mqttClient.on('close', () => {
        console.log('MQTT connection closed');
        updateConnectionStatus(false);
        updateBrowserNodeStatus('offline');
    });

    mqttClient.on('offline', () => {
        console.log('MQTT client offline');
        updateConnectionStatus(false);
        updateBrowserNodeStatus('offline');
    });

    mqttClient.on('reconnect', () => {
        console.log('Attempting to reconnect...');
        updateBrowserNodeStatus('booting');
    });
}

// ============================================================================
// MESSAGE HANDLER
// ============================================================================

function handleMqttMessage(topic, message) {
    messageCount++;
    updateMessageCount();

    try {
        const payload = JSON.parse(message.toString());

        // Route message to appropriate handler
        if (topic.includes('/status')) {
            handleNodeStatus(payload);
        } else if (topic.includes('/fitness/')) {
            handleFitnessResult(payload);
        } else if (topic.includes('/capsule/in')) {
            handleGenomeCapsule(payload);
        } else if (topic.includes('/ohlcv/')) {
            handleOhlcvData(payload);
        }

        // Append to timeline
        appendToTimeline(topic, payload);

    } catch (e) {
        console.error('Failed to parse message:', e);
    }
}

// ============================================================================
// EVENT HANDLERS
// ============================================================================

function handleNodeStatus(status) {
    const nodeId = status.node;
    const nodeElement = document.getElementById(`node-${nodeId}`);

    if (nodeElement) {
        // Update state badge
        const stateElement = nodeElement.querySelector('.node-state');
        if (stateElement) {
            stateElement.textContent = status.state;
            stateElement.className = `node-state ${status.state}`;
        }

        // Update uptime
        const uptimeElement = nodeElement.querySelector('.uptime');
        if (uptimeElement) {
            uptimeElement.textContent = `${status.uptime_s}s`;
        }

        // Update node item styling
        if (status.state === 'ready') {
            nodeElement.classList.add('ready');
            connectedNodes.add(nodeId);
        } else {
            nodeElement.classList.remove('ready');
            connectedNodes.delete(nodeId);
        }

        updateConnectedNodesCount();
    }
}

function handleFitnessResult(fitness) {
    console.log(`Fitness result: ${fitness.agent_id} = ${fitness.fitness} (${fitness.status})`);

    // Add to fitness history
    if (fitness.status === 'ok') {
        fitnessHistory.push({
            generation: currentGeneration,
            fitness: fitness.fitness,
            timestamp: Date.now()
        });

        // Update chart
        updateFitnessChart();
    }
}

function handleGenomeCapsule(capsule) {
    console.log(`Genome capsule: ${capsule.agent_id} gen=${capsule.generation}`);

    currentGeneration = capsule.generation;

    // Display in capsule inspector
    displayCapsule(capsule);

    // Update generation counter
    document.getElementById('current-gen').textContent = currentGeneration;
}

function handleOhlcvData(ohlcv) {
    console.log(`OHLCV data: ${ohlcv.isin} (${ohlcv.data.length} bars)`);
}

// ============================================================================
// UI UPDATES
// ============================================================================

function updateConnectionStatus(connected) {
    const statusIndicator = document.getElementById('mqtt-status');
    const statusText = document.getElementById('mqtt-status-text');

    if (connected) {
        statusIndicator.className = 'status-indicator connected';
        statusText.textContent = 'Connected';
    } else {
        statusIndicator.className = 'status-indicator disconnected';
        statusText.textContent = 'Disconnected';
    }
}

function updateBrowserNodeStatus(state) {
    const stateElement = document.getElementById('browser-state');
    if (stateElement) {
        stateElement.textContent = state;
        stateElement.className = `node-state ${state}`;
    }

    const browserNode = document.getElementById('node-browser-observatory');
    if (browserNode && state === 'ready') {
        browserNode.classList.add('ready');
    }
}

function updateMessageCount() {
    document.getElementById('message-count').textContent = messageCount;
}

function updateConnectedNodesCount() {
    document.getElementById('connected-nodes').textContent = `${connectedNodes.size}/7`;
}

function displayCapsule(capsule) {
    const display = document.getElementById('capsule-display');
    const formatted = JSON.stringify(capsule, null, 2);

    // Simple syntax highlighting
    const highlighted = formatted
        .replace(/"([^"]+)":/g, '<span class="json-key">"$1"</span>:')
        .replace(/: "([^"]+)"/g, ': <span class="json-string">"$1"</span>')
        .replace(/: (\d+\.?\d*)/g, ': <span class="json-number">$1</span>')
        .replace(/: (true|false)/g, ': <span class="json-boolean">$1</span>');

    display.innerHTML = highlighted;
}

function appendToTimeline(topic, payload) {
    const timeline = document.getElementById('timeline');

    // Remove empty state if present
    const emptyState = timeline.querySelector('.empty-state');
    if (emptyState) {
        emptyState.remove();
    }

    const entry = document.createElement('div');
    entry.className = 'timeline-entry';

    // Add type-specific class
    if (topic.includes('capsule')) {
        entry.classList.add('capsule');
    } else if (topic.includes('fitness')) {
        entry.classList.add('fitness');
    } else if (topic.includes('ohlcv')) {
        entry.classList.add('ohlcv');
    }

    const timestamp = new Date().toLocaleTimeString();
    const summary = summarizePayload(topic, payload);

    entry.innerHTML = `
        <span class="time">[${timestamp}]</span>
        <span class="topic">${topic}</span>
        <span class="summary">${summary}</span>
    `;

    timeline.appendChild(entry);

    // Auto-scroll to bottom
    timeline.scrollTop = timeline.scrollHeight;

    // Keep only last 100 entries
    while (timeline.children.length > 100) {
        timeline.removeChild(timeline.firstChild);
    }
}

function summarizePayload(topic, payload) {
    if (topic.includes('/status')) {
        return `Node ${payload.node}: ${payload.state} (${payload.role})`;
    } else if (topic.includes('/fitness/')) {
        return `Fitness: ${payload.agent_id} = ${payload.fitness.toFixed(4)} (${payload.status})`;
    } else if (topic.includes('/capsule/in')) {
        return `Capsule: ${payload.agent_id} gen=${payload.generation} hash=${payload.genome_hash.substring(0, 20)}...`;
    } else if (topic.includes('/ohlcv/')) {
        return `OHLCV: ${payload.isin} (${payload.data.length} bars, ${payload.resolution})`;
    }
    return JSON.stringify(payload).substring(0, 60) + '...';
}

// ============================================================================
// FITNESS CHART
// ============================================================================

function updateFitnessChart() {
    const canvas = document.getElementById('fitness-chart');
    const ctx = canvas.getContext('2d');

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (fitnessHistory.length === 0) {
        ctx.fillStyle = '#999';
        ctx.font = '14px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('Waiting for fitness data...', canvas.width / 2, canvas.height / 2);
        return;
    }

    // Chart dimensions
    const padding = 40;
    const chartWidth = canvas.width - 2 * padding;
    const chartHeight = canvas.height - 2 * padding;

    // Draw axes
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();

    // Labels
    ctx.fillStyle = '#333';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Generation', canvas.width / 2, canvas.height - 10);
    ctx.save();
    ctx.translate(15, canvas.height / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Fitness', 0, 0);
    ctx.restore();

    // Data range
    const maxGen = Math.max(...fitnessHistory.map(d => d.generation));
    const maxFitness = Math.max(...fitnessHistory.map(d => d.fitness));
    const minFitness = Math.min(...fitnessHistory.map(d => d.fitness));

    // Scale functions
    const scaleX = (gen) => padding + (gen / maxGen) * chartWidth;
    const scaleY = (fitness) => canvas.height - padding - ((fitness - minFitness) / (maxFitness - minFitness || 1)) * chartHeight;

    // Draw line
    ctx.strokeStyle = '#4A90E2';
    ctx.lineWidth = 2;
    ctx.beginPath();
    fitnessHistory.forEach((point, i) => {
        const x = scaleX(point.generation);
        const y = scaleY(point.fitness);
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();

    // Draw points
    ctx.fillStyle = '#4A90E2';
    fitnessHistory.forEach(point => {
        const x = scaleX(point.generation);
        const y = scaleY(point.fitness);
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fill();
    });

    // Update stats
    const bestFitness = Math.max(...fitnessHistory.map(d => d.fitness));
    const avgFitness = fitnessHistory.reduce((sum, d) => sum + d.fitness, 0) / fitnessHistory.length;

    document.getElementById('best-fitness').textContent = bestFitness.toFixed(4);
    document.getElementById('avg-fitness').textContent = avgFitness.toFixed(4);
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

document.getElementById('clear-timeline').addEventListener('click', () => {
    const timeline = document.getElementById('timeline');
    timeline.innerHTML = '<div class="empty-state">Timeline cleared</div>';
});

// ============================================================================
// BROWSER UPTIME COUNTER
// ============================================================================

setInterval(() => {
    const uptime = Math.floor((Date.now() - browserStartTime) / 1000);
    const uptimeElement = document.getElementById('browser-uptime');
    if (uptimeElement) {
        uptimeElement.textContent = `${uptime}s`;
    }
}, 1000);

// ============================================================================
// INITIALIZATION
// ============================================================================

window.addEventListener('DOMContentLoaded', () => {
    console.log('TR4D3RZ MVP Browser Demo initialized');
    connectToMqtt();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (mqttClient) {
        mqttClient.end();
    }
});
