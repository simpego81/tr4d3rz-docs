# ADR-0004: OHLCV Data Contract

**Date**: 2026-05-10
**Status**: Accepted
**Author**: Manus (Chief Architect)

---

## Context

The `borsa-italiana-scraper` repository provides historical and intraday OHLCV (Open, High, Low, Close, Volume) data. To ensure the Evolution Nodes and FSM runtime can process this data efficiently, a strict data contract must be established for the MQTT payloads published by the scraper node.

## Decisions

### 1. Data Granularity and Modes
The system will support two modes of operation, mapped directly from the scraper:
- **Intraday Mode**: High-resolution data (1MN, 5MN, 15MN, 30MN, 1H). Used for live signaling and short-term FSM evaluation.
- **History Mode**: Daily resolution data (1M, 3M, 6M, 1Y, 3Y, 5Y). Used for long-term evolutionary fitness evaluation and backtesting.

### 2. MQTT Topic Structure for Data
The scraper will publish data to the following MQTT topics:
- `data/ohlcv/history/{isin}`
- `data/ohlcv/intraday/{isin}`

### 3. Payload Schema (JSON)
While internal node-to-node communication uses CBOR (ADR-0002), the raw data feed from the Node.js scraper will be published as JSON for ease of debugging and direct consumption by the Observatory UI. The `tr4d3rz-messaging` Gateway/Relay can optionally transcode this to CBOR for embedded nodes.

**History Payload Schema**:
```json
{
  "v": 1,
  "type": "ohlcv_history",
  "isin": "IT0001233417",
  "mic": "MTAA",
  "resolution": "1D",
  "data": [
    {
      "ts": 1712448000000,  // Unix timestamp ms (parsed from "YYYYMMDD")
      "o": 2.51,
      "h": 2.559,
      "l": 2.508,
      "c": 2.518,
      "v": 10672012,
      "t": 3306            // Trades count
    }
  ]
}
```

**Intraday Payload Schema**:
```json
{
  "v": 1,
  "type": "ohlcv_intraday",
  "isin": "IT0001233417",
  "mic": "MTAA",
  "resolution": "1MN",
  "data": [
    {
      "ts": 1715065200000,  // Unix timestamp ms (parsed from "YYYYMMDD-HH:MM:SS")
      "o": 2.394,
      "h": 2.396,
      "l": 2.379,
      "c": 2.38,
      "t": 101             // Trades count
    }
  ]
}
```

## Consequences

**Positive**: 
- Maps cleanly to the existing scraper output.
- Standardized keys (`o`, `h`, `l`, `c`, `v`, `t`, `ts`) reduce payload size compared to the verbose scraper output.

**Negative**:
- The scraper must be updated to parse its proprietary date formats (`YYYYMMDD` and `YYYYMMDD-HH:MM:SS`) into standard Unix timestamps (milliseconds) before publishing.
