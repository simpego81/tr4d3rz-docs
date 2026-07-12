# Risks — M1-T3-EVENT-LOGGER

## Risk 1: SQLite Write Contention
**Probability**: Medium  
**Impact**: High (event loss if concurrent writes fail)  
**Mitigation**: 
- Use WAL mode (allows concurrent reads, single writer)
- Single writer thread with channel-based event queue
- Retry logic with exponential backoff (max 3 retries)

## Risk 2: Disk Space Exhaustion
**Probability**: Medium (long-running systems, high event rate)  
**Impact**: High (application crash, data loss)  
**Mitigation**:
- Monitor disk usage before each insert
- Fail gracefully if <100MB available
- Log rotation policy (future: archive old events to Parquet)
- Alert in runbook: "Check disk space weekly"

## Risk 3: MQTT Subscription Lag
**Probability**: Low  
**Impact**: Medium (events lost if subscriber down during burst)  
**Mitigation**:
- QoS 1 on critical topics (GenomeCapsule, FitnessResult)
- Broker persistence enabled (NanoMQ/Mosquitto)
- Reconnect logic with resume from last event ID

## Risk 4: CBOR Deserialization Failure
**Probability**: Low (schemas stable in M1)  
**Impact**: Medium (event skipped, logged as error)  
**Mitigation**:
- Store raw CBOR bytes even if deserialization fails
- Error table: failed_events(id, topic, raw_bytes, error_msg)
- Manual recovery via error table inspection

## Risk 5: Database File Corruption
**Probability**: Low (power loss, hardware failure)  
**Impact**: High (all historical data lost)  
**Mitigation**:
- SQLite integrity checks on startup (`PRAGMA integrity_check`)
- Periodic backups (daily cron job copying .db file)
- Runbook section: "How to restore from backup"
