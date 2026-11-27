import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rows = []
for line in open("/tmp/84pkts.txt"):
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 3:
        continue
    fn, port, data = parts[0], parts[1], parts[2]
    if not port or not data:
        continue
    try:
        db = bytes.fromhex(data)
    except Exception:
        continue
    rows.append((int(fn), int(port), db))
one = [d for _, _, d in rows if len(d) == 1]
raw = bytes(c[0] for c in one)
print("brut:", raw.decode("latin-1", "replace"))
# dedupe des repetitions consecutives
out = bytearray()
for ch in raw:
    if not out or out[-1] != ch:
        out.append(ch)
print("\ndeduit:", out.decode("latin-1", "replace"))
# dedupe global (garder la premiere occurrence de chaque caractere dans l'ordre)
seen = set()
uniq = bytes(c for c in raw if not (c in seen or seen.add(c)))
print("\npremieres occurrences:", uniq.decode("latin-1", "replace"))
# par paquets de 2 (chaque char envoye 2 fois ?)
every2 = raw[::2]
print("\n1 sur 2:", every2.decode("latin-1", "replace"))
m = re.search(rb"\{[^}]*\}", raw)
print("\nentre accolades (brut):", m.group(0) if m else None)
