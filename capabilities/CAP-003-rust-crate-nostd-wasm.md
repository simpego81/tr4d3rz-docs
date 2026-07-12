# CAP-003: Rust Crate Creation (no_std + WASM)

**Capability ID**: CAP-003  
**Category**: Development  
**Status**: ACTIVE  
**Created**: 2026-07-12  
**Last Updated**: 2026-07-12  
**Last Used**: M1-T2 (tr4d3rz-messaging)  
**Reuse Count**: 2 (M1-T1: tr4d3rz-core, M1-T2: tr4d3rz-messaging)

---

## Purpose

**What does this capability solve?**

Creating Rust crates that work across multiple targets: standard library (desktop/server), `no_std` (embedded ESP8266/STM32), and WASM (browser Observatory) requires specific configuration to avoid compilation errors and feature conflicts.

**Why is this capability reusable?**

Every TR4D3RZ Rust crate (`tr4d3rz-core`, `tr4d3rz-messaging`, `tr4d3rz-evolution`, `tr4d3rz-persistence`) must support multiple targets. Without this procedure, agents repeatedly rediscover the correct feature flags, dependency configuration, and compilation checks.

---

## Prerequisites

**Before using this capability, you must have**:

- [x] Rust 1.70+ installed
- [x] WASM target installed: `rustup target add wasm32-unknown-unknown`
- [x] Understanding of Cargo.toml feature flags
- [x] Understanding of `#![no_std]` vs `std` environments

**Knowledge dependencies**:

- [ADR-0002: Technology Stack](../adr/ADR-0002-technology-stack.md) — Rust as core language
- [TR4D3RZ Multi-Repository Structure](../README.md) — Repository boundaries

---

## Procedure

### Step 1: Initialize Crate with Multi-Target Structure

**What**: Create base crate structure with feature flags for std/no_std/WASM

**How**:
```bash
# Create new library crate
cargo new --lib tr4d3rz-<component>
cd tr4d3rz-<component>
```

**Expected output**: 
```
Created library `tr4d3rz-<component>` package
```

**Common issues**: None

---

### Step 2: Configure Cargo.toml with Feature Flags

**What**: Set up conditional compilation for std/no_std/WASM targets

**How**:

Edit `Cargo.toml`:

```toml
[package]
name = "tr4d3rz-<component>"
version = "0.1.0"
edition = "2021"

[dependencies]
# Core dependencies (no_std compatible)
serde = { version = "1.0", default-features = false, features = ["derive"] }
ciborium = { version = "0.2", default-features = false }

# Optional std-only dependencies
[dependencies.std-only-dep]
version = "1.0"
optional = true

[features]
default = ["std"]
std = [
    "serde/std",
    "ciborium/std",
    "std-only-dep"
]

[dev-dependencies]
# Test dependencies (always use std)
serde_json = "1.0"

[[example]]
name = "example_name"
required-features = ["std"]
```

**Expected output**: Valid Cargo.toml with feature flags

**Common issues**: 
- **Issue**: Dependency doesn't support `no_std`
- **Solution**: Find `no_std` alternative or make it optional with `std` feature

---

### Step 3: Configure lib.rs for Conditional std

**What**: Set up library root to conditionally use `std` or `no_std`

**How**:

Edit `src/lib.rs`:

```rust
//! TR4D3RZ <Component> Library
//!
//! Supports multiple targets:
//! - std (desktop/server)
//! - no_std (embedded ESP8266/STM32)
//! - WASM (browser Observatory)

#![cfg_attr(not(feature = "std"), no_std)]

// Conditional imports
#[cfg(feature = "std")]
extern crate std;

#[cfg(not(feature = "std"))]
extern crate core;

// Use prelude based on feature
#[cfg(feature = "std")]
use std::prelude::v1::*;

#[cfg(not(feature = "std"))]
use core::prelude::v1::*;

// Your module declarations
pub mod types;
pub mod utils;

#[cfg(feature = "std")]
pub mod std_only_feature;
```

