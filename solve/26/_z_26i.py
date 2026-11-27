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
# estimation FFT toutes les 5 ms
win = int(rate * 0.005)
hop = win // 2
nf = (len(x) - win) // hop
freq = np.zeros(nf)
for i in range(nf):
    seg = x[i * hop:i * hop + win] * np.hanning(win)
    sp = np.abs(np.fft.rfft(seg))
    freq[i] = np.fft.rfftfreq(win, 1.0 / rate)[int(np.argmax(sp))]
print("fenetres:", nf, "duree/fenetre=%.1f ms" % (hop / rate * 1000))
sync = (freq > 1150) & (freq < 1260)
runs = []
i = 0
while i < len(sync):
    if sync[i]:
        j = i
        while j < len(sync) and sync[j]:
            j += 1
        runs.append((i * hop, (j - i) * hop))
        i = j
    else:
        i += 1
print("syncs:", len(runs), "| durees (ms):", [round(r[1] / rate * 1000, 1) for r in runs[:10]])
if len(runs) < 10:
    sys.exit(1)
# periode de ligne estimee = mediane des ecarts
starts = np.array([r[0] for r in runs])
d = np.diff(starts)
print("ecarts (ms) median: %.1f" % (np.median(d) / rate * 1000))
PIX = 320
SCAN = 146.4
pix_n = int(SCAN / 1000 * rate / PIX)
img = np.zeros((min(len(starts), 256), PIX, 3), dtype=np.uint8)
print("pixels par scan:", pix_n)


def freq_px(a, b):
    seg = x[a:b]
    if len(seg) < 4:
        return 1500.0
    s = np.sign(seg)
    s[s == 0] = 1
    c = np.sum(np.abs(np.diff(s)) > 0)
    return c / 2.0 / ((b - a) / rate)


rows = 0
for li, st in enumerate(starts[:256]):
    base = st
    ok = False
    for ci, cname in enumerate(("G", "B", "R")):
        chan = {"R": 0, "G": 1, "B": 2}[cname]
        off = base + int((9.0 + 1.5 + ci * (SCAN + 1.5)) / 1000 * rate)
        for px in range(PIX):
            a = off + px * pix_n
            b = a + pix_n
            if b >= len(x):
                break
            f = freq_px(a, b)
            v = (f - 1500.0) / 800.0 * 255.0
            img[li, px, chan] = int(max(0, min(255, v)))
        ok = True
    if ok:
        rows += 1
print("lignes:", rows)
Image.fromarray(img[:rows]).save("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/26_manual2.png")
print("ecrit 26_manual2.png")
