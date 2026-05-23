# TR4D3RZ — ArchiMate Site Documentation for AI Agents

## Overview
This document provides instructions for other AI agents (e.g., Claude Code, GitHub Copilot, Gemini CLI) that will work on the TR4D3RZ project. It explains the structure of the ArchiMate documentation site, how to read the architecture, and how to update it.

## The ArchiMate Documentation Site
The official architecture documentation is hosted on GitHub Pages:
**URL:** [https://simpego81.github.io/tr4d3rz-docs/](https://simpego81.github.io/tr4d3rz-docs/)

### Site Structure
The site is built as a static HTML generator (no build step, pure Python script). It consists of:
1.  **Homepage (`index.html`)**: A grid of 13 cards, each representing a specific `Technology_Device` in the TR4D3RZ ecosystem.
2.  **Device Pages (`[device].html`)**: 13 individual pages that render the ArchiMate elements specific to that device.

### The ArchiMate Grid
Each device page organizes architectural elements into a strict grid based on the ArchiMate 3.2 specification:
*   **Rows (Layers)**: Motivation, Business, Application, Technology.
*   **Columns (Aspects)**: Active Structure, Behavior, Passive Structure, Motivation.

### Interactive Elements
Every element in the grid is an interactive box. Clicking an element opens a modal popup containing:
*   **Type**: The exact ArchiMate element type (e.g., `Application_Component`).
*   **Role in TR4D3RZ**: A semantic description of what the element does in the context of the project.
*   **Technology**: Specific technical implementation details (e.g., "NanoMQ on Raspberry Pi 2 ARMv7", "SQLite event logger", "MQTT WebSocket bridge").
*   **Relationships**: How this element connects to others (e.g., "Realizes MQTT Service").

## How to Read the Architecture
When assigned a task, you MUST consult the relevant device page to understand your constraints:
1.  **Identify your target device**: If you are writing infrastructure code for the central Raspberry Pi 2 node, look at `rasp2.html`. If you are writing the browser UI, look at `browser.html`.
2.  **Check the Application Layer**: See what components run on your device.
3.  **Check the Technology Layer**: See what runtime and infrastructure constraints apply (e.g., `rasp2` hosts NanoMQ, scraper/relay and persistence services for the MVP).
4.  **Check the Data Objects**: Understand what data structures your components must handle (e.g., CBOR vs JSON).

## How to Update the Architecture
If you need to change the architecture (e.g., adding a new component or changing a technology), you MUST follow this workflow:
1.  **Do NOT edit the HTML files directly.** They are auto-generated.
2.  **Edit the source PUML files**: The source files are located in `diagrams/per-device/` (e.g., `device_rasp2.puml`).
3.  **Update the generator**: If you add new elements, you MUST update the `KNOWLEDGE_BASE` dictionary inside the `generate_site_v2.py` script so the popup contains the correct description.
4.  **Run the generator**: Execute `python3.11 generate_site_v2.py` to rebuild the `docs/` folder.
5.  **Commit and Push**: Commit the changes to both the `.puml` files and the `docs/` folder. GitHub Pages will automatically redeploy.

## Source Code
The repository containing all source code and documentation is:
[https://github.com/simpego81/tr4d3rz-docs](https://github.com/simpego81/tr4d3rz-docs)

*Document authored by Manus AI — Chief Architect*
