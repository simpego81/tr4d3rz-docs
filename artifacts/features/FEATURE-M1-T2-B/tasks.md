# IMPLEMENTATION TASKS: FEATURE-M1-T2-B

## 1. Infrastructure Setup
- [x] Ensure `.env.test` is in `.gitignore`.
- [x] Define standard for `TR4D3RZ_BROKER_IP`.

## 2. Code Implementation (`tr4d3rz-messaging`)
- [x] Add `dotenvy` to `[dev-dependencies]` in `Cargo.toml`.
- [x] Implement `examples/remote_validation_probe.rs`.
- [x] Use `rumqttc::AsyncClient` with manual event loop polling.
- [x] Implement CBOR serialization/deserialization for `NodeStatus`.

## 3. Documentation
- [x] Add "Remote Validation" section to `README.md`.
- [x] Document exit codes and usage instructions.

## 4. Verification Gate
- [x] Compile check (No warnings).
- [x] Hardware loopback test (Verified PC ↔ RPi connection).
