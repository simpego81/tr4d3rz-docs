# TR4D3RZ - Visual Studio Code Debugging Guide

**Target**: Microsoft Visual Studio Code + GitHub Copilot  
**Date**: 2026-06-05  
**Audience**: Developers working on TR4D3RZ real MVP implementation  
**Scope**: Rust development, MQTT debugging, embedded targets, multi-repository workflow

---

## Table of Contents

1. [VS Code Setup](#1-vs-code-setup)
2. [Recommended Extensions](#2-recommended-extensions)
3. [Workspace Configuration](#3-workspace-configuration)
4. [Rust Debugging](#4-rust-debugging)
5. [MQTT Debugging](#5-mqtt-debugging)
6. [Embedded Targets (ESP8266/STM32)](#6-embedded-targets-esp8266stm32)
7. [Multi-Repository Workflow](#7-multi-repository-workflow)
8. [GitHub Copilot Tips](#8-github-copilot-tips)
9. [Common Issues and Solutions](#9-common-issues-and-solutions)
10. [Debugging Cheat Sheet](#10-debugging-cheat-sheet)

---

## 1. VS Code Setup

### 1.1 Prerequisites

**Required Tools**:
- **Visual Studio Code**: v1.85.0 or later
- **Rust**: Latest stable (install via [rustup](https://rustup.rs/))
- **Node.js**: v18+ (for MQTT testing tools)
- **Git**: Latest version

**Verify Installation**:
```bash
code --version      # Should show v1.85+
rustc --version     # Should show rustc 1.7x+
cargo --version     # Should show cargo 1.7x+
node --version      # Should show v18+
git --version       # Should show 2.x+
```

### 1.2 Initial Configuration

**Open Settings** (Ctrl+,) and configure:

```json
{
  // Editor
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "editor.tabSize": 4,
  "editor.insertSpaces": true,

  // Rust
  "rust-analyzer.checkOnSave.command": "clippy",
  "rust-analyzer.cargo.features": "all",
  "rust-analyzer.inlayHints.enable": true,

  // Files
  "files.exclude": {
    "**/target": true,
    "**/.git": true
  },

  // Terminal
  "terminal.integrated.defaultProfile.windows": "Git Bash",
  
  // Copilot
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "rust": true,
    "toml": true
  }
}
```

---

## 2. Recommended Extensions

### 2.1 Essential Extensions

Install these extensions from the VS Code marketplace:

| Extension | ID | Purpose |
|---|---|---|
| **rust-analyzer** | `rust-lang.rust-analyzer` | Rust language server, autocomplete, diagnostics |
| **CodeLLDB** | `vadimcn.vscode-lldb` | LLDB debugger for Rust |
| **Even Better TOML** | `tamasfe.even-better-toml` | TOML syntax highlighting for Cargo.toml |
| **Error Lens** | `usernamehm.errorlens` | Inline error/warning display |
| **GitHub Copilot** | `github.copilot` | AI pair programmer |
| **GitHub Copilot Chat** | `github.copilot-chat` | Chat interface for Copilot |
| **GitLens** | `eamodio.gitlens` | Enhanced Git integration |
| **Markdown All in One** | `yzhang.markdown-all-in-one` | Markdown editing |
| **PlantUML** | `jebbs.plantuml` | UML diagram preview |

**Install via CLI**:
```bash
code --install-extension rust-lang.rust-analyzer
code --install-extension vadimcn.vscode-lldb
code --install-extension tamasfe.even-better-toml
code --install-extension usernamehm.errorlens
code --install-extension github.copilot
code --install-extension github.copilot-chat
code --install-extension eamodio.gitlens
code --install-extension yzhang.markdown-all-in-one
code --install-extension jebbs.plantuml
```

### 2.2 Optional Extensions (MQTT/Embedded)

| Extension | ID | Purpose |
|---|---|---|
| **MQTT Explorer** | `shandilya1998.mqtt-explorer` | MQTT client GUI |
| **Serial Monitor** | `ms-vscode.vscode-serial-monitor` | Serial port monitor for embedded |
| **PlatformIO IDE** | `platformio.platformio-ide` | Embedded development (ESP8266/STM32) |
| **Cortex-Debug** | `marus25.cortex-debug` | ARM Cortex-M debugging |

**Install via CLI**:
```bash
code --install-extension shandilya1998.mqtt-explorer
code --install-extension ms-vscode.vscode-serial-monitor
code --install-extension platformio.platformio-ide
code --install-extension marus25.cortex-debug
```

---

## 3. Workspace Configuration

### 3.1 Multi-Root Workspace

TR4D3RZ is a multi-repository project. Create a workspace file to manage all repos:

**File**: `C:\projects\seq\tr4d3rz.code-workspace`

```json
{
  "folders": [
    {
      "path": "tr4d3rz-docs",
      "name": "📚 Docs (SSOT)"
    },
    {
      "path": "tr4d3rz-core",
      "name": "🧬 Core (Rust)"
    },
    {
      "path": "tr4d3rz-messaging",
      "name": "📡 Messaging (Rust)"
    },
    {
      "path": "tr4d3rz-evolution",
      "name": "🧪 Evolution (Rust)"
    },
    {
      "path": "tr4d3rz-persistence",
      "name": "💾 Persistence (Rust)"
    },
    {
      "path": "tr4d3rz-observatory",
      "name": "🌐 Observatory (TypeScript)"
    },
    {
      "path": "tr4d3rz-embedded",
      "name": "🔌 Embedded (C/Rust)"
    }
  ],
  "settings": {
    "rust-analyzer.linkedProjects": [
      "tr4d3rz-core/Cargo.toml",
      "tr4d3rz-messaging/Cargo.toml",
      "tr4d3rz-evolution/Cargo.toml",
      "tr4d3rz-persistence/Cargo.toml"
    ],
    "files.watcherExclude": {
      "**/target/**": true,
      "**/node_modules/**": true
    }
  },
  "launch": {
    "version": "0.2.0",
    "configurations": []
  }
}
```

**Open Workspace**:
```bash
code C:\projects\seq\tr4d3rz.code-workspace
```

### 3.2 Per-Repository .vscode/

Each Rust repository should have a `.vscode/` directory with:

**`.vscode/settings.json`**:
```json
{
  "rust-analyzer.check.allTargets": false,
  "rust-analyzer.cargo.target": null,
  "rust-analyzer.cargo.features": ["std"]
}
```

**`.vscode/launch.json`** (see section 4.2)

**`.vscode/tasks.json`** (see section 4.3)

---

## 4. Rust Debugging

### 4.1 Basic Rust Debugging Setup

#### Install CodeLLDB

The **CodeLLDB** extension provides LLDB integration for Rust debugging.

**Verify Installation**:
- Open Command Palette (Ctrl+Shift+P)
- Type "LLDB: Version" → Should show LLDB version

#### Enable Debug Symbols

Ensure `Cargo.toml` has debug profile configured:

```toml
[profile.dev]
opt-level = 0
debug = true

[profile.release]
opt-level = 3
debug = false
lto = true
```

### 4.2 Launch Configuration

**File**: `tr4d3rz-core/.vscode/launch.json`

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug unit tests",
      "cargo": {
        "args": [
          "test",
          "--no-run",
          "--lib",
          "--package=tr4d3rz_core"
        ],
        "filter": {
          "name": "tr4d3rz_core",
          "kind": "lib"
        }
      },
      "args": [],
      "cwd": "${workspaceFolder}"
    },
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug example (ohlcv_demo)",
      "cargo": {
        "args": [
          "build",
          "--example=ohlcv_demo",
          "--package=tr4d3rz_core"
        ],
        "filter": {
          "name": "ohlcv_demo",
          "kind": "example"
        }
      },
      "args": [],
      "cwd": "${workspaceFolder}"
    },
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug current file",
      "cargo": {
        "args": [
          "build",
          "--bin=${fileBasenameNoExtension}"
        ]
      },
      "args": [],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### 4.3 Tasks Configuration

**File**: `tr4d3rz-core/.vscode/tasks.json`

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "cargo",
      "command": "check",
      "problemMatcher": ["$rustc"],
      "group": "build",
      "label": "rust: cargo check"
    },
    {
      "type": "cargo",
      "command": "clippy",
      "args": ["--all-targets", "--all-features"],
      "problemMatcher": ["$rustc"],
      "group": "build",
      "label": "rust: cargo clippy"
    },
    {
      "type": "cargo",
      "command": "test",
      "args": ["--lib", "--", "--nocapture"],
      "problemMatcher": ["$rustc"],
      "group": "test",
      "label": "rust: cargo test"
    },
    {
      "type": "cargo",
      "command": "build",
      "args": ["--release"],
      "problemMatcher": ["$rustc"],
      "group": "build",
      "label": "rust: cargo build --release"
    },
    {
      "type": "shell",
      "command": "cargo",
      "args": ["build", "--target", "wasm32-unknown-unknown"],
      "problemMatcher": ["$rustc"],
      "label": "rust: build WASM"
    }
  ]
}
```

### 4.4 Debugging Workflow

1. **Set Breakpoints**: Click left gutter in code editor
2. **Start Debugging**: Press F5 or select configuration from Run menu
3. **Step Through Code**:
   - F10: Step Over
   - F11: Step Into
   - Shift+F11: Step Out
   - F5: Continue
4. **Inspect Variables**: Hover over variables or use Debug sidebar
5. **Evaluate Expressions**: Debug Console → type expression

### 4.5 Common Rust Debugging Commands

**Debug Console Commands** (during debug session):

```lldb
# Print variable
p variable_name

# Print with format
p/x variable_name  # Hex
p/t variable_name  # Binary
p/d variable_name  # Decimal

# Show type
ptype variable_name

# Backtrace
bt

# List source
list

# Set breakpoint
b main.rs:42

# Continue
c

# Step
s  # Step into
n  # Step over
finish  # Step out
```

---

## 5. MQTT Debugging

### 5.1 MQTT Tools Setup

#### Install MQTT.fx or MQTT Explorer

**Option 1: MQTT Explorer** (Recommended)
```bash
# Download from: https://mqtt-explorer.com/
# Or install via winget:
winget install MQTT-Explorer
```

**Option 2: MQTTX** (Cross-platform)
```bash
# Download from: https://mqttx.app/
```

#### Install Mosquitto CLI Tools

```bash
# Windows (via Chocolatey)
choco install mosquitto

# Or download from: https://mosquitto.org/download/

# Verify
mosquitto_pub --version
mosquitto_sub --version
```

### 5.2 Debugging MQTT Messages

#### Monitor All Topics

```bash
# Subscribe to all topics on localhost
mosquitto_sub -h localhost -p 1883 -t 'tr4d3rz/#' -v

# Subscribe with QoS 1
mosquitto_sub -h localhost -p 1883 -t 'tr4d3rz/#' -q 1 -v

# Save to file
mosquitto_sub -h localhost -p 1883 -t 'tr4d3rz/#' -v > mqtt_log.txt
```

#### Publish Test Messages

```bash
# Publish test OHLCV
mosquitto_pub -h localhost -p 1883 -t 'tr4d3rz/data/ohlcv/history/TEST' \
  -m '{"v":1,"type":"ohlcv_history","isin":"TEST","data":[]}'

# Publish test genome capsule
mosquitto_pub -h localhost -p 1883 -t 'tr4d3rz/node/esp8266-01/capsule/in' \
  -m '{"v":1,"agent_id":"test-001","generation":0}'
```

#### Monitor Specific Node

```bash
# Monitor only fitness results
mosquitto_sub -h localhost -p 1883 -t 'tr4d3rz/ecosystem/fitness/+' -v

# Monitor only status updates
mosquitto_sub -h localhost -p 1883 -t 'tr4d3rz/node/+/status' -v
```

### 5.3 MQTT Explorer Configuration

**Connect to Local Broker**:
1. Open MQTT Explorer
2. Click "+" to add connection
3. Configure:
   - **Name**: TR4D3RZ Local Broker
   - **Host**: localhost
   - **Port**: 1883
   - **Protocol**: mqtt://
   - **Client ID**: mqtt-explorer-debug
4. Click "Advanced" → Set "Auto-expand limit" to 5000
5. Click "Connect"

**Subscribe to All Topics**:
- In the tree view, subscribe to `tr4d3rz/#`
- Messages will appear in the tree structure

### 5.4 VS Code MQTT Extension

If you installed `shandilya1998.mqtt-explorer`:

1. Open Command Palette (Ctrl+Shift+P)
2. Type "MQTT: Connect"
3. Enter broker URL: `mqtt://localhost:1883`
4. View messages in "MQTT" panel

---

## 6. Embedded Targets (ESP8266/STM32)

### 6.1 ESP8266 Setup

#### Install PlatformIO

PlatformIO extension handles ESP8266 toolchain automatically.

**Initialize PlatformIO Project**:
```bash
cd tr4d3rz-embedded/esp8266
pio init --board nodemcuv2
```

**platformio.ini**:
```ini
[env:nodemcuv2]
platform = espressif8266
board = nodemcuv2
framework = arduino
monitor_speed = 115200
lib_deps = 
    PubSubClient  # MQTT library
    ArduinoJson
```

#### Upload and Monitor

```bash
# Build
pio run

# Upload to ESP8266
pio run --target upload

# Monitor serial output
pio device monitor --baud 115200
```

#### VS Code Debug Configuration

**File**: `tr4d3rz-embedded/.vscode/launch.json`

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "platformio-debug",
      "request": "launch",
      "name": "PlatformIO Debug (ESP8266)",
      "executable": ".pio/build/nodemcuv2/firmware.elf",
      "projectEnvName": "nodemcuv2",
      "toolchainBinDir": "${env:HOME}/.platformio/packages/toolchain-xtensa/bin",
      "preLaunchTask": {
        "type": "PlatformIO",
        "task": "Pre-Debug"
      }
    }
  ]
}
```

### 6.2 STM32 Setup

#### Install Cortex-Debug Extension

Already listed in section 2.2.

#### STM32 Debug Configuration

**File**: `tr4d3rz-embedded/.vscode/launch.json`

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "cortex-debug",
      "request": "launch",
      "name": "Debug STM32 (OpenOCD)",
      "cwd": "${workspaceFolder}",
      "executable": "./target/thumbv7em-none-eabihf/debug/stm32-firmware",
      "servertype": "openocd",
      "configFiles": [
        "interface/stlink.cfg",
        "target/stm32f1x.cfg"
      ],
      "device": "STM32F103",
      "svdFile": "${workspaceFolder}/STM32F103.svd"
    }
  ]
}
```

#### Build for STM32

```bash
# Add target
rustup target add thumbv7em-none-eabihf

# Build
cargo build --target thumbv7em-none-eabihf --release

# Flash with probe-rs
cargo flash --chip STM32F103C8 --release
```

### 6.3 Serial Debugging

#### Monitor Serial Output (ESP8266)

```bash
# Using PlatformIO
pio device monitor --baud 115200

# Using Arduino Serial Monitor
# Tools → Serial Monitor → Set baud to 115200

# Using VS Code Serial Monitor extension
# Ctrl+Shift+P → "Serial Monitor: Start"
```

#### Log to Serial

**ESP8266 (Arduino)**:
```cpp
void setup() {
  Serial.begin(115200);
  Serial.println("[DEBUG] Starting...");
}

void loop() {
  Serial.printf("[DEBUG] Heap: %d bytes\n", ESP.getFreeHeap());
  delay(1000);
}
```

**STM32 (Rust)**:
```rust
use cortex_m_semihosting::hprintln;

hprintln!("DEBUG: Starting...").unwrap();
```

---

## 7. Multi-Repository Workflow

### 7.1 Opening Multiple Repositories

**Option 1: Multi-Root Workspace** (Recommended)

Use the workspace file created in section 3.1:
```bash
code C:\projects\seq\tr4d3rz.code-workspace
```

**Option 2: Multiple Windows**

Open each repository in a separate window:
```bash
code C:\projects\seq\tr4d3rz-core
code C:\projects\seq\tr4d3rz-messaging
```

### 7.2 Cross-Repository Navigation

**Using GitLens**:
1. Click "Source Control" icon (Ctrl+Shift+G)
2. GitLens shows history across all repos
3. Right-click commit → "Compare with Working Tree"

**Using Go to File**:
1. Press Ctrl+P
2. Type filename from any repository
3. Workspace search includes all folders

### 7.3 Debugging Across Repositories

When debugging `tr4d3rz-messaging` that depends on `tr4d3rz-core`:

**Cargo.toml**:
```toml
[dependencies]
tr4d3rz_core = { path = "../tr4d3rz-core" }
```

**Enable Source Debugging**:
- CodeLLDB will automatically step into `tr4d3rz_core` source
- Set breakpoints in either repository

---

## 8. GitHub Copilot Tips

### 8.1 Enabling Copilot

**Prerequisites**:
- GitHub Copilot subscription
- Signed in to GitHub in VS Code (Accounts icon in bottom left)

**Verify Copilot is Active**:
- Look for Copilot icon in status bar (bottom right)
- Should show "Ready"

### 8.2 Using Copilot for Rust

#### Inline Suggestions

Type a comment describing what you want:
```rust
// Generate a function that serializes GenomeCapsule to CBOR
```
Copilot will suggest the function. Press Tab to accept.

#### Copilot Chat

Open Copilot Chat (Ctrl+Shift+I) and ask:
```
@workspace How do I serialize a Rust struct to CBOR using ciborium?
```

#### Explain Code

Select code → Right-click → "Copilot: Explain This"

#### Generate Tests

```rust
// Generate unit tests for this function
pub fn generate_mock_ohlcv(bars: usize) -> OhlcvHistory {
    // ...
}
```

### 8.3 Copilot for MQTT/Protocols

Ask Copilot to generate code from specs:

**In Chat**:
```
Generate Rust code to publish a GenomeCapsule to MQTT topic 
tr4d3rz/node/{node_id}/capsule/in using the rumqttc library.
The GenomeCapsule struct should match the schema in 
@tr4d3rz-docs/protocols/MVP_INTERFACE_CONTRACTS.md
```

### 8.4 Copilot for Debugging

**Ask Copilot to explain errors**:
```
@workspace Why am I getting "cannot borrow as mutable" error on line 42?
```

**Ask for debugging strategies**:
```
How can I debug a deadlock in Rust async code?
```

---

## 9. Common Issues and Solutions

### 9.1 Rust Analyzer Issues

#### Issue: "rust-analyzer failed to load workspace"

**Solution**:
```bash
# Restart rust-analyzer
Ctrl+Shift+P → "Rust Analyzer: Restart Server"

# Or reload window
Ctrl+Shift+P → "Developer: Reload Window"
```

#### Issue: "proc macro loading failed"

**Solution**:
```bash
# Update rust-analyzer
rustup update
Ctrl+Shift+P → "Extensions: Update All Extensions"
```

### 9.2 LLDB Debugging Issues

#### Issue: "lldb: command not found"

**Solution**:
```bash
# Install CodeLLDB extension
code --install-extension vadimcn.vscode-lldb

# Or manually download LLDB
# Windows: https://llvm.org/builds/
```

#### Issue: Breakpoints not hitting

**Solution**:
1. Ensure debug symbols are enabled (`debug = true` in Cargo.toml)
2. Build in debug mode: `cargo build` (not `cargo build --release`)
3. Restart debugger (Ctrl+Shift+F5)

### 9.3 MQTT Connection Issues

#### Issue: "Connection refused" when connecting to localhost:1883

**Solution**:
```bash
# Check if broker is running
netstat -an | grep 1883

# Start demo broker
cd tr4d3rz-docs/specs/mvp-browser-demo
npm start

# Or install Mosquitto broker
choco install mosquitto
mosquitto -v
```

#### Issue: Messages not appearing in MQTT Explorer

**Solution**:
1. Verify topic matches subscription pattern
2. Check QoS level (use QoS 0 for testing)
3. Verify broker is running: `mosquitto_sub -h localhost -t '$SYS/#'`

### 9.4 Embedded Target Issues

#### Issue: "espcomm_upload_mem failed" (ESP8266)

**Solution**:
```bash
# Put ESP8266 in flash mode:
# 1. Hold FLASH button
# 2. Press RESET button
# 3. Release RESET
# 4. Release FLASH
# 5. Upload again

pio run --target upload
```

#### Issue: "Error: No probe found" (STM32)

**Solution**:
```bash
# Check ST-Link connection
lsusb  # Linux
# Should show "STMicroelectronics ST-LINK/V2"

# Update ST-Link firmware
# Download from: https://www.st.com/en/development-tools/stsw-link007.html
```

---

## 10. Debugging Cheat Sheet

### 10.1 Keyboard Shortcuts

| Action | Windows/Linux | macOS |
|---|---|---|
| **Start Debugging** | F5 | F5 |
| **Stop Debugging** | Shift+F5 | Shift+F5 |
| **Restart Debugging** | Ctrl+Shift+F5 | Cmd+Shift+F5 |
| **Step Over** | F10 | F10 |
| **Step Into** | F11 | F11 |
| **Step Out** | Shift+F11 | Shift+F11 |
| **Continue** | F5 | F5 |
| **Toggle Breakpoint** | F9 | F9 |
| **Open Debug Console** | Ctrl+Shift+Y | Cmd+Shift+Y |
| **Run Task** | Ctrl+Shift+B | Cmd+Shift+B |
| **Open Terminal** | Ctrl+` | Ctrl+` |

### 10.2 Rust Quick Commands

```bash
# Check code
cargo check

# Run clippy
cargo clippy --all-targets

# Run tests
cargo test

# Run tests with output
cargo test -- --nocapture

# Build for release
cargo build --release

# Build for WASM
cargo build --target wasm32-unknown-unknown

# Format code
cargo fmt

# Update dependencies
cargo update

# Clean build artifacts
cargo clean
```

### 10.3 MQTT Quick Commands

```bash
# Subscribe to all TR4D3RZ topics
mosquitto_sub -h localhost -t 'tr4d3rz/#' -v

# Publish test message
mosquitto_pub -h localhost -t 'tr4d3rz/test' -m '{"hello":"world"}'

# Monitor broker stats
mosquitto_sub -h localhost -t '$SYS/#' -v

# Test connection
mosquitto_pub -h localhost -t 'test' -m 'ping'
```

### 10.4 Git Quick Commands

```bash
# Status all repos
for d in tr4d3rz-*; do (cd "$d" && echo "=== $d ===" && git status -s); done

# Pull all repos
for d in tr4d3rz-*; do (cd "$d" && echo "=== $d ===" && git pull); done

# Commit with message
git add .
git commit -m "feat: implement genome capsule serialization"

# Push
git push origin main
```

---

## 11. TR4D3RZ-Specific Debugging Workflows

### 11.1 Debugging Genome Capsule Serialization

**Scenario**: Testing CBOR serialization of GenomeCapsule

**Steps**:
1. Open `tr4d3rz-core/src/genome.rs`
2. Set breakpoint in `GenomeCapsule::new()`
3. Create test in `tests/` directory:
   ```rust
   #[test]
   fn test_capsule_cbor_roundtrip() {
       let capsule = GenomeCapsule::new(...);
       let bytes = ciborium::ser::into_writer(&capsule, Vec::new()).unwrap();
       let decoded: GenomeCapsule = ciborium::de::from_reader(&bytes[..]).unwrap();
       assert_eq!(capsule.agent_id, decoded.agent_id);
   }
   ```
4. Run test in debugger: F5 → Select "Debug unit tests"
5. Step through serialization logic

### 11.2 Debugging MQTT Message Flow

**Scenario**: Evolution node publishes capsule, ESP8266 doesn't receive

**Steps**:
1. **Terminal 1**: Start MQTT broker
   ```bash
   cd tr4d3rz-docs/specs/mvp-browser-demo
   npm start
   ```

2. **Terminal 2**: Monitor all topics
   ```bash
   mosquitto_sub -h localhost -t 'tr4d3rz/#' -v
   ```

3. **Terminal 3**: Run evolution node
   ```bash
   cd tr4d3rz-evolution
   cargo run
   ```

4. **Check Terminal 2**: Should see capsule messages
5. If not, check:
   - Topic name matches spec
   - QoS level
   - Broker connection status

### 11.3 Debugging Embedded Fitness Evaluation

**Scenario**: ESP8266 receives capsule but doesn't publish fitness

**Steps**:
1. Connect ESP8266 via USB
2. Open Serial Monitor (Ctrl+Shift+P → "Serial Monitor")
3. Set baud to 115200
4. Add debug prints in ESP8266 code:
   ```cpp
   void onMqttMessage(char* topic, byte* payload, unsigned int length) {
     Serial.printf("[DEBUG] Received on %s: %d bytes\n", topic, length);
     // ... process message
     Serial.println("[DEBUG] Publishing fitness...");
     client.publish("tr4d3rz/ecosystem/fitness/agent-001", fitnessJson);
     Serial.println("[DEBUG] Published");
   }
   ```
5. Upload code: `pio run --target upload`
6. Watch serial output for debug messages

---

## 12. Best Practices

### 12.1 Code Organization

- Keep debug code in `#[cfg(debug_assertions)]` blocks
- Use `log` crate for structured logging
- Create `examples/` for manual testing

**Example**:
```rust
#[cfg(debug_assertions)]
{
    eprintln!("[DEBUG] Capsule: {:?}", capsule);
}
```

### 12.2 Testing Strategy

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test MQTT message flow with demo broker
3. **Embedded Tests**: Test on real hardware (ESP8266/STM32)
4. **End-to-End Tests**: Run full evolution cycle

### 12.3 Version Control

- Commit after each working feature
- Use conventional commits: `feat:`, `fix:`, `docs:`
- Reference task IDs: `feat(core): implement genome serialization (M1-T1)`

---

## 13. Additional Resources

**Rust Debugging**:
- [Rust Debugging Guide](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [CodeLLDB Documentation](https://github.com/vadimcn/vscode-lldb)

**MQTT**:
- [MQTT.org](https://mqtt.org/)
- [Mosquitto Documentation](https://mosquitto.org/documentation/)

**Embedded**:
- [PlatformIO Docs](https://docs.platformio.org/)
- [Embedded Rust Book](https://docs.rust-embedded.org/book/)

**VS Code**:
- [VS Code Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [Tasks in VS Code](https://code.visualstudio.com/docs/editor/tasks)

---

**Document Version**: 1.0  
**Last Updated**: 2026-06-05  
**Maintained by**: Claude Code  
**For**: TR4D3RZ Development Team
