# Edge QR Scanner — M5Stack UnitV K210 (OV7740)

Offline QR code scanner on the **M5Stack UnitV K210 AI Camera M12 (OV7740)** using **MaixPy**.  
Scans QR codes on-device, validates with a multi-frame stability lock, and logs results to internal flash — no cloud, no Wi‑Fi required.

---

## Demo

### 1. QR Scanner Demo
Live QR detection on UnitV K210 (MaixPy IDE preview)

<video controls width="100%" playsinline preload="metadata">
  <source src="https://cdn.jsdelivr.net/gh/adilzahoor2812/unitv-qr-scanner@main/qr-scanner.mp4" type="video/mp4">
</video>

### 2. Serial Monitor Demo
Decoded QR payload printed on the serial console

<video controls width="100%" playsinline preload="metadata">
  <source src="https://cdn.jsdelivr.net/gh/adilzahoor2812/unitv-qr-scanner@main/serial-monitor.mp4" type="video/mp4">
</video>

**What you will see**
- Live camera preview in MaixPy IDE
- QR detection with on-screen box
- Console / serial output of scanned payloads
- Offline scanning workflow on UnitV K210

---

## Hardware

| Item | Details |
|------|---------|
| Device | M5Stack **UnitV K210** M12 Version (OV7740) |
| MCU / AI | Kendryte K210 + KPU |
| Camera | OV7740, ~80° M12 lens |
| Host (dev) | Mac + USB-C |
| Storage | Internal flash (`/flash/scans.txt`) |

**Not required for MVP:** ESP32, Wi‑Fi, microSD, display.

---

## Features

- On-device QR decoding (`image.find_qrcodes()`)
- Stability lock (same payload across consecutive frames before accept)
- Minimum size filter (rejects far / tiny codes)
- Duplicate cooldown (avoids spam while holding the same QR)
- Append-only audit log on flash
- Runs from MaixPy IDE; can auto-start via `main.py`

---

## Project structure

```text
unitv-qr-scanner/
├── README.md
├── main.py                 # QR scanner + flash logging
├── qr-scanner.mp4          # demo (plays in README)
└── serial-monitor.mp4      # serial demo (plays in README)
```

---

## Firmware & tools

1. **MaixPy firmware** for UnitV / M5StickV  
   - Recommended for QR: full StickV package, e.g. `M5StickV_Firmware_v5.1.2.kfpkg`  
   - Flash with [Kflash_GUI](https://github.com/sipeed/kflash_gui/releases)  
   - Board select: **M5StickV**
2. **MaixPy IDE** (Mac) — connect, run, optional live preview  
3. Board in IDE: **Tools → Select Board → M5StickV**

> Note: “minimum” MaixPy builds may strip OpenMV QR APIs. If `find_qrcodes` is missing, re-flash the full StickV/UnitV MaixPy firmware.

---

## Quick start

### 1. Flash firmware
- Connect UnitV via USB-C  
- Open Kflash_GUI → board **M5StickV** → burn MaixPy firmware → success  
- Unplug / replug  

### 2. Open MaixPy IDE
- Select board **M5StickV**  
- Connect to serial port (e.g. `cu.usbserial-...`)  

### 3. Run
- Open `main.py`  
- Click **Run**  
- Point a clear QR at the camera (good light, hold steady, fill a large part of the view)  

### 4. Read the log

```python
print(open("/flash/scans.txt").read())
```

Or from Mac (IDE closed):

```bash
ampy --port /dev/cu.usbserial-XXXX get /flash/scans.txt ./scans.txt
```

### 5. Auto-run on boot (optional)
In MaixPy IDE: save/upload this script as **`/flash/main.py`**.  
Then USB power alone is enough for scanning + logging.

---

## Usage tips (reliability)

| Tip | Why |
|-----|-----|
| Hold QR large and centered | Small codes decode poorly on QVGA |
| Prefer printed QR over phone screen | Less glare |
| Bright, even lighting | Fewer failed frames |
| Hold still ~0.5 s | Stability lock needs consecutive frames |
| Keep ~10–20 cm distance | Typical sweet spot for this lens |

Decoded text is **exactly** the QR payload (e.g. `STU2026001`, URL, or custom ID string).

---

## Example log format

`/flash/scans.txt`:

```text
123456,HELLO-UNITV
128902,STU2026001
135440,TOOL-17
```

Columns: `timestamp_ms,payload`

---

## Applications

- Lab / workshop **inventory** tagging  
- **Student / staff check-in** demo (offline audit trail)  
- Event badge scanning prototype  
- Teaching edge vision + embedded logging  

---

## Limitations

- Not as fast as a phone camera scanner  
- QVGA + wide lens → QR must be reasonably close and sharp  
- No built-in Wi‑Fi on UnitV (phone alerts need a later ESP32/Pi bridge)  
- Some microSD cards (especially 64 GB / exFAT) may not mount; flash logging avoids that  

---

## Possible extensions

- [ ] Button to clear log / switch inventory vs check-in mode  
- [ ] UART JSON output to ESP32 → web page / Telegram  
- [ ] AprilTag support for robotics targets  
- [ ] Custom TinyML classifier alongside QR for hybrid demos  

---

## Author

**Adil Zahoor**  
M.Sc. Artificial Intelligence — Berlin  
Embedded / edge AI experiments with M5Stack UnitV K210  

---

## License

MIT — free to use and modify for learning and portfolio demos.
