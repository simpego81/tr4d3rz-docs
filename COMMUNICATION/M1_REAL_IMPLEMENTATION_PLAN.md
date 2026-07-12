# TR4D3RZ M1 - Real Implementation Plan

**Status**: Ready to Start  
**Date**: 2026-06-05  
**Milestone**: M1 - Foundational Backbone Single RPi2  
**Prepared by**: Claude Code

---

## Executive Summary

Following successful validation of the MVP Browser Demo, we are ready to implement the **real M1 Foundational Backbone** on actual hardware and production-ready Rust code.

**Key Changes from Demo**:
- ✅ Real MQTT broker (NanoMQ on Raspberry Pi 2)
- ✅ Production Rust code (not mock JavaScript)
- ✅ Real CBOR serialization (not JSON)
- ✅ Actual hardware targets (RPi2, ESP8266)
- ✅ Proper error handling and logging
- ✅ Systemd services for production deployment

---

## M1 Task Status

| Task ID | Repository | Owner | Status | Dependencies | Priority |
|---------|------------|-------|--------|--------------|----------|
| **M1-T0** | tr4d3rz-docs | Manus | ✅ COMPLETED | None | N/A |
| **M1-T1** | tr4d3rz-core | Claude Code | ✅ COMPLETED | M1-T0 | N/A |
| **M1-T2** | tr4d3rz-messaging | Claude Code | 🔲 READY | M1-T0, M1-T1 | **HIGH** |
| **M1-T3** | tr4d3rz-persistence | Claude Code | 🔲 BLOCKED | M1-T0, M1-T1 | MEDIUM |
| **M1-T4** | tr4d3rz-evolution | Claude Code | 🔲 BLOCKED | M1-T1, M1-T2 | MEDIUM |
| **M1-T5** | tr4d3rz-embedded | GitHub Copilot | 🔲 BLOCKED | M1-T1, M1-T2 | LOW |
| **M1-T6** | tr4d3rz-observatory | Gemini CLI | 🔲 BLOCKED | M1-T2, M1-T3 | LOW |
| **M1-T7** | Cross-repo | Gemini CLI | 🔲 BLOCKED | M1-T1..M1-T6 | LOW |

**Next Task**: **M1-T2** (tr4d3rz-messaging)

---

## M1-T2: tr4d3rz-messaging Implementation Plan

### Objective

Implement MQTT messaging infrastructure for Raspberry Pi 2, including:
- NanoMQ broker setup
- Rust MQTT client library wrapper
- Topic routing and validation
- Message serialization/deserialization (CBOR)
- Integration tests with real broker

### Deliverables

1. **NanoMQ Broker Configuration**
   - Installation script for Raspberry Pi 2
   - Configuration file (`nanomq.conf`)
   - Systemd service unit
   - Health check script

2. **Rust MQTT Library** (`tr4d3rz_messaging` crate)
   - MQTT client wrapper (based on `rumqttc`)
   - Topic builder/validator
   - Message publisher with CBOR serialization
   - Message subscriber with CBOR deserialization
   - Connection pool management
   - Reconnection logic

3. **Testing Suite**
   - Unit tests for topic validation
   - Integration tests with NanoMQ
   - CBOR roundtrip tests
   - Connection failure tests

4. **Documentation**
   - API documentation (rustdoc)
   - Setup guide for Raspberry Pi 2
   - Example programs

### Technical Specifications

#### 1. NanoMQ Broker Setup

**Target Hardware**: Raspberry Pi 2 Model B (ARMv7, 1GB RAM)

**Installation**:
```bash
# On Raspberry Pi 2 (Debian/Raspbian)
sudo apt-get update
sudo apt-get install -y build-essential cmake

# Clone NanoMQ
git clone https://github.com/nanomq/nanomq.git
cd nanomq
git submodule update --init --recursive

# Build for ARMv7
mkdir build && cd build
cmake -DNNG_ENABLE_TLS=ON ..
make -j4
sudo make install
```

**Configuration** (`/etc/nanomq/nanomq.conf`):
```conf
# NanoMQ Configuration for TR4D3RZ M1

mqtt {
    url = "nmq-tcp://0.0.0.0:1883"
    max_packet_size = 256KB
    max_mqueue_len = 2048
    retry_interval = 10s
    keepalive_backoff = 1250
}

websocket {
    enable = true
    url = "nmq-ws://0.0.0.0:9001/mqtt"
}

log {
    level = info
    file = "/var/log/nanomq/nanomq.log"
}

auth {
    enable = false  # MVP: no auth
}
```

