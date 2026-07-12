# FEATURE: MQTT Remote Verification (Heartbeat Probe)

## 1. Goal
Implement a continuous validation system to ensure the MQTT communication backbone is operational from a remote workstation (PC).

## 2. Requirements
- **Remote Validation**: Validate RPi broker from PC.
- **Automated Workflow**: Connection -> Subscription -> Publication -> Verification -> Reporting.
- **Performance Baseline**: Measure Round Trip Time (RTT).
- **Exit Codes**: Provide specific exit codes for automated CI/CD integration.

## 3. Interfaces
- **MQTT Topic**: `tr4d3rz/node/validator/echo` (QoS 1).
- **Payload**: `NodeStatus` (serialized via CBOR).
- **Environment**: `TR4D3RZ_BROKER_IP` defined in `.env.test`.

## 4. Acceptance Criteria
- Compiles successfully: `cargo build --example remote_validation_probe`.
- Exit Code 0 on success.
- Exit Code 1 on timeout (10s).
- Exit Code 2 on auth error.
- Exit Code 3 on integrity failure.
- Exit Code 4 on generic error (e.g., missing ENV).
