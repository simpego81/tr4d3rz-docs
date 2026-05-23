# ADR-0003: MQTT Broker & Data Source Node

**Date**: 2026-05-10
**Status**: Accepted
**Author**: Manus (Chief Architect)

---

## Context

The TR4D3RZ ecosystem requires a reliable messaging backbone (MQTT) and a source of real OHLCV data from the Italian Stock Exchange. The user has specified that the local infrastructure must now run on a **single Raspberry Pi 2 Model B (ARMv7, quad-core, 900MHz, 1GB RAM)**. This device consolidates the former core infrastructure and persistence roles: MQTT broker, data scraper, event logger, local persistence and relay/gateway services. The existing `borsa-italiana-scraper` Node.js project will be reused for data collection.

The ARMv7 target is less constrained than the former single-core legacy profile. Modern Mosquitto 2.x "Illegal Instruction" issues that were critical on older 32-bit ARM deployments are therefore less severe on Raspberry Pi 2, but NanoMQ remains the preferred broker because it is lightweight, asynchronous and suitable for IoT edge workloads [1] [2] [3].

## Decisions

### 1. Hardware Role Assignment
The Raspberry Pi 2 is designated as the **Central Infrastructure & Persistence Node**. It will simultaneously act as:
- The central MQTT Broker for the entire local ecosystem.
- The Data Ingestion Node running `borsa-italiana-scraper`.
- The Event Logger and local Persistence Service for SQLite/Parquet outputs.
- The local relay/gateway endpoint for ESP8266, STM32, Linux PC and offline bridge nodes.

### 2. MQTT Broker Selection: NanoMQ
Instead of Eclipse Mosquitto, **NanoMQ** is selected as the MQTT broker for the Raspberry Pi 2.

**Rationale**:
- NanoMQ is specifically designed for constrained IoT edge devices and offers fully asynchronous I/O and multi-threading support [3].
- Mosquitto 2.x has documented "Illegal Instruction" compilation/execution issues on older 32-bit ARM deployments due to lack of backports and architecture mismatch in some Debian/Raspbian repositories [1] [2]. On ARMv7 this risk is reduced, but NanoMQ still provides a simpler low-overhead fit for a single always-on RPi2 node.

### 3. Data Ingestion: borsa-italiana-scraper
The existing `borsa-italiana-scraper` repository will be integrated into the TR4D3RZ ecosystem.

**Rationale**:
- The scraper is already capable of fetching Intraday (1MN to 1H) and Historical OHLCV data.
- It will be modified (or wrapped) to publish the scraped JSON data directly to the MQTT broker under the `data/ohlcv/{isin}` topic, acting as the live data feed for the Evolution Nodes.

## Consequences

**Positive**: 
- Centralizes data ingestion, messaging, logging and local persistence on a single low-power, always-on Raspberry Pi 2.
- Reuses existing, tested scraping logic.
- Uses the RPi2 quad-core CPU to separate broker responsiveness from scraper/logger activity.

**Negative**:
- The user's scraper environment is still assumed to run **Node.js 14.15.1**. The `borsa-italiana-scraper` codebase is compatible with Node 14 (ES modules via `type: module` are supported since Node 12.17+). However, the `p-limit` dependency must be downgraded from `^5.0.0` (which requires Node >=18) to `^4.0.0` (which supports Node >=14.13.1). The `axios` dependency (`^1.6.0`) is fully compatible with Node 14.
- NanoMQ must be given priority over scraper and logger bursts. Recommended mitigations include conservative scraper concurrency, SQLite WAL mode, log rotation, and process priority or CPU affinity so the broker remains responsive during market-data refreshes.

## References
[1] DietPi-Software | Mosquitto fails to install on ARMv6 #5140 - GitHub: https://github.com/MichaIng/DietPi/issues/5140
[2] Mosquitto MQTT broker on Opal GL-SFT1200 not working: https://forum.gl-inet.com/t/mosquitto-mqtt-broker-on-opal-gl-sft1200-not-working/37650
[3] NanoMQ: An Ultra-lightweight MQTT Broker for IoT Edge: https://nanomq.io/
