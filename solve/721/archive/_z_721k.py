import sys, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rows = []
for line in open("/tmp/tl721.txt", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("|")
    if len(p) < 11:
        continue
    try:
        mt, at, ct, cr = int(p[7]), int(p[8]), int(p[9]), int(p[10])
        size = int(p[6])
    except ValueError:
        continue
    if p[3].startswith("l/"):
        continue
    rows.append((cr, size, p[1], p[3], mt, at, ct))
rows.sort(reverse=True)
print("=== 15 crtime les plus recents (hors liens) ===")
for cr, size, path, perms, mt, at, ct in rows[:15]:
    f = lambda t: datetime.datetime.fromtimestamp(t, datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
    print("  cr=%s m=%s a=%s size=%-5d %s" % (f(cr), f(mt)[11:], f(at)[11:], size, path[:60]))
