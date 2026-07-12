# RISKS & MITIGATIONS: FEATURE-M1-T2-B

## 1. Technical Risks
- **Network Latency**: High RTT might trigger false negatives if timeouts are too aggressive.
    - *Mitigation*: Baseline measurement and configurable timeouts.
- **Event Loop Blocking**: If the poll loop isn't spawned correctly, the probe will hang.
    - *Mitigation*: Explicit `tokio::spawn` for the event loop as per architectural patterns.

## 2. Assumptions
- **Subnet Consistency**: Assumes PC and RPi are on the same local network.
- **Broker Config**: Assumes Mosquitto is configured to accept connections on `0.0.0.0:1883`.
