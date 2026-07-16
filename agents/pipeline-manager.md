# Role: Pipeline Manager

**STATUS: STUB — attivo dopo M1 completion**

## Constitutional Mapping
- CONSTITUTION.md: pipeline manager
- Option C: claude subagent + GitHub Actions

## Quando diventa ACTIVE

Il Pipeline Manager diventa operativo quando:
- M1 è completato (T3, T4, T5 tutti COMPLETED)
- GitHub Actions è configurato nei repository `tr4d3rz-core` e `tr4d3rz-messaging`
- I workflow `.github/workflows/ci.yml` sono presenti e funzionanti

## Trigger Conditions (future)

L'Orchestratore spawna il Pipeline Manager quando:
- Un merge su `main` di un repo tr4d3rz-* è completato
- Il Developer chiede una run CI manuale post-implementazione
- L'owner richiede verifica dello stato CI prima di un release

## Responsabilità (future)

1. Triggerare GitHub Actions CI (`cargo test`, `cargo clippy`, `cargo build`)
2. Leggere i risultati della run (`gh run view`, `gh run list`)
3. Riportare pass/fail all'Orchestratore con log compatto
4. Se fail: triggerare il Debugger con l'output di errore

## Output Schema (futuro)

```json
{
  "status": "PASS | FAIL | PENDING | STUB",
  "run_id": "github-actions-run-id",
  "repo": "tr4d3rz-core",
  "tests": {"total": 8, "pass": 8, "fail": 0},
  "build": "SUCCESS | FAIL",
  "log_summary": "compact error output if any",
  "action_required": "none | trigger_debugger | escalate_owner"
}
```

## Prerequisiti per attivazione

- [ ] `.github/workflows/ci.yml` creato in `tr4d3rz-core`
- [ ] `.github/workflows/ci.yml` creato in `tr4d3rz-messaging`
- [ ] `gh` CLI configurato con token per lettura CI status
- [ ] Aggiornare questo file da STUB ad ACTIVE

## Brief Template (placeholder — non usare finché STATUS = STUB)

```
[STUB — Pipeline Manager non ancora attivo. Vedere prerequisites in agents/pipeline-manager.md]
```

*Maintainer: Claude Code (Orchestratore) — Creato: 2026-07-16 — Attivazione: post-M1*
