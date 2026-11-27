import sys, wave
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
from PIL import Image

p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\117_main.wav"
w = wave.open(p, "rb")
sr = w.getframerate()
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
w.close()
a = a - a.mean()
print("echantillons:", len(a), "| sr:", sr)
win = 128
hop = 16
frames = []
for i in range(0, len(a) - win, hop):
    seg = a[i:i + win] * np.hanning(win)
    frames.append(np.abs(np.fft.rfft(seg)))
S = np.array(frames).T  # freq x time
print("spectrogramme:", S.shape)
S = 20 * np.log10(S + 1e-9)
S = np.clip((S - S.min()) / (S.max() - S.min()) * 255, 0, 255).astype(np.uint8)
img = Image.fromarray(S[::-1])  # freq en ordonnee croissante
img = img.resize((S.shape[1] * 3, S.shape[0] * 3), Image.NEAREST)
out = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\117_spec.png"
img.save(out)
print("ecrit:", out, img.size)
