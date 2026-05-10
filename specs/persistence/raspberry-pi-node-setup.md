# Raspberry Pi 1 — Core Infrastructure Node Setup Guide

**Status**: Draft
**Author**: Manus (Chief Architect)

---

## Hardware Profile

| Property | Value |
|---|---|
| Model | Raspberry Pi 1 (ARM1176 / ARMv6l) |
| Kernel | Linux 5.10.103+ |
| CPU | ARM1176 @ 700MHz (single core) |
| Architecture | ARMv6l, Little Endian |
| OS | Raspbian (Bullseye or later) |

---

## Role in the Ecosystem

This node acts as the **Core Infrastructure Node** for the local TR4D3RZ deployment. It hosts:
1. **NanoMQ MQTT Broker** — The central message bus for all local nodes.
2. **borsa-italiana-scraper** — The data ingestion process that fetches OHLCV data from `borsaitaliana.it` and publishes it to the MQTT broker.
3. **Persistence Service** (future, Milestone 2) — SQLite-based event log and archetype memory.

---

## NanoMQ Installation

NanoMQ must be compiled from source for ARMv6l, as pre-built binaries may not be available. The following procedure is recommended:

```bash
# Install build dependencies
sudo apt-get update
sudo apt-get install -y cmake git build-essential

# Clone NanoMQ
git clone https://github.com/emqx/nanomq.git
cd nanomq
git submodule update --init --recursive

# Build (single-threaded to avoid OOM on 512MB RPi 1)
mkdir build && cd build
cmake -DNNG_ENABLE_TLS=OFF -DBUILD_CLIENT=ON ..
make -j1

# Install
sudo make install
```

**Recommended NanoMQ configuration** (`/etc/nanomq.conf`):
```hocon
listeners.tcp {
  bind = "0.0.0.0:1883"
}
log {
  to = file
  level = warn
  dir = "/var/log/nanomq"
}
```

---

## borsa-italiana-scraper Setup

The target Raspberry Pi 1 is running **Node.js v14.15.1**. The `borsa-italiana-scraper` is fully compatible with Node 14's ES module support (`type: module`), but the `p-limit` dependency must be downgraded to version 4 (as version 5 requires Node >=18).

```bash
# Clone the scraper
git clone https://github.com/simpego81/borsa-italiana-scraper.git
cd borsa-italiana-scraper

# Install dependencies and downgrade p-limit for Node 14 compatibility
npm install
npm install p-limit@4

# Run (once MQTT integration is complete — see ADR-0004)
node index.js --period=1Y --mqtt=mqtt://localhost:1883
```

---

## Resource Constraints

Given the ARMv6l CPU and limited RAM, the following constraints apply:

| Constraint | Limit | Mitigation |
|---|---|---|
| CPU | 700MHz single core | Run NanoMQ and scraper at different times; use cron for scheduled scraping |
| RAM | ~256–512MB | Limit scraper concurrency to 2–3 (not 5) |
| Storage | SD card | Use SQLite with WAL mode; rotate Parquet files |

---

## Cron Schedule (Recommended)

```cron
# Daily historical data refresh at 18:30 (after market close)
30 18 * * 1-5 cd /home/pi/borsa-italiana-scraper && node index.js --period=1M --mqtt=mqtt://localhost:1883

# Intraday data every 15 minutes during market hours (09:00-17:30 CET)
*/15 9-17 * * 1-5 cd /home/pi/borsa-italiana-scraper && node index.js --mode=intraday --resolution=5MN --mqtt=mqtt://localhost:1883
```