**Systemd Service** (`/etc/systemd/system/nanomq.service`):
```ini
[Unit]
Description=NanoMQ MQTT Broker for TR4D3RZ
After=network.target

[Service]
Type=simple
User=nanomq
Group=nanomq
ExecStart=/usr/local/bin/nanomq start --conf /etc/nanomq/nanomq.conf
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

#### 2. Rust MQTT Library Architecture

**Crate Structure**:
```
tr4d3rz-messaging/
├── Cargo.toml
├── src/
│   ├── lib.rs              # Public API
│   ├── client.rs           # MQTT client wrapper
│   ├── topic.rs            # Topic builder/validator
│   ├── publisher.rs        # Message publisher
│   ├── subscriber.rs       # Message subscriber
│   ├── error.rs            # Error types
│   └── config.rs           # Configuration
├── examples/
│   ├── publish_capsule.rs
│   ├── subscribe_fitness.rs
│   └── roundtrip_test.rs
└── tests/
    ├── integration_test.rs
    └── cbor_test.rs
```

**Dependencies** (`Cargo.toml`):
```toml
[package]
name = "tr4d3rz-messaging"
version = "0.1.0"
edition = "2021"

[dependencies]
tr4d3rz_core = { path = "../tr4d3rz-core" }
rumqttc = "0.24"
tokio = { version = "1.35", features = ["full"] }
ciborium = "0.2"
thiserror = "1.0"
tracing = "0.1"
tracing-subscriber = "0.3"
serde = { version = "1.0", features = ["derive"] }

[dev-dependencies]
tokio-test = "0.4"
```

**Public API** (`src/lib.rs`):
```rust
pub use client::MqttClient;
pub use topic::{Topic, TopicBuilder};
pub use publisher::Publisher;
pub use subscriber::{Subscriber, MessageHandler};
pub use error::{MessagingError, Result};
pub use config::BrokerConfig;
```

**Topic Builder** (`src/topic.rs`):
```rust
/// Topic builder for TR4D3RZ MQTT topics
pub struct TopicBuilder;

impl TopicBuilder {
    /// tr4d3rz/node/{node_id}/capsule/in
    pub fn capsule_in(node_id: &str) -> Topic {
        Topic::new(format!("tr4d3rz/node/{}/capsule/in", node_id))
    }

    /// tr4d3rz/ecosystem/fitness/{agent_id}
    pub fn fitness(agent_id: &str) -> Topic {
        Topic::new(format!("tr4d3rz/ecosystem/fitness/{}", agent_id))
    }

    /// tr4d3rz/node/{node_id}/status
    pub fn node_status(node_id: &str) -> Topic {
        Topic::new(format!("tr4d3rz/node/{}/status", node_id))
    }

    /// tr4d3rz/data/ohlcv/history/{isin}
    pub fn ohlcv_history(isin: &str) -> Topic {
        Topic::new(format!("tr4d3rz/data/ohlcv/history/{}", isin))
    }
}

pub struct Topic {
    inner: String,
}

impl Topic {
    pub fn new(topic: String) -> Self {
        Self { inner: topic }
    }

    /// Validate topic matches TR4D3RZ conventions
    pub fn validate(&self) -> Result<()> {
        if !self.inner.starts_with("tr4d3rz/") {
            return Err(MessagingError::InvalidTopic(
                "Topic must start with 'tr4d3rz/'".to_string()
            ));
        }
        Ok(())
    }

    pub fn as_str(&self) -> &str {
        &self.inner
    }
}
```

**Publisher** (`src/publisher.rs`):
```rust
use tr4d3rz_core::GenomeCapsule;
use rumqttc::{AsyncClient, QoS};
use ciborium;

pub struct Publisher {
    client: AsyncClient,
}

impl Publisher {
    pub fn new(client: AsyncClient) -> Self {
        Self { client }
    }

    /// Publish a genome capsule with CBOR serialization
    pub async fn publish_capsule(
        &self,
        topic: &Topic,
        capsule: &GenomeCapsule,
    ) -> Result<()> {
        // Serialize to CBOR
        let mut bytes = Vec::new();
        ciborium::ser::into_writer(capsule, &mut bytes)
            .map_err(|e| MessagingError::Serialization(e.to_string()))?;

        // Publish with QoS 1
        self.client
            .publish(topic.as_str(), QoS::AtLeastOnce, false, bytes)
            .await
            .map_err(|e| MessagingError::PublishFailed(e.to_string()))?;

        Ok(())
    }

