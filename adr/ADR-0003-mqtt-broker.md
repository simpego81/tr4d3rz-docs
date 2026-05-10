# ADR-0003: MQTT Broker & Data Source Node

**Date**: 2026-05-10
**Status**: Accepted
**Author**: Manus (Chief Architect)

---

## Context

The TR4D3RZ ecosystem requires a reliable messaging backbone (MQTT) and a source of real OHLCV data from the Italian Stock Exchange. The user has specified that both the MQTT broker and the data scraper should run on a local Raspberry Pi 1 (ARM1176, ARMv6l, 700MHz). The existing `borsa-italiana-scraper` Node.js project will be reused for data collection.

The ARMv6l architecture is highly constrained. Modern versions of Mosquitto (2.x) have known issues (Illegal Instruction errors) on ARMv6l under certain OS configurations (e.g., DietPi/Debian Bullseye), while NanoMQ is designed as an ultra-lightweight alternative for IoT edge devices [1] [2] [3].

## Decisions

### 1. Hardware Role Assignment
The Raspberry Pi 1 (ARMv6l) is designated as a **Core Infrastructure Node**. It will simultaneously act as:
- The central MQTT Broker for the entire local ecosystem.
- The Data Ingestion Node (running `borsa-italiana-scraper`).

### 2. MQTT Broker Selection: NanoMQ
Instead of Eclipse Mosquitto, **NanoMQ** is selected as the MQTT broker for the Raspberry Pi 1.

**Rationale**:
- NanoMQ is specifically designed for constrained IoT edge devices and offers fully asynchronous I/O and multi-threading support [3].
- Mosquitto 2.x has documented "Illegal Instruction" compilation/execution issues on ARMv6l (Raspberry Pi 1 / Zero) due to lack of backports and architecture mismatch in some Debian/Raspbian repositories [1] [2]. NanoMQ mitigates this risk while providing full MQTT 3.1.1/5.0 compliance.

### 3. Data Ingestion: borsa-italiana-scraper
The existing `borsa-italiana-scraper` repository will be integrated into the TR4D3RZ ecosystem.

**Rationale**:
- The scraper is already capable of fetching Intraday (1MN to 1H) and Historical OHLCV data.
- It will be modified (or wrapped) to publish the scraped JSON data directly to the MQTT broker under the `data/ohlcv/{isin}` topic, acting as the live data feed for the Evolution Nodes.

## Consequences

**Positive**: 
- Centralizes data ingestion and messaging on a single low-power, always-on device.
- Reuses existing, tested scraping logic.

**Negative**:
- The user's Raspberry Pi 1 is running **Node.js 14.15.1**. The `borsa-italiana-scraper` codebase is fully compatible with Node 14 (ES modules via `type: module` are supported since Node 12.17+). However, the `p-limit` dependency must be downgraded from `^5.0.0` (which requires Node >=18) to `^4.0.0` (which supports Node >=14.13.1). The `axios` dependency (`^1.6.0`) is fully compatible with Node 14.
- NanoMQ configuration must be carefully tuned to avoid overwhelming the 700MHz single-core CPU when multiple Evolution Nodes connect simultaneously.

## References
[1] DietPi-Software | Mosquitto fails to install on ARMv6 #5140 - GitHub: https://github.com/MichaIng/DietPi/issues/5140
[2] Mosquitto MQTT broker on Opal GL-SFT1200 not working: https://forum.gl-inet.com/t/mosquitto-mqtt-broker-on-opal-gl-sft1200-not-working/37650
[3] NanoMQ: An Ultra-lightweight MQTT Broker for IoT Edge: https://nanomq.io/
