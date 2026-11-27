#!/usr/bin/env python3
import sys, wave
import numpy as np
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/26_message.wav"
w = wave.open(P, "rb")
rate = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
w.close()
x = x - x.mean()
win = int(rate * 0.005)
hop = win // 2
nf = (len(x) - win) // hop
freq = np.zeros(nf)
for i in range(nf):
    seg = x[i * hop:i * hop + win] * np.hanning(win)
    freq[i] = np.fft.rfftfreq(win, 1.0 / rate)[int(np.argmax(np.abs(np.fft.rfft(seg))))]
sync = (freq > 1150) & (freq < 1260)
runs = []
i = 0
while i < len(sync):
    if sync[i]:
        j = i
        while j < len(sync) and sync[j]:
            j += 1
        runs.append(i * hop)
        i = j
    else:
        i += 1
print("syncs:", len(runs))
PIX = 320
SCAN_MS = 138.24
pix_n = SCAN_MS / 1000 * rate / PIX
img = np.zeros((min(len(runs), 256), PIX, 3), dtype=np.uint8)


def freq_px(a, b):
    seg = x[a:b]
    if len(seg) < 4:
        return 1500.0
    s = np.sign(seg)
    s[s == 0] = 1
    c = np.sum(np.abs(np.diff(s)) > 0)
    return c / 2.0 / ((b - a) / rate)


rows = 0
for li, st in enumerate(runs[:256]):
    for ci, chan in enumerate((1, 2, 0)):  # G, B, R
        off = st + int((9.0 + 1.5 + ci * (SCAN_MS + 1.5)) / 1000 * rate)
        for px in range(PIX):
            a = int(off + px * pix_n)
            b = int(a + pix_n)
            if b >= len(x):
                break
            f = freq_px(a, b)
            img[li, px, chan] = int(max(0, min(255, (f - 1500.0) / 800.0 * 255.0)))
    rows += 1
print("lignes:", rows)
Image.fromarray(img[:rows]).save("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/26_manual3.png")
print("ecrit 26_manual3.png")
