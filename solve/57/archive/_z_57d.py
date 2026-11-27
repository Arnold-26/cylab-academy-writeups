import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\57_win-exec-1.exe"
d = open(p, "rb").read()
i = d.find(b"academy{")
print("=== zone autour du prefixe (1200 octets) ===")
seg = d[max(0, i-200):i+1200]
txt = re.sub(rb"[^\x20-\x7e]", b"\n", seg).decode("latin-1")
lines = [l.strip() for l in txt.split("\n") if len(l.strip()) >= 3]
for l in lines[:60]:
    print("  ", l[:100])
