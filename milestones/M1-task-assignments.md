# Milestone 1: Task Assignments

**Status**: Ready for execution
**Author**: Manus (Chief Architect)

---

## 1. Claude Code — `tr4d3rz-core` & `tr4d3rz-messaging`

**Objective**: Implement the foundation of the FSM runtime and the messaging backbone.

**Tasks**:
1. **Core Types (Rust)**: Implement the basic data structures in `tr4d3rz-core` for the OHLCV data contract defined in ADR-0004.
2. **Messaging (Rust)**: Implement a NanoMQ-compatible MQTT client in `tr4d3rz-messaging` that can subscribe to `data/ohlcv/#` and deserialize the JSON payloads into the core Rust types.
3. **FSM Skeleton (Rust)**: Create the basic trait definitions for an FSM node, state, and transition in `tr4d3rz-core`.

## 2. Gemini CLI — `tr4d3rz-observatory`

**Objective**: Build the initial Observatory UI skeleton to monitor the data feed.

**Tasks**:
1. **Project Setup**: Initialize a Vite + TypeScript + React project in `tr4d3rz-observatory`.
2. **MQTT Client (TS)**: Implement an MQTT WebSocket client to connect to the NanoMQ broker on the Raspberry Pi.
3. **Data Dashboard**: Create a simple real-time chart (e.g., using Chart.js or Lightweight Charts) that plots the incoming OHLCV data from `data/ohlcv/intraday/+`.

## 3. GitHub Copilot — `borsa-italiana-scraper` (Integration)

**Objective**: Adapt the existing scraper to publish to the MQTT broker.

**Tasks**:
1. **Node 14 Compatibility & MQTT**: Downgrade `p-limit` to version 4 (`npm install p-limit@4`) to ensure compatibility with Node.js 14.15.1 on the Raspberry Pi. Then, add the `mqtt` npm package.
2. **Data Transformation**: Modify `index.js` to transform the scraped data into the schema defined in ADR-0004 (Unix timestamps, minified keys).
3. **Publishing Logic**: Add a CLI flag `--mqtt=mqtt://<rpi-ip>:1883` to publish the transformed data to `data/ohlcv/history/{isin}` and `data/ohlcv/intraday/{isin}` instead of (or in addition to) saving to files.
