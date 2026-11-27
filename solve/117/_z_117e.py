import sys, wave, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np

p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\117_main.wav"
w = wave.open(p, "rb")
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(int)
w.close()
print("premiers echantillons:", a[:8].tolist())
vals = [int(str(v)[:-2]) for v in a]
uniq = sorted(set(vals))
print("valeurs uniques:", uniq, "| nombre:", len(uniq))
hexdigits = "0123456789abcdef"
s = "".join(hexdigits[uniq.index(v)] for v in vals)
print("longueur hex:", len(s))
if len(s) % 2:
    s = s[:-1]
try:
    raw = bytes.fromhex(s)
except Exception as e:
    print("err hex:", e)
    raw = b""
print("=== texte decode ===")
print(raw.decode("latin-1", "replace")[:1500])
m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", raw)
print("\nFLAG:", m.group(0).decode() if m else None)
