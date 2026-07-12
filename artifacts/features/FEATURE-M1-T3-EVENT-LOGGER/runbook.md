# Runbook — M1-T3 Event Logger

**Component**: `tr4d3rz_persistence::EventLogger`  
**Criticality**: High (data loss impacts Observatory and replay)

---

## Error Codes

| Code | Message | Meaning |
|---|---|---|
| E001 | Database error: unable to open | DB file permissions or path invalid |
| E002 | Integrity check failed | DB corruption detected on startup |
| E003 | Disk space low | <100MB available, inserts failing |
| E004 | Serialization error | CBOR decode failed (schema mismatch) |

---

## Expected Logs

### Success Path
```
INFO: Event logger initialized (DB: /var/tr4d3rz/events.db)
INFO: Integrity check: ok
INFO: WAL mode enabled
DEBUG: Inserted event #1234 (type=genome_capsule)
```

### Failure Path (Disk Full)
```
ERROR: [E003] Disk space low: 50MB remaining (threshold: 100MB)
WARN: Event insertion failed, retry in 5s
```

### Failure Path (DB Corruption)
```
ERROR: [E002] Integrity check failed: database disk image is malformed
FATAL: Cannot start event logger, check backup
```

---

## Metrics to Monitor

| Metric | Normal Range | Alert Threshold | Action |
|---|---|---|---|
| Disk usage | <70% | >85% | Archive old events to Parquet |
| Insert latency | <10ms | >100ms | Check disk I/O, vacuum DB |
| Failed inserts/min | 0 | >5 | Investigate serialization errors |
| Event count growth | Linear | Sudden spike | Check for MQTT loop |

---

## Failure Modes

### 1. Database File Corruption
**Symptoms**: Startup fails with "integrity check failed"  
**Cause**: Power loss during write, hardware failure  
**Diagnosis Time**: <30 seconds (check logs for E002)  
**Recovery**:
```bash
# 1. Stop service
systemctl stop tr4d3rz-persistence

# 2. Restore from last backup
cp /backup/events_$(date -d yesterday +%Y%m%d).db /var/tr4d3rz/events.db

# 3. Restart
systemctl start tr4d3rz-persistence
```

---

### 2. Disk Space Exhaustion
**Symptoms**: Inserts fail with "disk space low"  
**Cause**: High event rate, no rotation policy  
**Diagnosis Time**: <1 minute (check `df -h`)  
**Recovery**:
```bash
# 1. Archive old events (older than 30 days)
sqlite3 /var/tr4d3rz/events.db \
  "SELECT * FROM events WHERE timestamp < datetime('now', '-30 days')" \
  | gzip > /archive/events_archive_$(date +%Y%m%d).csv.gz

# 2. Delete archived events
sqlite3 /var/tr4d3rz/events.db \
  "DELETE FROM events WHERE timestamp < datetime('now', '-30 days')"

# 3. Vacuum to reclaim space
sqlite3 /var/tr4d3rz/events.db "VACUUM"
```

---

### 3. MQTT Subscription Lag
**Symptoms**: Event count lower than expected, gaps in timeline  
**Cause**: Subscriber down during burst, QoS 0 on critical topics  
**Diagnosis Time**: <2 minutes (compare event count to broker stats)  
**Recovery**:
```bash
# Check broker stats for message count
mosquitto_sub -t 'tr4d3rz/#' -C 100 | wc -l

# If mismatch, check subscriber logs
journalctl -u tr4d3rz-persistence --since "10 minutes ago"

# Restart subscriber with QoS 1
# (permanent fix: update subscriber code to use QoS 1)
```

---

## Diagnostic Flowchart

```
Service not starting?
├─ Check logs for E002 (integrity)
│  └─ YES → Restore from backup
│  └─ NO → Check disk space
│     └─ <100MB? → Archive old events
│     └─ >100MB? → Check file permissions
│
Events missing?
├─ Check MQTT broker stats
│  └─ Mismatch? → Subscription lag (check QoS)
│  └─ Match? → Check event_type filtering (is topic pattern correct?)
│
Slow inserts (>100ms)?
└─ Check disk I/O (iostat)
   └─ High? → Consider SSD upgrade or WAL tuning
   └─ Low? → VACUUM database (fragmentation)
```

---

## 2 AM Failure Test: PASS

**Scenario**: Event logger crashes at 2 AM due to disk full  
**Question**: Can human diagnose cause in <2 minutes?

**Steps**:
1. Check systemd status: `systemctl status tr4d3rz-persistence` (10s)
2. Read last 20 log lines: `journalctl -u tr4d3rz-persistence -n 20` (20s)
3. See E003 error code → disk space issue (30s)
4. Verify: `df -h /var/tr4d3rz` → 98% full (10s)
5. **Total**: 70 seconds ✅ <2 minutes

**Action**: Archive events (5 min) or emergency delete (30s)

---

**Runbook Version**: 1.0  
**Last Updated**: 2026-07-10  
**Maintained By**: Implementation Agent (Claude Code)
