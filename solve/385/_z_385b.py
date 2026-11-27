import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

INPUT = 34414012771923267025329027534276989288205997301964262080788052262850398745
for ratio in (5, 1, 8, 40, 3, 4):
    out = INPUT * ratio
    h = format(out, "x")
    if len(h) % 2:
        h = "0" + h
    try:
        txt = bytes.fromhex(h).decode("ascii", errors="replace")
    except Exception:
        txt = "?"
    print(f"ratio {ratio}: {txt[:100]}")
    if "academy{" in txt or "picoCTF{" in txt:
        print("  >>> CANDIDAT:", txt)
