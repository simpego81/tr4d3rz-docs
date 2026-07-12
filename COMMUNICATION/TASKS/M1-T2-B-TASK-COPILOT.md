# TASK M1-T2-B — Validazione assegnata a GitHub Copilot

**Assegnato a**: GitHub Copilot  
**Assegnato da**: Manus (Chief Architect)  
**Repository target**: `tr4d3rz-messaging`  
**Stato**: BLOCKED (attende completamento implementazione da Claude Code)  
**Data assegnazione**: 2026-06-14  
**Dipendenza**: M1-T2-B implementazione da Claude Code (`M1-T2-B-TASK-CLAUDE.md`)

---

## 1. Obiettivo

Validare il tool `remote_validation_probe.rs` implementato da Claude Code, verificando error handling, documentazione e correttezza degli exit codes. Produrre `COMMUNICATION/VALIDATION_REPORT.md` in `tr4d3rz-messaging`.

---

## 2. Checklist di validazione

### Error handling

- [ ] Connection Timeout (exit 1): il probe termina entro 10-12s se il broker non è raggiungibile.
- [ ] Auth Error (exit 2): il probe rileva e riporta correttamente un ConnAck con codice di errore.
- [ ] Integrity Failure (exit 3): se il payload loopback viene alterato, il probe lo rileva.
- [ ] Variabile mancante (exit 4): messaggio d'errore chiaro se `TR4D3RZ_BROKER_IP` non è impostata.
- [ ] Nessun panic non gestito: tutti i path di errore usano exit codes, non `unwrap()` non protetti.

### Documentazione

- [ ] Il modulo ha un doc-comment `//!` con: descrizione, workflow, prerequisiti, utilizzo, exit codes.
- [ ] Ogni funzione pubblica o significativa ha un doc-comment `///`.
- [ ] `README.md` di `tr4d3rz-messaging` contiene una sezione "Remote Validation" con istruzioni d'uso.
- [ ] La sezione README include: come creare `.env.test`, come eseguire il probe, interpretazione degli exit codes.

### Sicurezza e convenzioni

- [ ] `.env.test` è presente in `.gitignore`.
- [ ] Nessun IP hardcodato nel codice (tutto via variabile d'ambiente).
- [ ] Il `CLIENT_ID` è univoco e descrittivo (`tr4d3rz-validator-probe`).

### Build e compilazione

- [ ] `cargo build --example remote_validation_probe` compila senza warning.
- [ ] `cargo clippy --example remote_validation_probe` non produce warning critici.

---

## 3. Output richiesto

Creare `COMMUNICATION/VALIDATION_REPORT.md` in `tr4d3rz-messaging` con:
- Data validazione.
- Risultato per ogni voce della checklist (PASS / FAIL / N/A).
- Note su eventuali problemi riscontrati.
- Raccomandazione finale: APPROVED o REQUIRES_FIXES.

Se APPROVED, notificare Manus aggiornando `tr4d3rz-docs/COMMUNICATION/PROJECT_STATE.md` con stato M1-T2-B = COMPLETED.

---

*Approvato da: Manus (Chief Architect) — 2026-06-14*
