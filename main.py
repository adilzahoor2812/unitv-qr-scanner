"""
UnitV K210 — Offline QR Scanner with flash logging
Hardware: M5Stack UnitV K210 AI Camera M12 (OV7740)
Runtime: MaixPy (MicroPython)
"""

import sensor
import image
import time
import gc

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)  # 320x240 — avoid windowing (distorts OV7740)
sensor.set_auto_gain(True)
sensor.set_auto_whitebal(True)
sensor.skip_frames(time=1000)
sensor.run(1)

LOG = "/flash/scans.txt"
last_data = ""
last_time = 0
stable = 0

NEED_STABLE = 2      # same payload required this many frames
COOLDOWN_MS = 2000   # ignore same code for 2 seconds after log
MIN_SIZE = 70        # reject tiny / unreliable detections


def log_scan(data):
    line = "%d,%s\n" % (time.ticks_ms(), data)
    with open(LOG, "a") as f:
        f.write(line)
    print("SCAN OK:", data)


print("QR scanner ready")
print("Hold QR steady, large in frame, good light")

while True:
    gc.collect()
    img = sensor.snapshot()
    codes = img.find_qrcodes()

    if not codes:
        stable = 0
        time.sleep_ms(20)
        continue

    q = max(codes, key=lambda c: c.w() * c.h())
    data = q.payload()

    if q.w() < MIN_SIZE:
        print("move closer")
        stable = 0
        time.sleep_ms(20)
        continue

    img.draw_rectangle(q.rect(), color=(0, 255, 0), thickness=2)
    img.draw_string(2, 2, data[:24], color=(0, 255, 0), scale=1)

    if data == last_data:
        stable += 1
    else:
        last_data = data
        stable = 1

    print("reading %d/%d: %s" % (stable, NEED_STABLE, data))

    if stable >= NEED_STABLE:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_time) > COOLDOWN_MS:
            try:
                log_scan(data)
            except Exception as e:
                print("log error:", e)
            last_time = now
        stable = 0

    time.sleep_ms(20)
