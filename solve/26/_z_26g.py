#!/usr/bin/env python3
import sys, wave
import numpy as np
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = "/tmp/cylab_eps/26_message.wav"
w = wave.open(P, "rb")
rate = w.getframerate()
raw = w.readframes(w.getnframes())
w.close()
x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
print("rate", rate, "len", len(x), "duree", len(x) / rate)

# 1) frequence instantanee grossiere par fenetres de 1 ms (zero crossings)
win = int(rate * 0.001)
nwin = len(x) // win
fr = np.zeros(nwin)
for i in range(nwin):
    seg = x[i * win:(i + 1) * win]
    s = np.sign(seg)
    s[s == 0] = 1
    crossings = np.sum(np.abs(np.diff(s)) > 0)
    fr[i] = crossings / 2.0 / 0.001
print("freq: min %.0f max %.0f median %.0f" % (fr.min(), fr.max(), np.median(fr)))

# 2) detection des syncs : ~1200 Hz pendant >= 6 ms
sync = (fr > 1100) & (fr < 1300)
starts = []
i = 0
while i < len(sync):
    if sync[i]:
        j = i
        while j < len(sync) and sync[j]:
            j += 1
        if (j - i) >= 6:
            starts.append(i)
        i = j
    else:
        i += 1
print("syncs detectes:", len(starts), "premiers:", starts[:5])
if len(starts) < 2:
    print("pas assez de syncs")
    sys.exit(1)
line_ms = starts[1] - starts[0]
print("periode de ligne: %d ms" % line_ms)

# 3) decodage Scottie 1 : apres sync 9 ms + sep 1.5 ms -> G 146.4 ms, sep, B, sep, R
PIX = 320
SCAN = 146.4
img = np.zeros((256, PIX, 3), dtype=np.uint8)


def freq_at(t_ms, dur_ms):
    a = int((t_ms) / 1000 * rate)
    b = int((t_ms + dur_ms) / 1000 * rate)
    if b > len(x) or a >= b:
        return 1500.0
    seg = x[a:b]
    s = np.sign(seg)
    s[s == 0] = 1
    c = np.sum(np.abs(np.diff(s)) > 0)
    return c / 2.0 / (dur_ms / 1000.0)


pix_dur = SCAN / PIX
line = 0
for st in starts:
    if line >= 256:
        break
    base = st
    for ci, cname in enumerate(("G", "B", "R")):
        chan = {"R": 0, "G": 1, "B": 2}[cname]
        start = base + 9.0 + 1.5 + ci * (SCAN + 1.5)
        for px in range(PIX):
            f = freq_at(start + px * pix_dur, pix_dur)
            v = (f - 1500.0) / (2300.0 - 1500.0) * 255.0
            img[line, px, chan] = int(max(0, min(255, v)))
    line += 1
print("lignes decodees:", line)
Image.fromarray(img).save("/tmp/cylab_eps/26_manual.png")
print("ecrit 26_manual.png")
