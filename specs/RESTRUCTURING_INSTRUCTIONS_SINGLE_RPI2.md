# Direttive per la Riorganizzazione Architetturale: Consolidamento su Singola Raspberry Pi 2

## Contesto
A seguito della specifica dell'utente, l'ecosistema TR4D3RZ deve essere riprogettato per operare con una **singola Raspberry Pi 2 Model B (2015)**, eliminando ogni riferimento a Raspberry Pi 1 o a nodi di persistenza multipli basati su RPi. 

**Nota tecnica:** La RPi 2 (ARMv7, quad-core, 1GB RAM) è più potente della RPi 1 precedentemente ipotizzata, il che permette un consolidamento più stabile dei servizi critici.

---

## Task List per Manus (Chief Architect)

### 1. Revisione delle Specifiche Master
*   **File:** `specs/manus_master_spec.md`
*   **Azione:** Unificare la "Classe 1 (Core Infrastructure)" e la "Classe 4 (Persistence)" in un'unica classe di nodo: **"Central Infrastructure & Persistence Node"**.
*   **Hardware Target:** Aggiornare la lista hardware rimuovendo RPi 1 e confermando RPi 2 come spina dorsale del sistema.

### 2. Aggiornamento della Matrice Hardware-Funzioni
*   **File:** `specs/hardware_function_matrix.md`
*   **Azione:** 
    *   Rimuovere la riga dedicata alla Raspberry Pi 1.
    *   Aggiornare la riga **Raspberry Pi 2** segnando come attive le funzioni: `Persistence`, `Gateway`, e `Broker` (precedentemente assegnata a RPi 1).
    *   Aggiungere una nota sulla capacità quad-core che permette l'esecuzione parallela di Scraper, Broker e Logger.

### 3. Aggiornamento dei Diagrammi ArchiMate (.puml)
*   **File:** `diagrams/archimate/archimate_diagram_v2.puml`
*   **Azione:** 
    *   Eliminare il `package "Core Infrastructure Node [Raspberry Pi 1]"` e il relativo elemento `Technology_Device(hw_rpi1, ...)`.
    *   Spostare tutti i servizi assegnati a RPi 1 (MQTT Broker, Web Server, Scraper) all'interno del `package "Persistence Node [Raspberry Pi 2]"`.
    *   Ridenominare il package risultante in **"Central Node [Raspberry Pi 2]"**.
    *   Aggiornare le relazioni `Rel_Assignment` per puntare a `hw_rpi2`.

### 4. Riorganizzazione dei Diagrammi per Device
*   **Azioni:**
    *   **Eliminare** `diagrams/per-device/device_rpi1.puml`.
    *   **Aggiornare** `diagrams/per-device/device_rasp2.puml` (o ridenominarlo se necessario) per includere l'intero stack software consolidato (NanoMQ + Scraper + Event Logger + Persistence Service).

### 5. Aggiornamento degli ADR (Architecture Decision Records)
*   **File:** `adr/ADR-0003-mqtt-broker.md`
*   **Azione:** Aggiornare la sezione "Context" rimuovendo il vincolo ARMv6l/700MHz e sostituendolo con ARMv7/900MHz. Confermare NanoMQ come scelta ottimale per efficienza, pur notando che i problemi di "Illegal Instruction" di Mosquitto 2.x sono meno critici su ARMv7.

### 6. Pulizia e Rigenerazione Documentazione
*   **Script:** `scripts/generate_docs.ps1` e `scripts/generate_holistic_data.ps1`.
*   **Azione:** Rimuovere `rpi1` dalla `$deviceList`.
*   **File docs:** Eliminare `docs/rpi1.html`.
*   **Esecuzione:** Rigenerare l'intero sito della documentazione per riflettere i cambiamenti nei metadati KB e nelle relazioni.

### 7. Impatto sui Nodi Distribuiti
*   Assicurarsi che le specifiche di connettività per **ESP8266**, **STM32** e **Linux PC** puntino ora all'unico IP del nodo centrale RPi 2.
*   Documentare la gestione delle risorse sulla RPi 2: CPU affinity o priorità per assicurare che il Broker MQTT non soffra durante i picchi di scrittura dello Scraper o del Logger.

---

**Manus è incaricato di eseguire questa ristrutturazione con priorità assoluta per ristabilire la coerenza del Single Source of Truth.**