**Expected output**: Library compiles with both `--features std` and `--no-default-features`

**Common issues**:
- **Issue**: `Vec`, `String`, `HashMap` not available in `no_std`
- **Solution**: Use `alloc` crate or redesign to use stack-allocated arrays

---

### Step 4: Test Multi-Target Compilation

**What**: Verify crate compiles for all targets

**How**:
```bash
# Test std (default)
cargo build

# Test no_std
cargo build --no-default-features

# Test WASM
cargo build --target wasm32-unknown-unknown --no-default-features

# Run tests (std only)
cargo test
```

**Expected output**:
```
   Compiling tr4d3rz-<component> v0.1.0
    Finished dev [unoptimized + debuginfo] target(s)
```

**Common issues**:
- **Issue**: `error[E0463]: can't find crate for 'std'` with `--no-default-features`
- **Solution**: Ensure `#![cfg_attr(not(feature = "std"), no_std)]` is at top of `lib.rs`

---

### Step 5: Add CBOR Serialization Support

**What**: Configure CBOR serialization for multi-target

**How**:

Add to types:
```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MyType {
    pub field1: u32,
    pub field2: [u8; 16],
}

#[cfg(feature = "std")]
impl MyType {
    /// Serialize to CBOR (std only)
    pub fn to_cbor(&self) -> Result<Vec<u8>, ciborium::ser::Error<std::io::Error>> {
        let mut buffer = Vec::new();
        ciborium::into_writer(self, &mut buffer)?;
        Ok(buffer)
    }

    /// Deserialize from CBOR (std only)
    pub fn from_cbor(bytes: &[u8]) -> Result<Self, ciborium::de::Error<std::io::Error>> {
        ciborium::from_reader(bytes)
    }
}
```

**Expected output**: CBOR serialization available in `std` mode, types still usable in `no_std`

**Common issues**:
- **Issue**: `Vec` not available in `no_std`
- **Solution**: CBOR serialization is `std`-only; embedded devices use preallocated buffers

---

### Step 6: Create Examples (std only)

**What**: Add usage examples demonstrating features

**How**:

Create `examples/basic_usage.rs`:
```rust
//! Basic usage example
//!
//! Run with: cargo run --example basic_usage

use tr4d3rz_component::MyType;

fn main() {
    let instance = MyType {
        field1: 42,
        field2: [0u8; 16],
    };

    // Serialize to CBOR
    let cbor = instance.to_cbor().expect("serialization failed");
    println!("CBOR size: {} bytes", cbor.len());

    // Deserialize from CBOR
    let recovered = MyType::from_cbor(&cbor).expect("deserialization failed");
    println!("Recovered: {:?}", recovered);
}
```

Run with:
```bash
cargo run --example basic_usage
```

**Expected output**:
```
CBOR size: 24 bytes
Recovered: MyType { field1: 42, field2: [0, 0, ...] }
```

**Common issues**: Examples require `std` feature — ensure `required-features = ["std"]` in Cargo.toml

---

### Step 7: Document Multi-Target Support

**What**: Add rustdoc explaining target support

**How**:

Add to `src/lib.rs`:
```rust
//! ## Target Support
//!
//! This crate supports three target environments:
//!
//! ### Standard Library (Desktop/Server)
//! ```bash
//! cargo build --features std
//! ```
//! Full functionality including CBOR serialization via `Vec`.
//!
//! ### no_std (Embedded ESP8266/STM32)
//! ```bash
//! cargo build --no-default-features
//! ```
//! Core types only. CBOR serialization requires preallocated buffers.
//!
//! ### WASM (Browser Observatory)
//! ```bash
//! cargo build --target wasm32-unknown-unknown --no-default-features
//! ```
//! Core types available for browser-side usage.
```

Generate docs:
```bash
cargo doc --open
```

**Expected output**: Documentation site opens showing multi-target information

**Common issues**: None

---

## Expected Outcomes

**After completing this capability, you should have**:

- ✅ Rust crate that compiles with `--features std`
- ✅ Rust crate that compiles with `--no-default-features` (no_std)
- ✅ Rust crate that compiles for `wasm32-unknown-unknown`
- ✅ CBOR serialization available in std mode
- ✅ Working examples demonstrating usage
- ✅ Rustdoc explaining target support

**Validation criteria**:

- [ ] `cargo build` succeeds (std)
- [ ] `cargo build --no-default-features` succeeds (no_std)
- [ ] `cargo build --target wasm32-unknown-unknown --no-default-features` succeeds (WASM)
- [ ] `cargo test` passes all tests
- [ ] `cargo doc` generates documentation
- [ ] Examples run successfully

---

## Examples

### Example 1: tr4d3rz-core (M1-T1)

**Context**: First shared types crate for TR4D3RZ

**Implementation**:
```toml
[features]
default = ["std"]
std = ["serde/std", "ciborium/std"]
```

```rust
#![cfg_attr(not(feature = "std"), no_std)]

