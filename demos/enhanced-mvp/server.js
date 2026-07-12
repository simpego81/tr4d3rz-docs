/**
 * TR4D3RZ Enhanced MVP Demo - Server
 *
 * This server integrates REAL Rust components (tr4d3rz-core) via CLI bridge
 * to demonstrate the actual implementation status of M1.
 */

const express = require('express');
const { exec } = require('child_process');
const { promisify } = require('util');
const path = require('path');
const fs = require('fs');

const execAsync = promisify(exec);
const app = express();
const PORT = 3100;

// Path to tr4d3rz-core demo CLI
const DEMO_CLI = path.join(__dirname, '../../..', 'tr4d3rz-core/target/release/examples/demo_cli.exe');

// Middleware
app.use(express.json());
app.use(express.static('public'));

// API: Get component info
app.get('/api/component/info', async (req, res) => {
    try {
        const { stdout } = await execAsync(`"${DEMO_CLI}" info`);
        res.json(JSON.parse(stdout));
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// API: Create GenomeCapsule
app.get('/api/create/capsule/:agentId/:isin', async (req, res) => {
    try {
        const { agentId, isin } = req.params;
        const { stdout } = await execAsync(`"${DEMO_CLI}" create-capsule ${agentId} ${isin}`);
        const capsule = JSON.parse(stdout);

        // Calculate CBOR size
        const cborCmd = `"${DEMO_CLI}" encode-cbor capsule '${stdout.replace(/'/g, "\\'")}'`;
        const { stdout: cborOutput } = await execAsync(cborCmd);
        const cborInfo = JSON.parse(cborOutput);

        res.json({
            capsule,
            cbor_size: cborInfo.cbor_size_bytes
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// API: Create FitnessResult
app.get('/api/create/fitness/:agentId/:value', async (req, res) => {
    try {
        const { agentId, value } = req.params;
        const { stdout } = await execAsync(`"${DEMO_CLI}" create-fitness ${agentId} ${value}`);
        const fitness = JSON.parse(stdout);

        // Calculate CBOR size
        const cborCmd = `"${DEMO_CLI}" encode-cbor fitness '${stdout.replace(/'/g, "\\'")}'`;
        const { stdout: cborOutput } = await execAsync(cborCmd);
        const cborInfo = JSON.parse(cborOutput);

        res.json({
            fitness,
            cbor_size: cborInfo.cbor_size_bytes
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// API: Create OHLCV data
app.get('/api/create/ohlcv/:isin', async (req, res) => {
    try {
        const { isin } = req.params;
        const { stdout } = await execAsync(`"${DEMO_CLI}" create-ohlcv ${isin}`);
        const ohlcv = JSON.parse(stdout);

        // Calculate CBOR size
        const cborCmd = `"${DEMO_CLI}" encode-cbor ohlcv '${stdout.replace(/'/g, "\\'")}'`;
        const { stdout: cborOutput } = await execAsync(cborCmd);
        const cborInfo = JSON.parse(cborOutput);

        res.json({
            ohlcv,
            cbor_size: cborInfo.cbor_size_bytes,
            bars_count: ohlcv.data.length
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// API: Get M1 status
app.get('/api/m1/status', (req, res) => {
    res.json({
        milestone: "M1",
        title: "Foundational Backbone Single RPi2",
        tasks: [
            {
                id: "M1-T0",
                repo: "tr4d3rz-docs",
                title: "Specs & Contracts",
                status: "COMPLETED",
                agent: "Manus",
                tests_passing: null,
                deliverables: ["SPEC_MASTER.md", "TASK_QUEUE.md", "MVP contracts"]
            },
            {
                id: "M1-T1",
                repo: "tr4d3rz-core",
                title: "Core Types (Rust)",
                status: "COMPLETED",
                agent: "Claude Code",
                tests_passing: 8,
                tests_total: 8,
                deliverables: ["OHLCV types", "GenomeCapsule", "FitnessResult", "NodeStatus"]
            },
            {
                id: "M1-T2",
                repo: "tr4d3rz-messaging",
                title: "MQTT Client (Rust)",
                status: "COMPLETED",
                agent: "Claude Code",
                tests_passing: 12,
                tests_total: 13,
                deliverables: ["MQTT wrapper", "Topic builder", "CBOR serialization"]
            },
            {
                id: "M1-T2-B",
                repo: "tr4d3rz-messaging",
                title: "Remote Validation Probe",
                status: "COMPLETED",
                agent: "Claude Code",
                tests_passing: null,
                deliverables: ["Heartbeat probe", "PC-to-RPi validation"]
            },
            {
                id: "M1-T3",
                repo: "tr4d3rz-persistence",
                title: "Event Logger (SQLite)",
                status: "READY",
                agent: "Claude Code",
                tests_passing: null,
                deliverables: ["SQLite logger", "MQTT subscriber", "Query API"]
            },
            {
                id: "M1-T4",
                repo: "tr4d3rz-evolution",
                title: "Evolution CLI",
                status: "READY",
                agent: "Claude Code",
                tests_passing: null,
                deliverables: ["Genome generator", "Mutation operators"]
            },
            {
                id: "M1-T5",
                repo: "tr4d3rz-embedded",
                title: "ESP8266 Firmware",
                status: "READY",
                agent: "GitHub Copilot",
                tests_passing: null,
                deliverables: ["ESP8266 firmware or simulator"]
            },
            {
                id: "M1-T6",
                repo: "tr4d3rz-observatory",
                title: "Observatory UI",
                status: "BLOCKED",
                agent: "Antigravity",
                tests_passing: null,
                dependencies: ["M1-T2", "M1-T3"],
                deliverables: ["Event timeline", "Node status", "Fitness chart"]
            },
            {
                id: "M1-T7",
                repo: "cross-repo",
                title: "Architectural Audit",
                status: "BLOCKED",
                agent: "Antigravity",
                tests_passing: null,
                dependencies: ["M1-T1", "M1-T2", "M1-T3", "M1-T4", "M1-T5", "M1-T6"],
                deliverables: ["ARCHITECTURAL_AUDIT.md"]
            }
        ],
        summary: {
            total: 9,
            completed: 4,
            ready: 3,
            blocked: 2
        }
    });
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', demo: 'enhanced-mvp', version: '1.0.0' });
});

// Start server
app.listen(PORT, () => {
    console.log(`✅ TR4D3RZ Enhanced MVP Demo Server running on http://localhost:${PORT}`);
    console.log(`📦 Using Rust demo CLI: ${DEMO_CLI}`);
    console.log();
    console.log(`Available endpoints:`);
    console.log(`  GET  /                                      - Demo UI`);
    console.log(`  GET  /api/component/info                    - Component info`);
    console.log(`  GET  /api/create/capsule/:agentId/:isin     - Create GenomeCapsule`);
    console.log(`  GET  /api/create/fitness/:agentId/:value    - Create FitnessResult`);
    console.log(`  GET  /api/create/ohlcv/:isin                - Create OHLCV data`);
    console.log(`  GET  /api/m1/status                         - M1 milestone status`);
});
