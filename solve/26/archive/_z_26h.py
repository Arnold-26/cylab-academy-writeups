#!/usr/bin/env python3
import sys, wave
import numpy as np
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = "/tmp/cylab_eps/26_message.wav"
w = wave.open(P, "rb")
rate = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
w.close()
print("DC offset:", x.mean(), "| min/max:", x.min(), x.max())
x = x - x.mean()
win = 480  # 10 ms
n = len(x) // win
freqs = []
for i in range(min(n, 12000)):
    seg = x[i * win:(i + 1) * win]
    sp = np.abs(np.fft.rfft(seg * np.hanning(win)))
    f = np.fft.rfftfreq(win, 1.0 / rate)
    k = int(np.argmax(sp))
    freqs.append((f[k], sp[k]))
freqs = np.array(freqs)
print("freq dominante: min %.0f max %.0f median %.0f" % (freqs[:, 0].min(), freqs[:, 0].max(), np.median(freqs[:, 0])))
import collections
c = collections.Counter((freqs[:, 0] / 100).round() * 100)
print("top frequences:", c.most_common(10))
# segments a 1200 Hz
mask = (freqs[:, 0] > 1150) & (freqs[:, 0] < 1250)
runs = []
i = 0
while i < len(mask):
    if mask[i]:
        j = i
        while j < len(mask) and mask[j]:
            j += 1
        runs.append((i, j - i))
        i = j
    else:
        i += 1
print("runs 1200Hz (>=1):", len(runs), "durees (x10ms):", [r[1] for r in runs[:20]])