    /// Publish node status (JSON for MVP)
    pub async fn publish_status(
        &self,
        topic: &Topic,
        status: &NodeStatus,
    ) -> Result<()> {
        let json = serde_json::to_string(status)
            .map_err(|e| MessagingError::Serialization(e.to_string()))?;

        self.client
            .publish(topic.as_str(), QoS::AtMostOnce, false, json)
            .await
            .map_err(|e| MessagingError::PublishFailed(e.to_string()))?;

        Ok(())
    }
}
```

**Subscriber** (`src/subscriber.rs`):
```rust
use tr4d3rz_core::FitnessResult;
use rumqttc::{AsyncClient, Event, Packet, QoS};
use tokio::sync::mpsc;

pub trait MessageHandler: Send + Sync {
    async fn handle_fitness(&self, fitness: FitnessResult);
    async fn handle_capsule(&self, capsule: GenomeCapsule);
}

pub struct Subscriber {
    client: AsyncClient,
}

impl Subscriber {
    pub fn new(client: AsyncClient) -> Self {
        Self { client }
    }

    /// Subscribe to fitness results
    pub async fn subscribe_fitness(&self, agent_id: &str) -> Result<()> {
        let topic = TopicBuilder::fitness(agent_id);
        self.client
            .subscribe(topic.as_str(), QoS::AtLeastOnce)
            .await
            .map_err(|e| MessagingError::SubscribeFailed(e.to_string()))?;

        Ok(())
    }

    /// Event loop to handle incoming messages
    pub async fn run(&mut self, handler: Box<dyn MessageHandler>) -> Result<()> {
        loop {
            match self.eventloop.poll().await {
                Ok(Event::Incoming(Packet::Publish(p))) => {
                    // Deserialize based on topic
                    if p.topic.contains("/fitness/") {
                        let fitness: FitnessResult = ciborium::de::from_reader(&p.payload[..])
                            .map_err(|e| MessagingError::Deserialization(e.to_string()))?;
                        handler.handle_fitness(fitness).await;
                    } else if p.topic.contains("/capsule/in") {
                        let capsule: GenomeCapsule = ciborium::de::from_reader(&p.payload[..])
                            .map_err(|e| MessagingError::Deserialization(e.to_string()))?;
                        handler.handle_capsule(capsule).await;
                    }
                }
                Ok(_) => {}
                Err(e) => {
                    tracing::error!("MQTT error: {:?}", e);
                    return Err(MessagingError::ConnectionLost(e.to_string()));
                }
            }
        }
    }
}
```

#### 3. Integration Tests

**Test with Real Broker** (`tests/integration_test.rs`):
```rust
#[tokio::test]
async fn test_publish_subscribe_roundtrip() {
    // Start NanoMQ broker (assume running on localhost:1883)
    let config = BrokerConfig::default();
    let client = MqttClient::connect(&config).await.unwrap();

    let publisher = client.publisher();
    let mut subscriber = client.subscriber();

    // Subscribe to fitness topic
    subscriber.subscribe_fitness("test-agent").await.unwrap();

    // Publish a fitness result
    let fitness = FitnessResult::ok(
        Utc::now().timestamp_millis() as u64,
        "test-node".to_string(),
        "test-agent".to_string(),
        "test-hash".to_string(),
        0.85,
        None,
    );

    let topic = TopicBuilder::fitness("test-agent");
    publisher.publish_fitness(&topic, &fitness).await.unwrap();

    // Receive and verify
    let received = subscriber.recv_fitness().await.unwrap();
    assert_eq!(received.fitness, 0.85);
}
```

### Implementation Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Phase 1**: NanoMQ Setup | 2h | Broker running on RPi2 |
| **Phase 2**: Rust Library Scaffold | 2h | Crate structure, Cargo.toml |
| **Phase 3**: Topic Builder | 1h | Topic validation logic |
| **Phase 4**: Publisher Implementation | 3h | CBOR serialization, publish methods |
| **Phase 5**: Subscriber Implementation | 3h | CBOR deserialization, event loop |
| **Phase 6**: Integration Tests | 2h | Roundtrip tests with NanoMQ |
| **Phase 7**: Documentation | 2h | Rustdoc, examples, setup guide |

**Total**: 15 hours (~2 days)

---

## Next Tasks After M1-T2

### M1-T3: tr4d3rz-persistence

**Objective**: SQLite event logger on Raspberry Pi 2

**Dependencies**:
- ✅ M1-T1 (core types)
- ✅ M1-T2 (MQTT client)

**Key Features**:
- Subscribe to `tr4d3rz/#` (all events)
- Insert events into SQLite database
- Append-only schema (no updates/deletes)
- Query API for Observatory

