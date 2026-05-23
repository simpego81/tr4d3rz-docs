# Raspberry Pi 2 — Central Infrastructure & Persistence Node Setup Guide

**Status**: Draft
**Author**: Manus (Chief Architect)

---

## Hardware Profile

| Property | Value |
|---|---|
| Model | Raspberry Pi 2 Model B (2015) |
| Kernel | Linux 5.10+ or later |
| CPU | ARM Cortex-A7 @ 900MHz (quad-core) |
| Architecture | ARMv7, Little Endian |
| RAM | 1GB |
| OS | Raspberry Pi OS / Raspbian compatible release |

---

## Role in the Ecosystem

This node acts as the **Central Infrastructure & Persistence Node** for the local TR4D3RZ deployment. It hosts NanoMQ, the OHLCV scraper, the append-only event logger, the local persistence service and the relay/gateway endpoint. ESP8266, STM32 bridge processes and Linux PC evolution nodes must target the single RPi2 IP address for MQTT, WebSocket and local relay traffic.

---

## NanoMQ Installation

NanoMQ remains the preferred MQTT broker because it is lightweight and suitable for IoT edge workloads. On ARMv7/RPi2 the Mosquitto 2.x illegal-instruction risk seen on older 32-bit ARM deployments is less critical, but NanoMQ still preserves a smaller and more controllable infrastructure footprint.

```bash
# Install build dependencies
sudo apt-get update
sudo apt-get install -y cmake git build-essential

# Clone NanoMQ
git clone https://github.com/emqx/nanomq.git
cd nanomq
git submodule update --init --recursive

# Build for the quad-core RPi2 while keeping RAM use conservative
mkdir build && cd build
cmake -DNNG_ENABLE_TLS=OFF -DBUILD_CLIENT=ON ..
make -j2

# Install
sudo make install
```

**Recommended NanoMQ configuration** (`/etc/nanomq.conf`):
```hocon
listeners.tcp {
  bind = "0.0.0.0:1883"
}
listeners.ws {
  bind = "0.0.0.0:8083/mqtt"
}
log {
  to = file
  level = warn
  dir = "/var/log/nanomq"
}
```

---

## borsa-italiana-scraper Setup

The scraper environment is still assumed to use **Node.js v14.15.1** unless upgraded explicitly. The `borsa-italiana-scraper` project remains compatible with Node 14's ES module support (`type: module`), but `p-limit` should remain on version 4 when Node 14 is used.

```bash
# Clone the scraper
git clone https://github.com/simpego81/borsa-italiana-scraper.git
cd borsa-italiana-scraper

# Install dependencies and keep p-limit compatible with Node 14
npm install
npm install p-limit@4

# Run (once MQTT integration is complete — see ADR-0004)
node index.js --period=1Y --mqtt=mqtt://localhost:1883
```

---

## Resource Management

The RPi2 quad-core CPU permits NanoMQ, scraper, logger and persistence service to run together, but broker responsiveness remains the priority. The recommended baseline is to reserve operational headroom for NanoMQ, limit scraper concurrency and keep persistence writes append-only.

| Resource | RPi2 Baseline | Mitigation |
|---|---|---|
| CPU | ARMv7 quad-core @ 900MHz | Run NanoMQ with higher process priority; optionally pin scraper/logger away from the broker core using CPU affinity. |
| RAM | 1GB | Limit scraper concurrency to a conservative value and avoid large in-memory OHLCV batches. |
| Storage | SD card | Use SQLite WAL mode, rotate logs and export historical data to Parquet in scheduled windows. |
| Network | Single local endpoint | Keep ESP8266, STM32 bridges and Linux PC clients pointed to the same RPi2 IP for MQTT/WebSocket traffic. |

---

## Cron Schedule (Recommended)

```cron
# Daily historical data refresh at 18:30 (after market close)
30 18 * * 1-5 cd /home/pi/borsa-italiana-scraper && nice -n 5 node index.js --period=1M --mqtt=mqtt://localhost:1883

# Intraday data every 15 minutes during market hours (09:00-17:30 CET)
*/15 9-17 * * 1-5 cd /home/pi/borsa-italiana-scraper && nice -n 5 node index.js --mode=intraday --resolution=5MN --mqtt=mqtt://localhost:1883
```
