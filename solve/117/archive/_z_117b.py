import sys, wave
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
p = r"/tmp/cylab_eps\117_main.wav"
w = wave.open(p, "rb")
print("channels:", w.getnchannels(), "| width:", w.getsampwidth(), "| rate:", w.getframerate(),
      "| frames:", w.getnframes(), "| duree:", w.getnframes() / w.getframerate())
data = w.readframes(w.getnframes())
w.close()
a = np.frombuffer(data, dtype=np.int16 if w.getsampwidth() == 2 else np.int8).astype(float)
print("echantillons:", len(a), "| min/max:", a.min(), a.max())
# FFT globale
spec = np.abs(np.fft.rfft(a))
freqs = np.fft.rfftfreq(len(a), 1.0 / w.getframerate())
top = np.argsort(spec)[-12:][::-1]
print("frequences dominantes:", [(round(freqs[i], 1), round(spec[i] / spec.max(), 3)) for i in top])
# decoupage en fenetres et detection de la frequence dominante
sr = w.getframerate()
win = 512
print("\n--- frequence dominante par fenetre (debut) ---")
seq = []
for i in range(0, min(len(a) - win, win * 60), win):
    seg = a[i:i + win] * np.hanning(win)
    s2 = np.abs(np.fft.rfft(seg))
    f2 = np.fft.rfftfreq(win, 1.0 / sr)
    k = int(np.argmax(s2))
    seq.append((round(f2[k], 1), round(s2[k], 1)))
print(seq[:40])
