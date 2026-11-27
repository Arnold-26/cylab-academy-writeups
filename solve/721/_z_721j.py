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
    rows.append((cr, size, p[1], p[3], mt, at, ct))
rows.sort(reverse=True)
print("=== 15 crtime les plus recents ===")
for cr, size, path, perms, mt, at, ct in rows[:15]:
    print("  cr=%s size=%-6d %-50s %s" % (
        datetime.datetime.fromtimestamp(cr, datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"),
        size, path[:50], perms))
print("\n=== fichiers de taille 40-60 octets, crees le plus tardivement ===")
for cr, size, path, perms, mt, at, ct in rows:
    if 35 <= size <= 70:
        print("  cr=%s size=%-4d %-55s %s" % (
            datetime.datetime.fromtimestamp(cr, datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"),
            size, path[:55], perms))
