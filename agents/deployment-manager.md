# Role: Deployment Manager

**STATUS: STUB — attivo dopo M1 completion + SSH config RPi2**

## Constitutional Mapping
- CONSTITUTION.md: deployment manager
- Option C: claude subagent con accesso SSH al device target

## Quando diventa ACTIVE

Il Deployment Manager diventa operativo quando:
- M1 è completato
- SSH access al RPi2 è configurato (chiave SSH, IP, user)
- I servizi systemd per tr4d3rz sono definiti su RPi2
- La cross-compilation toolchain per `armv7-unknown-linux-gnueabihf` è disponibile

## Trigger Conditions (future)

L'Orchestratore spawna il Deployment Manager quando:
- Un release tag è creato su un repo tr4d3rz-*
- L'owner richiede esplicitamente un deploy su device
- Un firmware ESP8266 è pronto per il flash

## Responsabilità (future)

### Deploy su RPi2

1. `cargo build --release --target armv7-unknown-linux-gnueabihf` (cross-compilation)
2. `scp` del binario sul RPi2
3. `systemctl restart tr4d3rz-<service>` via SSH
4. Health check: MQTT heartbeat entro 30s dalla ripartenza
5. Rollback automatico se health check fallisce

### Deploy su ESP8266

1. Compilazione firmware con `cargo build --target xtensa-esp8266-none-elf`
2. Flash via `esptool.py` o `cargo espflash`
3. Verifica connessione MQTT post-flash

## Output Schema (futuro)

```json
{
  "status": "DEPLOYED | FAILED | ROLLBACK | STUB",
  "device": "RPi2 | ESP8266",
  "service": "tr4d3rz-persistence | tr4d3rz-messaging",
  "binary_size_bytes": 2048576,
  "health_check": "PASS | FAIL",
  "rollback_performed": false,
  "notes": ""
}
```

## Prerequisiti per attivazione

- [ ] SSH key configurata per RPi2 (`~/.ssh/tr4d3rz_rpi2`)
- [ ] IP e user RPi2 documentati in `.env.test` (NON committati)
- [ ] Toolchain `armv7-unknown-linux-gnueabihf` installata
- [ ] Servizi systemd definiti su RPi2
- [ ] Aggiornare questo file da STUB ad ACTIVE

## Brief Template (placeholder — non usare finché STATUS = STUB)

```
[STUB — Deployment Manager non ancora attivo. Vedere prerequisites in agents/deployment-manager.md]
```

*Maintainer: Claude Code (Orchestratore) — Creato: 2026-07-16 — Attivazione: post-M1*
