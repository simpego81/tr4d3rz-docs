# TASK M1-T2-B: MQTT Remote Verification & Automated Validation Spec

**Role**: State Evaluator & QA (Gemini CLI)  
**Recipient**: Manus (Chief Architect)  
**Status**: DRAFT / PROPOSAL  
**Reference**: Extension of M1-T2 (Backbone Messaging)

---

## 1. Executive Summary
Following the successful manual verification of the MQTT broker on Raspberry Pi (via SSH and PC-side manual tools), we need to formalize a **continuous validation system**. This system must ensure that the communication backbone is operational at any time, validated from a remote PC acting as the primary research workstation.

## 2. Automated Test Design: "The Heartbeat Probe"
The test will be implemented as a specialized integration test within the `tr4d3rz-messaging` repository, designed to run on the PC.

### Test Workflow (Sequence)
1.  **Connection Phase**: The PC client connects to the RPi Broker using the IP address provided in environment variables.
2.  **Subscription Phase**: The PC client subscribes to `tr4d3rz/node/validator/echo`.
3.  **Publication Phase**: The PC client generates a randomized `NodeStatus` payload, serializes it via CBOR, and publishes it to `tr4d3rz/node/validator/echo`.
4.  **Verification Phase**:
    - The client waits for the message to be received (loopback via broker).
    - It deserializes the payload and compares it with the original.
    - It measures the Round Trip Time (RTT) to establish a baseline for latency.
5.  **Reporting Phase**: The tool exits with code 0 on success, or a descriptive error code on failure (Connection Timeout, Auth Error, Integrity Failure).

## 3. Instructions for Manus (Orchestration)
To properly integrate this into the workflow, **Manus** is requested to:

1.  **Update `TASK_QUEUE.md`**: Add `M1-T2-B` as a mandatory validation gate before proceeding to `M1-T5` (Embedded).
2.  **Assign Task to Claude Code**: Claude should implement a new example/tool in `tr4d3rz-messaging` called `remote_validation_probe.rs`.
3.  **Assign Validation to GitHub Copilot**: Copilot should verify the tool's error handling and documentation.
4.  **Infrastructure Secret Management**: Define a standard for `.env.test` files (to be added to `.gitignore`) where the user stores the `TR4D3RZ_BROKER_IP`.

## 4. Software & System Requirements

### PC (Validation Host)
- **Rust Toolchain**: `stable-x86_64-pc-windows-msvc` or equivalent.
- **Crate dependencies**: `tr4d3rz-messaging` (local path), `tokio`, `anyhow`, `dotenvy`.
- **Environment**: Must be on the same subnet as the Raspberry Pi.

### Raspberry Pi (Target Service)
- **OS**: Raspberry Pi OS (Lite recommended).
- **Broker**: Mosquitto Broker (`sudo apt install mosquitto mosquitto-clients`).
- **Configuration**:
    - Port `1883` must be open and binding to `0.0.0.0` (or the specific local IP).
    - Allow anonymous connections for M1 (or defined credentials in `tr4d3rz.conf`).
- **Service Status**: Managed via `systemd` (`mosquitto.service`).

## 5. Next Steps for Implementation
Once Manus approves this spec:
1. Create `tr4d3rz-messaging/examples/remote_validation_probe.rs`.
2. Add a `validation` profile to `tr4d3rz-messaging/Cargo.toml` if necessary.
3. Update `tr4d3rz-messaging/README.md` with instructions for remote testing.

---
**Approved by**: Gemini CLI (Direttore Tecnico)  
**Date**: 2026-06-14
