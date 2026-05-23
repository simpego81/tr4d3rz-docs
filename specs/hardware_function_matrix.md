# Matrice Hardware-Funzioni dell'Ecosistema TR4D3RZ

Questa tabella mappa i dispositivi tecnologici previsti sulle macro-funzioni del sistema, per facilitare la selezione dei nodi per l'MVP. La ristrutturazione Single RPi2 consolida broker, gateway locale e persistenza sulla **Raspberry Pi 2 Model B (2015)**.

| Dispositivo | Evolution | Optimization | Persistence | Observatory | Gateway | Broker | Note Tecniche |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Linux PC** | [X] | [ ] | [ ] | [X] | [X] | [ ] | Nodo primario per sviluppo, debug e carichi evolutivi. x86_64, Rust, Python, Full UI. |
| **Android Tablet** | [X] | [ ] | [ ] | [X] | [ ] | [ ] | Schermo grande, ideale per Observatory Mobile. ARM64. |
| **Android Smartphone** | [X] | [ ] | [ ] | [X] | [ ] | [ ] | Observatory "light" e Evolution mobile. |
| **Raspberry Pi 2** | [ ] | [ ] | [X] | [ ] | [X] | [X] | ARMv7 quad-core 900MHz, 1GB RAM. Nodo centrale consolidato: NanoMQ, scraper, Event Logger, Persistence Service e relay/gateway locale. |
| **MIMXRT1050-EVK** | [X] | [X] | [ ] | [ ] | [ ] | [ ] | Cortex-M7 (600MHz). Evoluzione "bare-metal" veloce. |
| **Renesas RA8** | [ ] | [X] | [ ] | [ ] | [ ] | [ ] | Cortex-M85 con Helium (SIMD). Ottimo per FSM pesanti. |
| **ESP8266 (WiFi)** | [ ] | [X] | [ ] | [ ] | [ ] | [ ] | Xtensa, 80KB RAM. Connettività WiFi nativa verso l'IP unico della RPi2. |
| **STM32F3 Discovery** | [ ] | [X] | [ ] | [ ] | [ ] | [ ] | Cortex-M4 con FPU. Calcolo fitness floating-point; raggiunge MQTT tramite bridge/gateway verso RPi2 se privo di rete diretta. |
| **STM32F107VC** | [ ] | [X] | [ ] | [ ] | [ ] | [ ] | Cortex-M3. UART-only, richiede bridge verso l'IP unico della RPi2. |
| **Olimex STR-E912** | [ ] | [ ] | [ ] | [ ] | [X] | [ ] | ARM9. Bridge UART -> Ethernet/MQTT verso il nodo centrale RPi2. |
| **M24LR Discovery** | [ ] | [X] | [ ] | [ ] | [ ] | [ ] | NFC/RFID passivo. Scambio capsule offline. |
| **Web Browser** | [ ] | [X]* | [ ] | [X] | [ ] | [ ] | *Optimization tramite Replay/WASM. |
| **Hosting PHP** | [ ] | [ ] | [X] | [ ] | [ ] | [ ] | Backup lineage e Archetype Memory remota. |

## Definizioni Funzioni
- **Evolution:** Generazione genomi (L-System), mutazioni, gestione popolazione e nicchie.
- **Optimization:** Esecuzione FSM (Phenotype Runtime) e calcolo fitness su dati locali.
- **Persistence:** Archiviazione eventi, database dei lineage e memoria collettiva (archetipi).
- **Observatory:** Visualizzazione real-time, 3D Galaxy, replay e monitoraggio.
- **Gateway:** Traduzione protocolli (es. UART -> MQTT) e gestione nodi offline.
- **Broker:** Servizio MQTT centrale e WebSocket endpoint per i nodi locali.

---

## Analisi per MVP (Walking Skeleton)
Per un **Walking Skeleton** efficace, è necessario scegliere almeno un dispositivo per ogni colonna "X":

1.  **Evolution:** Linux PC (più semplice da debuggare inizialmente).
2.  **Optimization:** ESP8266 (WiFi nativo) o STM32F3 (se serve FPU).
3.  **Persistence / Gateway / Broker:** Raspberry Pi 2 come nodo centrale unico.
4.  **Observatory:** Web Browser (accessibile ovunque).

La capacità quad-core della Raspberry Pi 2 consente l'esecuzione parallela di **Scraper**, **Broker** e **Logger**, a condizione di mantenere NanoMQ prioritario rispetto ai picchi di I/O dello scraper e alle scritture append-only del logger.