pub mod ohlcv;
pub mod genome;
pub mod fitness;
```

**Result**: 
- Compiled for ESP8266 (no_std)
- Compiled for browser (WASM)
- Full functionality on desktop (std)

---

### Example 2: tr4d3rz-messaging (M1-T2)

**Context**: MQTT client library needing std for `rumqttc`

**Implementation**:
```toml
[features]
default = ["std"]
std = ["serde/std", "ciborium/std", "rumqttc"]

[dependencies.rumqttc]
version = "0.24"
optional = true
```

**Result**:
- Core message types available in no_std (for embedded to validate messages)
- Full MQTT client only in std mode (desktop/server)

---

## Common Issues and Troubleshooting

### Issue 1: "can't find crate for 'std'" in no_std build

**Symptoms**: 
```
error[E0463]: can't find crate for `std`
```

**Cause**: Missing `#![no_std]` attribute when building without std

**Solution**: Ensure `src/lib.rs` starts with:
```rust
#![cfg_attr(not(feature = "std"), no_std)]
```

---

### Issue 2: Vec/String not available in no_std

**Symptoms**:
```
error[E0433]: failed to resolve: use of undeclared crate or module `std`
```

**Cause**: Using `Vec`, `String`, `HashMap` without std

**Solution**: 
- Option 1: Enable `alloc` crate (requires allocator on embedded)
- Option 2: Use fixed-size arrays (`[u8; N]`) instead of `Vec<u8>`
- Option 3: Make feature `std`-only

```rust
#[cfg(feature = "std")]
pub fn to_vec(&self) -> Vec<u8> { /* ... */ }
```

---

### Issue 3: WASM compilation fails with missing symbols

**Symptoms**:
```
error: linking with `rust-lld` failed: exit status: 1
```

**Cause**: Trying to link std-only dependencies in WASM build

**Solution**: Ensure WASM builds use `--no-default-features`:
```bash
cargo build --target wasm32-unknown-unknown --no-default-features
```

And verify `std`-only deps are properly gated:
```toml
[dependencies.std-only-dep]
version = "1.0"
optional = true
```

---

## Related Capabilities

- [CAP-002: CBOR Serialization Workflow](CAP-002-cbor-serialization.md) — CBOR encoding for multi-target types
- [CAP-001: MQTT Topic Validation](CAP-001-mqtt-topic-validation.md) — Message validation in no_std contexts

---

## History

**Created**: 2026-07-12 by Librarian Agent (Claude Code)  
- Extracted from M1-T1 (tr4d3rz-core) and M1-T2 (tr4d3rz-messaging)
- Pattern used successfully for multi-target Rust crates

---

## Maintenance Notes

**Maintainer**: Librarian Agent

**Review frequency**: After each new Rust crate creation

**Deprecation criteria**: If Rust ecosystem changes feature flag patterns or WASM compilation model changes significantly

**Known Variations**:
- Some crates may need `alloc` feature for embedded heap usage
- Some crates may have platform-specific implementations (MQTT only on std, GPIO only on embedded)

---

**Capability Version**: 1.0  
**Last Updated**: 2026-07-12

