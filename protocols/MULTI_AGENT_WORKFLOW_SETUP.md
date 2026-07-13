# Protocollo di Collaborazione Multi-Agent & Setup Progetti GitHub

Questo documento definisce il setup operativo per lo sviluppo della **Milestone 1 (Opzione 1: Foundational Backbone)** e la struttura dei repository GitHub.

---

## 1. Struttura dei Repository GitHub (Ecosistema TR4D3RZ)

Manus dovrà inizializzare i seguenti 4 repository, definendo per ciascuno le specifiche di interfaccia (contratti CBOR/MQTT) prima dell'implementazione.

### [REPO 1] `tr4d3rz-core` (The Engine)
- **Tecnologia:** Rust (`no_std`).
- **Run Mode:** 
  - **Linux:** Compilato come binario nativo o libreria dinamica.
  - **WASM:** Compilato in WebAssembly per il browser.
  - **Embedded:** Compilato come libreria statica inclusa nel firmware.

### [REPO 2] `tr4d3rz-embedded` (The HAL & Drivers)
- **Tecnologia:** C++/Rust.
- **Run Mode:** 
  - **Firmware Bare-Metal:** Unico binario "flashato" su ESP8266/STM32.
  - **Interazione:** Comunica con il Broker via WiFi (MQTT) o UART.

### [REPO 3] `tr4d3rz-messaging` (The Backbone)
- **Tecnologia:** NanoMQ (C), Node.js (Scraper).
- **Run Mode (su RPi 2):**
  - **NanoMQ:** Servizio di sistema (`systemd`) in background.
  - **Scraper:** Servizio Node.js (gestito via `pm2` o `systemd`) con task pianificati (`cron`).
  - **Deployment:** L'utente installa le dipendenze e configura i servizi sulla RPi 2.

### [REPO 4] `tr4d3rz-persistence` (The Memory)
- **Tecnologia:** Rust, SQLite.
- **Run Mode (su RPi 2):**
  - **Event Logger:** Binario Rust eseguito come servizio di sistema.
  - **Storage:** Scrive su file `.sqlite` e `.parquet` nel filesystem della RPi 2.
  - **Deployment:** Cross-compilazione da Linux a ARMv7 (RPi 2) e trasferimento via SCP/SSH.

### [REPO 5] `tr4d3rz-observatory` (The UI)
- **Tecnologia:** TS, Three.js, Vanilla CSS.
- **Run Mode:**
  - **Client-Side:** Eseguito nel browser dell'utente (PC/Tablet).
  - **Hosting:** File statici (HTML/JS) serviti da un web server leggero sulla RPi 2 o tramite GitHub Pages.
  - **Deployment:** "Build" degli asset e upload sul server di hosting.

---

## 4. Riepilogo Target e Modalità di Esecuzione

| Target | Repo Coinvolte | Modalità di Esecuzione |
| :--- | :--- | :--- |
| **Linux PC** | `core`, `observatory` | Binario nativo (Evolution) + Browser (UI). |
| **Raspberry Pi 2** | `messaging`, `persistence` | Servizi di sistema (Broker, Scraper, Logger). |
| **ESP8266 / STM32** | `embedded` (+ `core`) | Firmware unico (Bare-metal). |
| **Browser** | `observatory`, `core` (WASM) | Esecuzione Client-side (Visualizzazione e Replay). |
| **Android Tablet** | `observatory` | Browser mobile (Visualizzazione). |

---

## 2. Strategia Multi-Target: Una repo per target o repo condivise?

Dopo analisi architetturale, adottiamo un modello **Ibrido**:

1.  **Logica Condivisa (Core):** Una sola repo (`tr4d3rz-core`) per tutti i target. È fondamentale che il "cervello" (come viene interpretata una FSM) sia identico su Linux, Browser e STM32 per garantire la determinismo evolutivo. Rust permette di compilare la stessa logica per `x86`, `WASM` e `Cortex-M`.
2.  **Specializzazione Hardware (Embedded):** Una repo dedicata (`tr4d3rz-embedded`) che funge da contenitore per i vari progetti firmware. Ogni sottocartella (es. `/esp8266`, `/stm32f3`) gestisce le specificità del ferro, ma tutte "chiamano" la libreria core.
3.  **Servizi di Infrastruttura:** Repo separate per Messaggistica, Persistenza e UI per permettere cicli di deploy indipendenti (es. aggiornare l'interfaccia senza toccare il database).


---

## 2. Setup Operativo del Team AI (Ruoli e Protocollo)

Gli agent comunicano tramite file Markdown dedicati nella directory `COMMUNICATION/` di ogni repository.

### **Manus (Chief Architect & Technical Director)**
- **Responsabilità:** Scrittura specifiche tecniche, pianificazione milestone, design delle interfacce (contratti dati), coordinamento alto livello.
- **Output:** File `TASK_QUEUE.md` e `SPEC_MASTER.md`.
- **Focus:** Assicurarsi che ogni modifica sia scalabile oltre l'MVP.

### **Claude (Lead Implementer)**
- **Responsabilità:** Implementazione del codice core, logica complessa, integrazione di sistema secondo le specifiche di Manus.
- **Output:** Codice sorgente e file `IMPLEMENTATION_LOG.md`.
- **Focus:** Efficienza algoritmica e aderenza alle interfacce.

### **GitHub Copilot (Tester & Validator)**
- **Responsabilità:** Scrittura di unit/integration test, debugging locale, validazione sintattica, refactoring suggerito.
- **Output:** Test suite e file `VALIDATION_REPORT.md`.
- **Focus:** Qualità del codice e copertura dei test.

### **Claude Code (State Evaluator & QA)**
- **Responsabilità:** Valutazione dello stato globale, verifica della coerenza fra i repo, analisi dell'allineamento diagrammi-codice, ottimizzazione dei token. *(Ruolo trasferito da Antigravity, uscita 2026-07-13)*
- **Output:** File `PROJECT_STATE.md` e `ARCHITECTURAL_AUDIT.md`.
- **Focus:** Visione d'insieme e rispetto degli standard architetturali.

---

## 3. Logica di Compilazione e Deployment Embedded

È fondamentale che Manus istruisca Claude e Copilot sulla distinzione tra "Libreria" e "Firmware":

### 1. Relazione tra Core ed Embedded
- **`tr4d3rz-core` come Dipendenza:** Questo repository non produce un binario eseguibile per l'utente finale, ma una libreria (crate Rust o libreria C-compatible) altamente ottimizzata e `no_std`.
- **`tr4d3rz-embedded` come Host:** Questo repository contiene i progetti finali (es. `/firmware/esp8266-node`). In fase di compilazione, il sistema "pesca" la logica da `tr4d3rz-core` e la compila insieme ai driver hardware.

### 2. Ciclo di Vita del Software sui Target
- **Linux/Browser:** Eseguono il codice core direttamente (o via WASM) come parte di un'applicazione più grande.
- **Microcontrollori (ESP/STM):** Ricevono un **unico file binario** prodotto dalla compilazione di `tr4d3rz-embedded` + `tr4d3rz-core`. 

### 3. Ruolo dell'Orchestratore (User) nel Deployment
- Gli agent AI preparano i binari e li caricano su GitHub come **Release Artifacts**.
- L'utente umano scarica il binario specifico (es. `tr4d3rz_esp8266_v1.bin`) e lo scrive fisicamente sul dispositivo tramite strumenti come `esptool` o `ST-Link`.

---

## 4. Protocollo di Comunicazione (Markdown-Driven)

Per minimizzare il consumo di token e mantenere la persistenza del contesto:

1.  **Handover:** Manus scrive un task in `COMMUNICATION/TASKS/current_task.md`.
2.  **Esecuzione:** Claude legge il task, implementa e aggiorna `IMPLEMENTATION_LOG.md`.
3.  **Validazione:** Copilot esegue i test e scrive l'esito in `VALIDATION_REPORT.md`.
4.  **Chiusura:** Claude Code legge i log, verifica l'allineamento con l'architettura globale e aggiorna il `PROJECT_STATE.md` dichiarando il task "COMPLETED" o richiedendo correzioni.

---

## 4. Istruzioni Immediate per Manus

1.  **Creare i 4 repository** su GitHub con una struttura README standard.
2.  **Definire i contratti di interfaccia** in `tr4d3rz-docs/protocols/` (es. schema CBOR per il genoma).
3.  **Inizializzare la directory `COMMUNICATION/`** in ogni repository per abilitare il flusso degli agent.
4.  **Assegnare il primo task a Claude:** Implementazione del broker MQTT consolidato su RPi 2 (secondo le nuove istruzioni `RESTRUCTURING_INSTRUCTIONS_SINGLE_RPI2.md`).
