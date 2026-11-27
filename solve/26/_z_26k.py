import sys, wave, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np

p = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_m00n/message.wav"
w = wave.open(p, "rb")
sr = w.getframerate()
n = w.getnframes()
raw = w.readframes(n)
s = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
print("sr:", sr, "n:", n, "duration:", n / sr)
# frequence dominante par fenetre de 50 ms
win = int(sr * 0.05)
print("\nfreq dominante par fenetre de 50ms (10 premieres):")
for k in range(10):
    seg = s[k * win:(k + 1) * win]
    if len(seg) < win:
        break
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    freqs = np.fft.rfftfreq(len(seg), 1 / sr)
    peak = freqs[np.argmax(spec)]
    print(f"  t={k*0.05:.2f}s  peak={peak:.0f} Hz")
# chercher le leader 1900 Hz
win2 = int(sr * 0.01)
peaks = []
for k in range(0, min(n // win2, 1500)):
    seg = s[k * win2:(k + 1) * win2]
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    freqs = np.fft.rfftfreq(len(seg), 1 / sr)
    peaks.append(freqs[np.argmax(spec)])
peaks = np.array(peaks)
lead = np.where((peaks > 1800) & (peaks < 2000))[0]
print("\nfenetres a ~1900 Hz:", len(lead), "premier:", lead[:5] if len(lead) else None)
