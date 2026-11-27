import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\57_win-exec-1.exe"
d = open(p, "rb").read()
seen = []
for m in re.finditer(rb"[ -~]{4,120}", d):
    s = m.group(0).decode("latin-1")
    if s not in seen:
        seen.append(s)
print("chaines distinctes:", len(seen))
for s in seen:
    if any(k in s.lower() for k in ("code", "vault", "key", "acade", "vault", "access", "secret", "congrat", "correct")):
        print("  ", s[:120])