### M1-T4: tr4d3rz-evolution

**Objective**: Evolution node that generates genome capsules

**Dependencies**:
- ✅ M1-T1 (core types)
- ✅ M1-T2 (MQTT client)

**Key Features**:
- Generate mock genome capsules (MVP)
- Publish to `tr4d3rz/node/{esp_id}/capsule/in`
- Subscribe to `tr4d3rz/ecosystem/fitness/+`
- Log fitness results

### M1-T5: tr4d3rz-embedded

**Objective**: ESP8266 firmware for fitness evaluation

**Dependencies**:
- ✅ M1-T1 (data contracts reference)
- ✅ M1-T2 (MQTT topics)

**Key Features**:
- Subscribe to `tr4d3rz/node/esp8266-01/capsule/in`
- Simulate FSM evaluation
- Publish to `tr4d3rz/ecosystem/fitness/{agent_id}`
- C/Arduino code (GitHub Copilot)

---

## Hardware Setup Requirements

### Raspberry Pi 2 Setup

**OS**: Raspberry Pi OS Lite (Debian-based)

**Initial Setup**:
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install development tools
sudo apt-get install -y build-essential cmake git curl

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Clone TR4D3RZ repositories
cd /home/pi
git clone https://github.com/simpego81/tr4d3rz-core.git
git clone https://github.com/simpego81/tr4d3rz-messaging.git
git clone https://github.com/simpego81/tr4d3rz-persistence.git
git clone https://github.com/simpego81/tr4d3rz-evolution.git
```

**Network Configuration**:
- Static IP: 192.168.1.100 (or configure DHCP reservation)
- Hostname: `rpi2-tr4d3rz`
- Firewall: Allow ports 1883 (MQTT), 9001 (WebSocket)

### ESP8266 Setup

**Hardware**: NodeMCU V2 or Wemos D1 Mini

**Development Environment**:
- Arduino IDE or PlatformIO
- ESP8266 board support
- PubSubClient library (MQTT)
- ArduinoJson library

**Flash Instructions**: See `VSCODE_DEBUGGING_GUIDE.md` section 6.1

---

## Success Criteria

M1 is complete when:

1. ✅ NanoMQ broker running on Raspberry Pi 2
2. ✅ `tr4d3rz-messaging` crate publishes/subscribes successfully
3. ✅ CBOR serialization roundtrip tests pass
4. ✅ Evolution node publishes genome capsules
5. ✅ ESP8266 receives capsules and publishes fitness
6. ✅ Persistence node logs all events to SQLite
7. ✅ All nodes publish heartbeats every 5 seconds
8. ✅ System runs stably for 30+ minutes

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| NanoMQ compatibility issues on ARMv7 | HIGH | Test build on RPi2 early; fallback to Mosquitto |
| CBOR serialization bugs | MEDIUM | Extensive roundtrip tests; JSON fallback for debug |
| ESP8266 memory constraints | MEDIUM | Use CBOR, limit payload size, monitor heap |
| MQTT connection instability | LOW | Implement reconnection logic, exponential backoff |
| SQLite write contention | LOW | Use WAL mode, batch writes |

---

## Documentation Deliverables

1. **M1-T2 Implementation Log** (`tr4d3rz-messaging/COMMUNICATION/IMPLEMENTATION_LOG.md`)
2. **NanoMQ Setup Guide** (`tr4d3rz-messaging/docs/nanomq-setup.md`)
3. **API Documentation** (rustdoc - `cargo doc --open`)
4. **Integration Test Report** (`tr4d3rz-messaging/COMMUNICATION/TEST_REPORT.md`)

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Setup Raspberry Pi 2** hardware
3. **Start M1-T2** implementation
4. **Update TASK_QUEUE.md** as tasks progress

---

**Plan Status**: ✅ Ready for Implementation  
**Prepared by**: Claude Code  
**Approval**: Pending (Manus)  
**Start Date**: TBD
