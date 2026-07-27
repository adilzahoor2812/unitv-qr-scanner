# Edge QR Check-in & Inventory Node
### M5Stack UnitV K210 · MaixPy · On-device computer vision

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Hardware](https://img.shields.io/badge/Hardware-UnitV%20K210-orange.svg)](https://docs.m5stack.com/en/unit/UNIT-V%20M12)
[![Runtime](https://img.shields.io/badge/Runtime-MaixPy-green.svg)](https://wiki.sipeed.com/soft/maixpy/en/)
[![Demo](https://img.shields.io/badge/Demo-Live%20Player-purple.svg)](https://adilzahoor2812.github.io/unitv-qr-scanner/)

Offline QR scanning on a **13 g edge-AI camera** — no cloud, no Wi‑Fi, no phone required.  
Built for **inventory tagging**, **lab/student check-in demos**, and **embedded vision portfolios**.

**Live demos:** [Open demo player](https://adilzahoor2812.github.io/unitv-qr-scanner/)

---

## Why this project

Most QR demos are phone apps or cloud APIs. This project runs **entirely on-device** on the Kendryte K210:

- Capture → decode → validate → log
- Works with USB power alone after `main.py` is installed
- Designed around real embedded constraints (QVGA, limited RAM, no OS)

That is the skill set recruiters look for in **embedded**, **edge AI**, and **sensor/verification** roles.

---

## Demo

### 1. QR Scanner Demo
Live detection in MaixPy IDE (bounding box + payload)

[![QR Scanner Demo](docs/qr-scanner.mp4.png)](https://adilzahoor2812.github.io/unitv-qr-scanner/)

### 2. Serial Monitor Demo
Decoded payload streamed to the host console / audit log

[![Serial Monitor Demo](docs/serial-monitor.mp4.png)](https://adilzahoor2812.github.io/unitv-qr-scanner/)

---

## System architecture

```text
┌─────────────────────────────────────────────┐
│              UnitV K210 (OV7740)             │
│  camera → find_qrcodes() → stability lock   │
│           → size filter → cooldown          │
│           → append /flash/scans.txt         │
└─────────────────────────────────────────────┘
        USB-C (dev)              USB power (deploy)
             │                          │
        MaixPy IDE                 standalone boot
        live preview               auto-run main.py
```

---

## Reliability design (not just a toy loop)

| Mechanism | Purpose |
|-----------|---------|
| **Multi-frame stability lock** | Same payload must appear on consecutive frames before accept |
| **Minimum size filter** | Rejects far/tiny codes that decode poorly on QVGA |
| **Cooldown** | Prevents duplicate spam while the code stays in view |
| **Flash audit log** | Persistent offline trail without microSD dependency |
| **No aggressive windowing** | Avoids OV7740 preview distortion that breaks decode |

---

## Hardware

| Item | Detail |
|------|--------|
| Device | [M5Stack UnitV K210 M12](https://docs.m5stack.com/en/unit/UNIT-V%20M12) (OV7740) |
| SoC | Kendryte K210 (RISC-V dual-core + KPU) |
| Optics | M12 wide lens (~80° FOV) |
| I/O | USB-C, Grove UART, 2 buttons, microSD slot |
| Dev host | macOS + MaixPy IDE + Kflash_GUI |

---

## Skills demonstrated

- Embedded MicroPython (MaixPy) on constrained MCU-class hardware  
- On-device computer vision / barcode-style decoding  
- Defensive event logic (debounce, cooldown, persistence)  
- Hardware bring-up (firmware flash, serial workflow, OV7740 tuning)  
- Technical documentation for reproducible demos  

---

## Repository layout

```text
unitv-qr-scanner/
├── README.md
├── LICENSE
├── main.py                 # production scanner script
├── qr-scanner.mp4          # demo clip
├── serial-monitor.mp4
└── docs/
    ├── index.html          # demo player (GitHub Pages)
    ├── qr-scanner.mp4.png
    └── serial-monitor.mp4.png
```

---

## Quick start

### 1. Flash MaixPy firmware
1. Connect UnitV via USB-C  
2. Open **Kflash_GUI** → board **M5StickV**  
3. Burn StickV/UnitV MaixPy firmware (full build recommended for QR APIs)  
4. Unplug / replug  

> Minimum MaixPy builds may strip OpenMV QR functions (`find_qrcodes`). Prefer full StickV firmware for this project.

### 2. Run in MaixPy IDE
1. **Tools → Select Board → M5StickV**  
2. Connect to the serial port (`cu.usbserial-...`)  
3. Open `main.py` → **Run**  
4. Present a sharp QR (good light, hold steady, fill a large part of the frame)  

### 3. Inspect the audit log

```python
print(open("/flash/scans.txt").read())
```

### 4. Deploy standalone
Save/upload as `/flash/main.py` so the node auto-starts on USB power.

---

## Example log format

`/flash/scans.txt`

```text
123456,HELLO-UNITV
128902,STU2026001
135440,TOOL-17
```

`timestamp_ms,payload`

Payload text is **exact** QR content (IDs, URLs, or structured strings you encode).

---

## Applications

- Workshop / lab **inventory** labeling  
- Offline **check-in** prototype (student / staff / visitor)  
- Event badge scanning without network dependency  
- Teaching edge vision + embedded logging  

---

## Limitations (honest)

- Not as fast as a modern smartphone scanner  
- QVGA + wide lens → QR must be relatively close and sharp  
- UnitV has no Wi‑Fi — phone/cloud alerts need a later host (ESP32/Pi)  
- Some microSD cards are unreliable on UnitV; this design logs to flash by default  

---

## Roadmap

- [ ] Button modes: inventory vs check-in  
- [ ] UART JSON output to ESP32 → web / Telegram gateway  
- [ ] AprilTag mode for robotics targets  
- [ ] Optional TinyML class head for hybrid QR + object context  

---

## Author

**Adil Zahoor**  
M.Sc. Artificial Intelligence — Berlin  
Focus: embedded systems, edge perception, sensor verification  

GitHub: [adilzahoor2812](https://github.com/adilzahoor2812)

---

## License

This project is released under the [MIT License](LICENSE).
